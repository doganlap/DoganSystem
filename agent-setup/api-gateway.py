"""
API Gateway - Main entry point for multi-tenant SaaS platform
Routes requests to appropriate tenant and handles authentication
Integrated with Unified Orchestrator
"""

from fastapi import FastAPI, Request, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging
import time
import os
from dotenv import load_dotenv

from tenant_manager import TenantManager
from tenant_isolation import TenantIsolation
from tenant_router import TenantRouter, get_tenant_id
from usage_tracker import UsageTracker, UsageMetric
from metrics_collector import MetricsCollector
from unified_orchestrator import UnifiedOrchestrator, UnifiedSystemConfig

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DoganSystem Multi-Tenant API Gateway", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
tenant_manager = TenantManager(
    platform_db_path=os.getenv("PLATFORM_DB_PATH", "platform.db")
)
tenant_isolation = TenantIsolation(
    tenant_manager,
    tenant_db_dir=os.getenv("TENANT_DB_DIR", "tenant_databases")
)
tenant_router = TenantRouter(tenant_manager, tenant_isolation)
usage_tracker = UsageTracker(tenant_manager)
metrics_collector = MetricsCollector(tenant_isolation)

# Initialize unified orchestrator
unified_config = UnifiedSystemConfig(
    platform_db_path=os.getenv("PLATFORM_DB_PATH", "platform.db"),
    tenant_db_dir=os.getenv("TENANT_DB_DIR", "tenant_databases"),
    default_erpnext_url=os.getenv("ERPNEXT_BASE_URL"),
    default_erpnext_api_key=os.getenv("ERPNEXT_API_KEY"),
    default_erpnext_api_secret=os.getenv("ERPNEXT_API_SECRET"),
    default_email_smtp_server=os.getenv("SMTP_SERVER"),
    default_email_smtp_port=int(os.getenv("SMTP_PORT", "587")),
    default_email_username=os.getenv("SMTP_USERNAME"),
    default_email_password=os.getenv("SMTP_PASSWORD"),
    claude_api_key=os.getenv("CLAUDE_API_KEY"),
    enable_multi_tenant=True,
    enable_autonomous_workflows=True,
    enable_self_healing=True,
    enable_email_processing=True,
    enable_employee_agents=True,
    enable_ksa_localization=True,
    enable_monitoring=True
)

unified_orchestrator = UnifiedOrchestrator(unified_config)

# Start unified orchestrator on startup
@app.on_event("startup")
async def startup_event():
    """Start unified orchestrator on API gateway startup"""
    logger.info("Starting unified orchestrator...")
    unified_orchestrator.start()
    logger.info("Unified orchestrator started")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop unified orchestrator on API gateway shutdown"""
    logger.info("Stopping unified orchestrator...")
    unified_orchestrator.stop()
    logger.info("Unified orchestrator stopped")


@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    """Middleware to set tenant context"""
    start_time = time.time()
    
    try:
        # Get tenant from request
        tenant_id = tenant_router.get_tenant_from_request(request)
        
        if tenant_id:
            # Set tenant context
            tenant_router.set_tenant_context(tenant_id)
            
            # Track API call
            usage_tracker.increment_api_call(tenant_id)
        
        # Process request
        response = await call_next(request)
        
        # Record metrics
        if tenant_id:
            response_time = time.time() - start_time
            metrics_collector.record_api_call(
                tenant_id=tenant_id,
                endpoint=request.url.path,
                response_time=response_time,
                status_code=response.status_code
            )
        
        return response
    except Exception as e:
        logger.error(f"Error in tenant middleware: {str(e)}")
        raise


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "DoganSystem Multi-Tenant API Gateway",
        "version": "1.0.0"
    }


@app.get("/api/v1/tenant/info")
async def get_tenant_info(tenant_id: str = Depends(get_tenant_id)):
    """Get current tenant information"""
    tenant = tenant_manager.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {
        "tenant_id": tenant.tenant_id,
        "name": tenant.name,
        "subdomain": tenant.subdomain,
        "status": tenant.status,
        "subscription_tier": tenant.subscription_tier
    }


@app.get("/api/v1/tenant/quota")
async def get_quota(tenant_id: str = Depends(get_tenant_id)):
    """Get tenant quotas"""
    quota = tenant_manager.get_tenant_quota(tenant_id)
    usage = usage_tracker.get_current_month_usage(tenant_id)
    
    return {
        "tenant_id": tenant_id,
        "quota": quota,
        "usage": usage
    }


@app.get("/api/v1/system/status")
async def get_system_status():
    """Get unified system status"""
    return unified_orchestrator.get_system_status()


@app.get("/api/v1/{tenant_id}/orchestrator/status")
async def get_tenant_orchestrator_status(tenant_id: str):
    """Get tenant orchestrator status"""
    try:
        orchestrator = unified_orchestrator.get_or_create_tenant_orchestrator(tenant_id)
        return orchestrator.get_status()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
