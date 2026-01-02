"""
Event Bus - Event routing and distribution for multi-tenant system
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass
from queue import Queue
import threading

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

from tenant_isolation import TenantIsolation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Event:
    """Event in the event bus"""
    event_id: str
    tenant_id: str
    event_type: str
    source: str  # erpnext, system, workflow, etc.
    data: Dict[str, Any]
    timestamp: datetime
    processed: bool = False


class EventBus:
    """Event bus for routing events to workflows"""
    
    def __init__(
        self,
        tenant_isolation: TenantIsolation,
        redis_host: Optional[str] = None,
        redis_port: int = 6379
    ):
        self.tenant_isolation = tenant_isolation
        self.event_queue: Queue = Queue()
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.redis_client = None
        
        # Use Redis if available
        if redis_host and REDIS_AVAILABLE:
            try:
                self.redis_client = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    decode_responses=True
                )
                self.redis_client.ping()
                logger.info("Using Redis for event bus")
            except Exception as e:
                logger.warning(f"Redis not available, using in-memory queue: {str(e)}")
        
        self.running = False
    
    def publish_event(
        self,
        tenant_id: str,
        event_type: str,
        source: str,
        data: Dict[str, Any]
    ) -> str:
        """Publish an event"""
        import uuid
        
        event_id = f"evt_{uuid.uuid4().hex[:12]}"
        event = Event(
            event_id=event_id,
            tenant_id=tenant_id,
            event_type=event_type,
            source=source,
            data=data,
            timestamp=datetime.now()
        )
        
        if self.redis_client:
            # Publish to Redis
            event_data = {
                "event_id": event.event_id,
                "tenant_id": event.tenant_id,
                "event_type": event.event_type,
                "source": event.source,
                "data": event.data,
                "timestamp": event.timestamp.isoformat()
            }
            self.redis_client.publish(
                f"events:tenant:{tenant_id}",
                json.dumps(event_data)
            )
        else:
            # Add to in-memory queue
            self.event_queue.put(event)
        
        logger.info(f"Event published: {event_type} for tenant {tenant_id}")
        return event_id
    
    def subscribe(
        self,
        event_type: str,
        handler: Callable[[Event], None]
    ):
        """Subscribe to an event type"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def start(self):
        """Start event bus processing"""
        self.running = True
        
        if self.redis_client:
            # Start Redis subscriber
            subscriber_thread = threading.Thread(target=self._redis_subscriber_loop, daemon=True)
            subscriber_thread.start()
        else:
            # Start in-memory processor
            processor_thread = threading.Thread(target=self._process_events, daemon=True)
            processor_thread.start()
        
        logger.info("Event bus started")
    
    def _redis_subscriber_loop(self):
        """Redis subscriber loop"""
        pubsub = self.redis_client.pubsub()
        
        # Subscribe to all tenant event channels
        pubsub.psubscribe("events:tenant:*")
        
        while self.running:
            try:
                message = pubsub.get_message(timeout=1)
                if message and message["type"] == "pmessage":
                    event_data = json.loads(message["data"])
                    event = Event(
                        event_id=event_data["event_id"],
                        tenant_id=event_data["tenant_id"],
                        event_type=event_data["event_type"],
                        source=event_data["source"],
                        data=event_data["data"],
                        timestamp=datetime.fromisoformat(event_data["timestamp"])
                    )
                    self._handle_event(event)
            except Exception as e:
                logger.error(f"Error in Redis subscriber: {str(e)}")
    
    def _process_events(self):
        """Process events from queue"""
        while self.running:
            try:
                event = self.event_queue.get(timeout=1)
                self._handle_event(event)
            except:
                continue
    
    def _handle_event(self, event: Event):
        """Handle an event"""
        # Call registered handlers
        handlers = self.event_handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in event handler: {str(e)}")
        
        # Trigger workflows for this event type
        # This would integrate with workflow engine
        # workflow_engine.trigger_workflows_by_event(event.tenant_id, event.event_type, event.data)
    
    def stop(self):
        """Stop event bus"""
        self.running = False
        logger.info("Event bus stopped")


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    
    tenant_manager = TenantManager()
    tenant_isolation = TenantIsolation(tenant_manager)
    event_bus = EventBus(tenant_isolation)
    
    # Subscribe to events
    def handle_quotation_created(event: Event):
        print(f"Quotation created for tenant {event.tenant_id}: {event.data}")
    
    event_bus.subscribe("quotation_created", handle_quotation_created)
    
    # Start event bus
    event_bus.start()
    
    # Publish event
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        event_bus.publish_event(
            tenant_id=tenant.tenant_id,
            event_type="quotation_created",
            source="erpnext",
            data={"quotation_id": "QUO-00001"}
        )
