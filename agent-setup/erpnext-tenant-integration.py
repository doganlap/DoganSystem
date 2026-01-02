"""
ERPNext Tenant Integration - Per-tenant ERPNext connections
"""

import sqlite3
import logging
from typing import Dict, Optional, Any
from datetime import datetime

from tenant_isolation import TenantIsolation
from agent_orchestrator import ERPNextClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ERPNextTenantIntegration:
    """Manages ERPNext connections per tenant"""
    
    def __init__(self, tenant_isolation: TenantIsolation):
        self.tenant_isolation = tenant_isolation
        self.clients: Dict[str, ERPNextClient] = {}  # Cache of clients per tenant
    
    def configure_erpnext(
        self,
        tenant_id: str,
        base_url: str,
        api_key: str,
        api_secret: str,
        site_name: Optional[str] = None
    ) -> bool:
        """Configure ERPNext connection for tenant"""
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO erpnext_config
                    (tenant_id, base_url, api_key, api_secret, site_name, configured, configured_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    tenant_id,
                    base_url,
                    api_key,
                    api_secret,
                    site_name,
                    True,
                    datetime.now().isoformat()
                ))
                
                conn.commit()
            
            # Create client and cache it
            client = ERPNextClient(base_url, api_key, api_secret)
            self.clients[tenant_id] = client
            
            logger.info(f"ERPNext configured for tenant {tenant_id}")
            return True
        except Exception as e:
            logger.error(f"Error configuring ERPNext for tenant {tenant_id}: {str(e)}")
            return False
    
    def get_erpnext_client(self, tenant_id: str) -> Optional[ERPNextClient]:
        """Get ERPNext client for tenant"""
        # Check cache first
        if tenant_id in self.clients:
            return self.clients[tenant_id]
        
        # Load from database
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM erpnext_config WHERE tenant_id = ? AND configured = TRUE
                """, (tenant_id,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                client = ERPNextClient(
                    base_url=row["base_url"],
                    api_key=row["api_key"],
                    api_secret=row["api_secret"]
                )
                
                # Cache client
                self.clients[tenant_id] = client
                
                return client
        except Exception as e:
            logger.error(f"Error getting ERPNext client for tenant {tenant_id}: {str(e)}")
            return None
    
    def test_connection(self, tenant_id: str) -> Dict[str, Any]:
        """Test ERPNext connection for tenant"""
        client = self.get_erpnext_client(tenant_id)
        if not client:
            return {
                "success": False,
                "error": "ERPNext not configured for tenant"
            }
        
        try:
            # Try a simple API call
            result = client.get("User", filters={"name": "Administrator"}, fields=["name"])
            return {
                "success": True,
                "message": "Connection successful",
                "base_url": client.base_url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_erpnext_config(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Get ERPNext configuration for tenant"""
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM erpnext_config WHERE tenant_id = ?
                """, (tenant_id,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                return {
                    "base_url": row["base_url"],
                    "site_name": row["site_name"],
                    "configured": bool(row["configured"]),
                    "configured_at": row["configured_at"]
                }
        except Exception as e:
            logger.error(f"Error getting ERPNext config: {str(e)}")
            return None


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    
    tenant_manager = TenantManager()
    tenant_isolation = TenantIsolation(tenant_manager)
    erpnext_integration = ERPNextTenantIntegration(tenant_isolation)
    
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        # Configure ERPNext
        success = erpnext_integration.configure_erpnext(
            tenant_id=tenant.tenant_id,
            base_url="http://localhost:8000",
            api_key="test_key",
            api_secret="test_secret"
        )
        print(f"ERPNext configured: {success}")
