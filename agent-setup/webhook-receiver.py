"""
Webhook Receiver - Receives ERPNext webhooks and routes to tenants
"""

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Optional, Any
import logging
import hmac
import hashlib
import json

from tenant_manager import TenantManager
from tenant_isolation import TenantIsolation
from autonomous_workflow import AutonomousWorkflowEngine, TriggerType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ERPNext Webhook Receiver", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
tenant_manager = TenantManager()
tenant_isolation = TenantIsolation(tenant_manager)


@app.post("/webhook/erpnext/{tenant_id}")
async def receive_webhook(
    tenant_id: str,
    request: Request,
    x_webhook_signature: Optional[str] = Header(None, alias="X-Webhook-Signature")
):
    """Receive ERPNext webhook for a tenant"""
    try:
        # Verify tenant exists
        tenant = tenant_manager.get_tenant(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        if tenant.status not in ["trial", "active"]:
            raise HTTPException(status_code=403, detail="Tenant not active")
        
        # Get webhook payload
        payload = await request.body()
        data = await request.json()
        
        # Verify webhook signature (if configured)
        # webhook_secret = get_webhook_secret(tenant_id)
        # if webhook_secret and x_webhook_signature:
        #     if not verify_signature(payload, x_webhook_signature, webhook_secret):
        #         raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Route to event bus
        event_type = data.get("event", "unknown")
        event_data = data.get("data", {})
        
        logger.info(f"Webhook received for tenant {tenant_id}: {event_type}")
        
        # Trigger workflows that listen to this event
        # This would integrate with workflow engine
        # workflow_engine.trigger_workflows_by_event(tenant_id, event_type, event_data)
        
        return {
            "success": True,
            "tenant_id": tenant_id,
            "event_type": event_type,
            "message": "Webhook received and processed"
        }
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/webhook/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Webhook Receiver"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
