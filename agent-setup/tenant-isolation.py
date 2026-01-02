"""
Tenant Isolation - Ensures data isolation between tenants
Database connection routing and cross-tenant access prevention
"""

import os
import sqlite3
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from functools import wraps
from contextlib import contextmanager

from tenant_manager import TenantManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TenantContext:
    """Thread-local tenant context"""
    def __init__(self):
        self._tenant_id: Optional[str] = None
        self._tenant_db_path: Optional[Path] = None
    
    def set_tenant(self, tenant_id: str, db_path: Path):
        """Set current tenant context"""
        self._tenant_id = tenant_id
        self._tenant_db_path = db_path
    
    def get_tenant_id(self) -> Optional[str]:
        """Get current tenant ID"""
        return self._tenant_id
    
    def get_db_path(self) -> Optional[Path]:
        """Get current tenant database path"""
        return self._tenant_db_path
    
    def clear(self):
        """Clear tenant context"""
        self._tenant_id = None
        self._tenant_db_path = None


# Global tenant context (thread-local in production)
_tenant_context = TenantContext()


class TenantIsolation:
    """Manages tenant data isolation"""
    
    def __init__(self, tenant_manager: TenantManager, tenant_db_dir: str = "tenant_databases"):
        self.tenant_manager = tenant_manager
        self.tenant_db_dir = Path(tenant_db_dir)
        self.tenant_db_dir.mkdir(exist_ok=True)
    
    def get_tenant_database_path(self, tenant_id: str) -> Optional[Path]:
        """Get tenant database path"""
        # First check platform database
        import sqlite3
        platform_db = sqlite3.connect(self.tenant_manager.platform_db_path)
        platform_db.row_factory = sqlite3.Row
        cursor = platform_db.cursor()
        
        cursor.execute("""
            SELECT database_name, connection_string FROM tenant_databases WHERE tenant_id = ?
        """, (tenant_id,))
        
        row = cursor.fetchone()
        platform_db.close()
        
        if row:
            if row["connection_string"]:
                return Path(row["connection_string"])
            elif row["database_name"]:
                return self.tenant_db_dir / row["database_name"]
        
        # Fallback: construct path
        return self.tenant_db_dir / f"{tenant_id}.db"
    
    @contextmanager
    def tenant_database(self, tenant_id: str):
        """Context manager for tenant database connection"""
        # Verify tenant exists and is active
        tenant = self.tenant_manager.get_tenant(tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        if tenant.status not in ["trial", "active"]:
            raise ValueError(f"Tenant {tenant_id} is not active (status: {tenant.status})")
        
        # Get database path
        db_path = self.get_tenant_database_path(tenant_id)
        if not db_path.exists():
            raise ValueError(f"Database not found for tenant {tenant_id}")
        
        # Set tenant context
        old_tenant_id = _tenant_context.get_tenant_id()
        old_db_path = _tenant_context.get_db_path()
        
        _tenant_context.set_tenant(tenant_id, db_path)
        
        try:
            # Open database connection
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            
            try:
                yield conn
            finally:
                conn.close()
        finally:
            # Restore previous context
            if old_tenant_id:
                _tenant_context.set_tenant(old_tenant_id, old_db_path)
            else:
                _tenant_context.clear()
    
    def get_current_tenant_id(self) -> Optional[str]:
        """Get current tenant ID from context"""
        return _tenant_context.get_tenant_id()
    
    def require_tenant(self, tenant_id: str):
        """Decorator to require tenant context"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                current_tenant = _tenant_context.get_tenant_id()
                if current_tenant != tenant_id:
                    raise ValueError(f"Tenant mismatch: expected {tenant_id}, got {current_tenant}")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def validate_tenant_access(self, tenant_id: str, resource_tenant_id: str):
        """Validate that tenant can access resource"""
        if tenant_id != resource_tenant_id:
            raise PermissionError(f"Tenant {tenant_id} cannot access resource from tenant {resource_tenant_id}")
        return True
    
    def enforce_tenant_isolation(self, tenant_id: str):
        """Enforce tenant isolation for current operation"""
        current_tenant = _tenant_context.get_tenant_id()
        if current_tenant and current_tenant != tenant_id:
            raise SecurityError(f"Cross-tenant access detected: {current_tenant} trying to access {tenant_id}")
        
        _tenant_context.set_tenant(tenant_id, self.get_tenant_database_path(tenant_id))


class SecurityError(Exception):
    """Security violation exception"""
    pass


def tenant_required(func):
    """Decorator to require tenant context"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        tenant_id = _tenant_context.get_tenant_id()
        if not tenant_id:
            raise ValueError("Tenant context required but not set")
        return func(*args, **kwargs)
    return wrapper


def get_current_tenant_id() -> Optional[str]:
    """Get current tenant ID from context"""
    return _tenant_context.get_tenant_id()


def set_tenant_context(tenant_id: str, isolation: TenantIsolation):
    """Set tenant context (helper function)"""
    db_path = isolation.get_tenant_database_path(tenant_id)
    _tenant_context.set_tenant(tenant_id, db_path)


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    
    manager = TenantManager()
    isolation = TenantIsolation(manager)
    
    # Get tenant
    tenant = manager.get_tenant_by_subdomain("testco")
    if tenant:
        # Use tenant database
        with isolation.tenant_database(tenant.tenant_id) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM agents")
            result = cursor.fetchone()
            print(f"Agents in tenant {tenant.tenant_id}: {result['count']}")
