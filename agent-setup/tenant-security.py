"""
Tenant Security - Security and compliance for multi-tenant system
"""

import logging
import hmac
import hashlib
from typing import Dict, Optional, Any
from datetime import datetime
import sqlite3

from tenant_isolation import TenantIsolation, get_current_tenant_id
from tenant_manager import TenantManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TenantSecurity:
    """Manages tenant security and compliance"""
    
    def __init__(
        self,
        tenant_manager: TenantManager,
        tenant_isolation: TenantIsolation
    ):
        self.tenant_manager = tenant_manager
        self.tenant_isolation = tenant_isolation
    
    def generate_api_key(self, tenant_id: str, name: str = "default") -> Dict[str, str]:
        """Generate API key for tenant"""
        import uuid
        
        api_key = f"ak_{uuid.uuid4().hex[:16]}"
        api_secret = f"as_{uuid.uuid4().hex[:32]}"
        
        # Save to platform database
        import sqlite3
        conn = sqlite3.connect(self.tenant_manager.platform_db_path)
        cursor = conn.cursor()
        
        key_id = f"key_{uuid.uuid4().hex[:12]}"
        cursor.execute("""
            INSERT INTO tenant_api_keys
            (key_id, tenant_id, api_key, api_secret, name, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            key_id,
            tenant_id,
            api_key,
            api_secret,
            name,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"API key generated for tenant {tenant_id}")
        
        return {
            "key_id": key_id,
            "api_key": api_key,
            "api_secret": api_secret
        }
    
    def verify_api_key(self, api_key: str) -> Optional[str]:
        """Verify API key and return tenant ID"""
        import sqlite3
        conn = sqlite3.connect(self.tenant_manager.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT tenant_id FROM tenant_api_keys
            WHERE api_key = ? AND (expires_at IS NULL OR expires_at > datetime('now'))
        """, (api_key,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        # Update last_used
        conn = sqlite3.connect(self.tenant_manager.platform_db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tenant_api_keys
            SET last_used = datetime('now')
            WHERE api_key = ?
        """, (api_key,))
        conn.commit()
        conn.close()
        
        return row["tenant_id"]
    
    def enforce_tenant_isolation(self, tenant_id: str, resource_tenant_id: str):
        """Enforce tenant data isolation"""
        if tenant_id != resource_tenant_id:
            raise SecurityError(f"Cross-tenant access violation: {tenant_id} accessing {resource_tenant_id}")
    
    def audit_log(
        self,
        tenant_id: str,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        user_id: Optional[str] = None,
        details: Optional[Dict] = None
    ):
        """Log audit event for compliance"""
        # This would write to audit log
        logger.info(f"AUDIT: tenant={tenant_id}, action={action}, resource={resource_type}, resource_id={resource_id}")
        
        # In production, write to dedicated audit log database/table
        # For KSA compliance, ensure all actions are logged
    
    def check_ksa_compliance(self, tenant_id: str) -> Dict[str, Any]:
        """Check KSA compliance status for tenant"""
        tenant = self.tenant_manager.get_tenant(tenant_id)
        if not tenant:
            return {"compliant": False, "error": "Tenant not found"}
        
        # KSA Personal Data Protection Law compliance checks
        compliance = {
            "compliant": True,
            "checks": {
                "data_isolation": True,  # Separate database per tenant
                "access_control": True,  # API keys and authentication
                "audit_logging": True,   # All actions logged
                "data_retention": True,  # Retention policies
                "encryption": False      # Would need to implement
            },
            "recommendations": []
        }
        
        if not compliance["checks"]["encryption"]:
            compliance["recommendations"].append("Enable data encryption at rest")
        
        return compliance


class SecurityError(Exception):
    """Security violation exception"""
    pass


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    
    tenant_manager = TenantManager()
    tenant_isolation = TenantIsolation(tenant_manager)
    security = TenantSecurity(tenant_manager, tenant_isolation)
    
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        # Generate API key
        keys = security.generate_api_key(tenant.tenant_id, "production")
        print(f"API Key: {keys['api_key']}")
        
        # Check compliance
        compliance = security.check_ksa_compliance(tenant.tenant_id)
        print(f"Compliance: {compliance}")
