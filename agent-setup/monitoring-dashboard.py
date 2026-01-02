"""
Monitoring Dashboard - API endpoints for monitoring and dashboards
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional, Any
import logging

from tenant_manager import TenantManager
from tenant_isolation import TenantIsolation
from metrics_collector import MetricsCollector
from usage_tracker import UsageTracker
from employee_agent_system import EmployeeAgentSystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Monitoring Dashboard API", version="1.0.0")

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
metrics_collector = MetricsCollector(tenant_isolation)
usage_tracker = UsageTracker(tenant_manager)
agent_system = EmployeeAgentSystem(tenant_isolation)


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "Monitoring Dashboard API",
        "version": "1.0.0"
    }


@app.get("/api/v1/{tenant_id}/dashboard/overview")
async def get_dashboard_overview(tenant_id: str):
    """Get dashboard overview for tenant"""
    tenant = tenant_manager.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Get metrics summary
    metrics_summary = metrics_collector.get_metric_summary(tenant_id)
    
    # Get usage
    usage = usage_tracker.get_current_month_usage(tenant_id)
    
    # Get agents
    agents = agent_system.list_agents(tenant_id)
    
    # Get quota
    quota = tenant_manager.get_tenant_quota(tenant_id)
    
    return {
        "tenant_id": tenant_id,
        "tenant_name": tenant.name,
        "status": tenant.status,
        "subscription_tier": tenant.subscription_tier,
        "metrics": metrics_summary,
        "usage": usage,
        "agents": {
            "total": len(agents),
            "available": sum(1 for a in agents if a.status == "available"),
            "busy": sum(1 for a in agents if a.status == "busy")
        },
        "quota": quota
    }


@app.get("/api/v1/{tenant_id}/dashboard/metrics")
async def get_metrics(
    tenant_id: str,
    metric_name: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get metrics for tenant"""
    metrics = metrics_collector.get_metrics(tenant_id, metric_name, limit)
    
    return {
        "tenant_id": tenant_id,
        "metrics": [
            {
                "metric_name": m.metric_name,
                "value": m.value,
                "labels": m.labels,
                "timestamp": m.timestamp.isoformat()
            }
            for m in metrics
        ]
    }


@app.get("/api/v1/{tenant_id}/dashboard/usage")
async def get_usage(tenant_id: str):
    """Get usage for tenant"""
    usage = usage_tracker.get_current_month_usage(tenant_id)
    quota = tenant_manager.get_tenant_quota(tenant_id)
    quota_check = usage_tracker.check_quota_exceeded(tenant_id)
    
    return {
        "tenant_id": tenant_id,
        "usage": usage,
        "quota": quota,
        "quota_exceeded": quota_check["exceeded"],
        "violations": quota_check["violations"]
    }


@app.get("/api/v1/{tenant_id}/dashboard/agents")
async def get_agents_dashboard(tenant_id: str):
    """Get agents dashboard data"""
    agents = agent_system.list_agents(tenant_id)
    
    # Group by department
    by_department = {}
    for agent in agents:
        dept = agent.department or "Unassigned"
        if dept not in by_department:
            by_department[dept] = []
        by_department[dept].append({
            "agent_id": agent.agent_id,
            "employee_name": agent.employee_name,
            "role": agent.role,
            "status": agent.status
        })
    
    return {
        "tenant_id": tenant_id,
        "total_agents": len(agents),
        "by_department": by_department,
        "by_status": {
            "available": sum(1 for a in agents if a.status == "available"),
            "busy": sum(1 for a in agents if a.status == "busy"),
            "away": sum(1 for a in agents if a.status == "away"),
            "offline": sum(1 for a in agents if a.status == "offline")
        }
    }


@app.get("/api/admin/dashboard/overview")
async def get_admin_dashboard():
    """Get admin dashboard overview"""
    tenants = tenant_manager.list_tenants(limit=1000)
    
    total_tenants = len(tenants)
    active_tenants = sum(1 for t in tenants if t.status == "active")
    trial_tenants = sum(1 for t in tenants if t.status == "trial")
    
    return {
        "total_tenants": total_tenants,
        "active_tenants": active_tenants,
        "trial_tenants": trial_tenants,
        "suspended_tenants": sum(1 for t in tenants if t.status == "suspended"),
        "by_tier": {
            "starter": sum(1 for t in tenants if t.subscription_tier == "starter"),
            "professional": sum(1 for t in tenants if t.subscription_tier == "professional"),
            "enterprise": sum(1 for t in tenants if t.subscription_tier == "enterprise")
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
