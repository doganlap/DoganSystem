"""
Tenant Admin API - Admin dashboard APIs for tenant management
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional, Any
import logging

from tenant_manager import TenantManager
from tenant_isolation import TenantIsolation
from employee_agent_system import EmployeeAgentSystem
from agent_teams import AgentTeams
from agent_hierarchy import AgentHierarchy
from module_marketplace import ModuleMarketplace
from usage_tracker import UsageTracker
from billing_system import BillingSystem
from subscription_plans import SubscriptionPlanManager
from metrics_collector import MetricsCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Tenant Admin API", version="1.0.0")

# CORS configuration - secure origins only
import os
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "https://doganconsult.com,https://www.doganconsult.com,https://api.doganconsult.com,https://ds.doganconsult.com").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Tenant-ID", "X-Requested-With"],
)

# Initialize managers
tenant_manager = TenantManager()
tenant_isolation = TenantIsolation(tenant_manager)
agent_system = EmployeeAgentSystem(tenant_isolation)
teams = AgentTeams(tenant_isolation, agent_system)
hierarchy = AgentHierarchy(tenant_isolation, agent_system)
marketplace = ModuleMarketplace(tenant_manager)
usage_tracker = UsageTracker(tenant_manager)
plan_manager = SubscriptionPlanManager()
billing = BillingSystem(tenant_manager, plan_manager, usage_tracker)
metrics_collector = MetricsCollector(tenant_isolation)


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "Tenant Admin API",
        "version": "1.0.0"
    }


@app.get("/api/v1/{tenant_id}/admin/dashboard")
async def get_tenant_dashboard(tenant_id: str):
    """Get comprehensive tenant dashboard"""
    tenant = tenant_manager.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Get all dashboard data
    agents = agent_system.list_agents(tenant_id)
    tenant_teams = teams.list_teams(tenant_id)
    tenant_modules = marketplace.get_tenant_modules(tenant_id)
    usage = usage_tracker.get_current_month_usage(tenant_id)
    quota = tenant_manager.get_tenant_quota(tenant_id)
    metrics_summary = metrics_collector.get_metric_summary(tenant_id)
    
    return {
        "tenant": {
            "tenant_id": tenant.tenant_id,
            "name": tenant.name,
            "status": tenant.status,
            "subscription_tier": tenant.subscription_tier
        },
        "agents": {
            "total": len(agents),
            "by_status": {
                "available": sum(1 for a in agents if a.status == "available"),
                "busy": sum(1 for a in agents if a.status == "busy")
            },
            "by_department": {}
        },
        "teams": {
            "total": len(tenant_teams),
            "teams": [{"team_id": t.team_id, "team_name": t.team_name} for t in tenant_teams]
        },
        "modules": {
            "total": len(tenant_modules),
            "modules": [{"module_name": m["module_name"], "enabled": m["enabled"]} for m in tenant_modules]
        },
        "usage": usage,
        "quota": quota,
        "metrics": metrics_summary
    }


@app.get("/api/v1/{tenant_id}/admin/statistics")
async def get_statistics(tenant_id: str):
    """Get tenant statistics"""
    agents = agent_system.list_agents(tenant_id)
    usage = usage_tracker.get_current_month_usage(tenant_id)
    metrics = metrics_collector.get_metric_summary(tenant_id)
    
    return {
        "tenant_id": tenant_id,
        "statistics": {
            "agents": {
                "total": len(agents),
                "available": sum(1 for a in agents if a.status == "available"),
                "busy": sum(1 for a in agents if a.status == "busy")
            },
            "usage": usage,
            "metrics": metrics
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
