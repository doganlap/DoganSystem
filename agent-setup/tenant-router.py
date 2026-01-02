"""
Tenant Router - Routes requests to correct tenant
Supports subdomain, path, and header-based routing
"""

from fastapi import Request, HTTPException
from typing import Optional
import logging

from tenant_manager import TenantManager
from tenant_isolation import TenantIsolation, set_tenant_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TenantRouter:
    """Routes requests to tenants"""
    
    def __init__(self, tenant_manager: TenantManager, tenant_isolation: TenantIsolation):
        self.tenant_manager = tenant_manager
        self.tenant_isolation = tenant_isolation
    
    def get_tenant_from_request(self, request: Request) -> Optional[str]:
        """Extract tenant ID from request"""
        # Method 1: Subdomain-based routing
        host = request.headers.get("host", "")
        if "." in host:
            subdomain = host.split(".")[0]
            tenant = self.tenant_manager.get_tenant_by_subdomain(subdomain)
            if tenant:
                return tenant.tenant_id
        
        # Method 2: Path-based routing (/api/tenant/{tenant_id}/...)
        path_parts = request.url.path.split("/")
        if len(path_parts) >= 3 and path_parts[1] == "api" and path_parts[2] == "tenant":
            if len(path_parts) >= 4:
                tenant_id = path_parts[3]
                tenant = self.tenant_manager.get_tenant(tenant_id)
                if tenant:
                    return tenant_id
        
        # Method 3: Header-based routing (X-Tenant-ID)
        tenant_id = request.headers.get("X-Tenant-ID")
        if tenant_id:
            tenant = self.tenant_manager.get_tenant(tenant_id)
            if tenant:
                return tenant_id
        
        # Method 4: Query parameter
        tenant_id = request.query_params.get("tenant_id")
        if tenant_id:
            tenant = self.tenant_manager.get_tenant(tenant_id)
            if tenant:
                return tenant_id
        
        return None
    
    def set_tenant_context(self, tenant_id: str):
        """Set tenant context for current request"""
        set_tenant_context(tenant_id, self.tenant_isolation)
    
    def require_tenant(self, request: Request) -> str:
        """Require tenant and raise if not found"""
        tenant_id = self.get_tenant_from_request(request)
        if not tenant_id:
            raise HTTPException(
                status_code=400,
                detail="Tenant ID required. Provide via subdomain, path, header, or query parameter."
            )
        
        # Verify tenant is active
        tenant = self.tenant_manager.get_tenant(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        if tenant.status not in ["trial", "active"]:
            raise HTTPException(status_code=403, detail=f"Tenant is not active (status: {tenant.status})")
        
        # Set tenant context
        self.set_tenant_context(tenant_id)
        
        return tenant_id


# Example usage as FastAPI dependency
def get_tenant_id(request: Request, router: TenantRouter) -> str:
    """FastAPI dependency to get tenant ID"""
    return router.require_tenant(request)
