"""
Tenant Management API - REST API for tenant operations
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
import logging

from tenant_manager import TenantManager, Tenant, TenantStatus
from tenant_provisioning import TenantProvisioner
from tenant_isolation import TenantIsolation, get_current_tenant_id, set_tenant_context

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Multi-Tenant SaaS Platform API", version="1.0.0")

# CORS middleware
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
tenant_provisioner = TenantProvisioner(
    tenant_manager,
    tenant_db_dir=os.getenv("TENANT_DB_DIR", "tenant_databases")
)
tenant_isolation = TenantIsolation(
    tenant_manager,
    tenant_db_dir=os.getenv("TENANT_DB_DIR", "tenant_databases")
)


# Request/Response models
class TenantCreateRequest(BaseModel):
    name: str
    subdomain: Optional[str] = None
    domain: Optional[str] = None
    subscription_tier: Optional[str] = "starter"
    trial_days: Optional[int] = 14


class TenantUpdateRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    subscription_tier: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class TenantResponse(BaseModel):
    tenant_id: str
    name: str
    subdomain: Optional[str]
    domain: Optional[str]
    status: str
    subscription_tier: str
    created_at: Optional[str]
    trial_end_date: Optional[str]


# Dependency to get tenant from header/subdomain
async def get_tenant_from_request(
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    subdomain: Optional[str] = Query(None)
) -> Optional[str]:
    """Extract tenant ID from request"""
    if x_tenant_id:
        return x_tenant_id
    if subdomain:
        tenant = tenant_manager.get_tenant_by_subdomain(subdomain)
        if tenant:
            return tenant.tenant_id
    return None


# Admin endpoints (no tenant required)
@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "Multi-Tenant SaaS Platform API",
        "version": "1.0.0"
    }


@app.post("/api/admin/tenants", response_model=Dict[str, Any])
async def create_tenant(request: TenantCreateRequest):
    """Create a new tenant (admin only)"""
    try:
        # Create tenant
        tenant = tenant_manager.create_tenant(
            name=request.name,
            subdomain=request.subdomain,
            domain=request.domain,
            subscription_tier=request.subscription_tier,
            trial_days=request.trial_days
        )
        
        # Provision tenant
        provision_result = tenant_provisioner.provision_tenant(tenant)
        
        return {
            "success": True,
            "tenant": {
                "tenant_id": tenant.tenant_id,
                "name": tenant.name,
                "subdomain": tenant.subdomain,
                "status": tenant.status,
                "subscription_tier": tenant.subscription_tier,
                "trial_end_date": tenant.trial_end_date.isoformat() if tenant.trial_end_date else None
            },
            "provisioning": provision_result
        }
    except Exception as e:
        logger.error(f"Error creating tenant: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/tenants", response_model=List[TenantResponse])
async def list_tenants(
    status: Optional[str] = Query(None),
    subscription_tier: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """List all tenants (admin only)"""
    try:
        tenants = tenant_manager.list_tenants(
            status=status,
            subscription_tier=subscription_tier,
            limit=limit,
            offset=offset
        )
        
        return [
            TenantResponse(
                tenant_id=t.tenant_id,
                name=t.name,
                subdomain=t.subdomain,
                domain=t.domain,
                status=t.status,
                subscription_tier=t.subscription_tier,
                created_at=t.created_at.isoformat() if t.created_at else None,
                trial_end_date=t.trial_end_date.isoformat() if t.trial_end_date else None
            )
            for t in tenants
        ]
    except Exception as e:
        logger.error(f"Error listing tenants: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/tenants/{tenant_id}", response_model=TenantResponse)
async def get_tenant(tenant_id: str = Path(...)):
    """Get tenant details (admin only)"""
    tenant = tenant_manager.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return TenantResponse(
        tenant_id=tenant.tenant_id,
        name=tenant.name,
        subdomain=tenant.subdomain,
        domain=tenant.domain,
        status=tenant.status,
        subscription_tier=tenant.subscription_tier,
        created_at=tenant.created_at.isoformat() if tenant.created_at else None,
        trial_end_date=tenant.trial_end_date.isoformat() if tenant.trial_end_date else None
    )


@app.put("/api/admin/tenants/{tenant_id}", response_model=Dict[str, Any])
async def update_tenant(
    tenant_id: str = Path(...),
    request: TenantUpdateRequest = None
):
    """Update tenant (admin only)"""
    tenant = tenant_manager.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    success = tenant_manager.update_tenant(
        tenant_id=tenant_id,
        name=request.name if request else None,
        status=request.status if request else None,
        subscription_tier=request.subscription_tier if request else None,
        metadata=request.metadata if request else None
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Update failed")
    
    updated_tenant = tenant_manager.get_tenant(tenant_id)
    return {
        "success": True,
        "tenant": {
            "tenant_id": updated_tenant.tenant_id,
            "name": updated_tenant.name,
            "status": updated_tenant.status,
            "subscription_tier": updated_tenant.subscription_tier
        }
    }


@app.post("/api/admin/tenants/{tenant_id}/suspend", response_model=Dict[str, Any])
async def suspend_tenant(tenant_id: str = Path(...)):
    """Suspend a tenant (admin only)"""
    success = tenant_manager.suspend_tenant(tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {"success": True, "message": f"Tenant {tenant_id} suspended"}


@app.post("/api/admin/tenants/{tenant_id}/activate", response_model=Dict[str, Any])
async def activate_tenant(tenant_id: str = Path(...)):
    """Activate a tenant (admin only)"""
    success = tenant_manager.activate_tenant(tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {"success": True, "message": f"Tenant {tenant_id} activated"}


@app.delete("/api/admin/tenants/{tenant_id}", response_model=Dict[str, Any])
async def delete_tenant(tenant_id: str = Path(...)):
    """Delete a tenant (admin only)"""
    success = tenant_manager.delete_tenant(tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {"success": True, "message": f"Tenant {tenant_id} deleted"}


@app.get("/api/admin/tenants/{tenant_id}/quota", response_model=Dict[str, Any])
async def get_tenant_quota(tenant_id: str = Path(...)):
    """Get tenant resource quotas (admin only)"""
    quota = tenant_manager.get_tenant_quota(tenant_id)
    if not quota:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {"tenant_id": tenant_id, "quota": quota}


# Tenant-scoped endpoints (require tenant context)
@app.get("/api/v1/tenant/info", response_model=TenantResponse)
async def get_tenant_info(tenant_id: Optional[str] = Depends(get_tenant_from_request)):
    """Get current tenant information"""
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID required")
    
    tenant = tenant_manager.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return TenantResponse(
        tenant_id=tenant.tenant_id,
        name=tenant.name,
        subdomain=tenant.subdomain,
        domain=tenant.domain,
        status=tenant.status,
        subscription_tier=tenant.subscription_tier,
        created_at=tenant.created_at.isoformat() if tenant.created_at else None,
        trial_end_date=tenant.trial_end_date.isoformat() if tenant.trial_end_date else None
    )


@app.get("/api/v1/tenant/quota", response_model=Dict[str, Any])
async def get_quota(tenant_id: Optional[str] = Depends(get_tenant_from_request)):
    """Get current tenant quotas"""
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID required")
    
    quota = tenant_manager.get_tenant_quota(tenant_id)
    if not quota:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {"tenant_id": tenant_id, "quota": quota}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
