"""
Metrics Collector - Collect system and business metrics per tenant
"""

import psutil
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

try:
    from prometheus_client import Counter, Gauge, Histogram, start_http_server
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    logger.warning("prometheus_client not installed. Install with: pip install prometheus-client")

from tenant_isolation import TenantIsolation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Metric:
    """Metric data point"""
    tenant_id: str
    metric_name: str
    value: float
    labels: Dict[str, str]
    timestamp: datetime


class MetricsCollector:
    """Collects metrics per tenant"""
    
    def __init__(self, tenant_isolation: TenantIsolation):
        self.tenant_isolation = tenant_isolation
        self.metrics: Dict[str, List[Metric]] = {}
        
        # Prometheus metrics (if available)
        if PROMETHEUS_AVAILABLE:
            self.agent_count = Gauge('dogansystem_agents_total', 'Number of agents', ['tenant_id'])
            self.workflow_executions = Counter('dogansystem_workflow_executions_total', 'Workflow executions', ['tenant_id', 'workflow_id', 'status'])
            self.api_calls = Counter('dogansystem_api_calls_total', 'API calls', ['tenant_id', 'endpoint'])
            self.response_time = Histogram('dogansystem_response_time_seconds', 'Response time', ['tenant_id', 'endpoint'])
            self.system_cpu = Gauge('dogansystem_cpu_usage_percent', 'CPU usage', ['tenant_id'])
            self.system_memory = Gauge('dogansystem_memory_usage_bytes', 'Memory usage', ['tenant_id'])
    
    def record_agent_count(self, tenant_id: str, count: int):
        """Record agent count"""
        if PROMETHEUS_AVAILABLE:
            self.agent_count.labels(tenant_id=tenant_id).set(count)
        
        self._record_metric(tenant_id, "agents", count, {})
    
    def record_workflow_execution(
        self,
        tenant_id: str,
        workflow_id: str,
        status: str,
        duration: Optional[float] = None
    ):
        """Record workflow execution"""
        if PROMETHEUS_AVAILABLE:
            self.workflow_executions.labels(
                tenant_id=tenant_id,
                workflow_id=workflow_id,
                status=status
            ).inc()
        
        self._record_metric(
            tenant_id,
            "workflow_execution",
            1,
            {"workflow_id": workflow_id, "status": status, "duration": duration or 0}
        )
    
    def record_api_call(
        self,
        tenant_id: str,
        endpoint: str,
        response_time: float,
        status_code: int = 200
    ):
        """Record API call"""
        if PROMETHEUS_AVAILABLE:
            self.api_calls.labels(tenant_id=tenant_id, endpoint=endpoint).inc()
            self.response_time.labels(tenant_id=tenant_id, endpoint=endpoint).observe(response_time)
        
        self._record_metric(
            tenant_id,
            "api_call",
            1,
            {"endpoint": endpoint, "response_time": response_time, "status_code": status_code}
        )
    
    def record_system_metrics(self, tenant_id: str):
        """Record system metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        if PROMETHEUS_AVAILABLE:
            self.system_cpu.labels(tenant_id=tenant_id).set(cpu_percent)
            self.system_memory.labels(tenant_id=tenant_id).set(memory.used)
        
        self._record_metric(tenant_id, "cpu_usage", cpu_percent, {})
        self._record_metric(tenant_id, "memory_usage", memory.used, {})
    
    def _record_metric(
        self,
        tenant_id: str,
        metric_name: str,
        value: float,
        labels: Dict[str, str]
    ):
        """Record a metric"""
        if tenant_id not in self.metrics:
            self.metrics[tenant_id] = []
        
        metric = Metric(
            tenant_id=tenant_id,
            metric_name=metric_name,
            value=value,
            labels=labels,
            timestamp=datetime.now()
        )
        
        self.metrics[tenant_id].append(metric)
        
        # Keep only last 1000 metrics per tenant
        if len(self.metrics[tenant_id]) > 1000:
            self.metrics[tenant_id] = self.metrics[tenant_id][-1000:]
    
    def get_metrics(
        self,
        tenant_id: str,
        metric_name: Optional[str] = None,
        limit: int = 100
    ) -> List[Metric]:
        """Get metrics for tenant"""
        if tenant_id not in self.metrics:
            return []
        
        metrics = self.metrics[tenant_id]
        
        if metric_name:
            metrics = [m for m in metrics if m.metric_name == metric_name]
        
        return metrics[-limit:]
    
    def get_metric_summary(self, tenant_id: str) -> Dict[str, Any]:
        """Get metric summary for tenant"""
        metrics = self.get_metrics(tenant_id)
        
        summary = {
            "tenant_id": tenant_id,
            "total_metrics": len(metrics),
            "by_metric": {}
        }
        
        for metric in metrics:
            if metric.metric_name not in summary["by_metric"]:
                summary["by_metric"][metric.metric_name] = {
                    "count": 0,
                    "total": 0,
                    "average": 0,
                    "min": float('inf'),
                    "max": float('-inf')
                }
            
            stat = summary["by_metric"][metric.metric_name]
            stat["count"] += 1
            stat["total"] += metric.value
            stat["min"] = min(stat["min"], metric.value)
            stat["max"] = max(stat["max"], metric.value)
        
        # Calculate averages
        for metric_name, stat in summary["by_metric"].items():
            if stat["count"] > 0:
                stat["average"] = stat["total"] / stat["count"]
            if stat["min"] == float('inf'):
                stat["min"] = 0
            if stat["max"] == float('-inf'):
                stat["max"] = 0
        
        return summary
    
    def start_prometheus_server(self, port: int = 8004):
        """Start Prometheus metrics server"""
        if PROMETHEUS_AVAILABLE:
            start_http_server(port)
            logger.info(f"Prometheus metrics server started on port {port}")
        else:
            logger.warning("Prometheus not available")


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    
    tenant_manager = TenantManager()
    tenant_isolation = TenantIsolation(tenant_manager)
    collector = MetricsCollector(tenant_isolation)
    
    # Start Prometheus server
    collector.start_prometheus_server()
    
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        # Record metrics
        collector.record_agent_count(tenant.tenant_id, 5)
        collector.record_workflow_execution(tenant.tenant_id, "workflow_001", "completed", 2.5)
        
        # Get summary
        summary = collector.get_metric_summary(tenant.tenant_id)
        print(f"Metrics summary: {summary}")
