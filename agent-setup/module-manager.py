"""
Module Manager - Install, configure, and manage modules per tenant
"""

import sqlite3
import logging
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

from tenant_isolation import TenantIsolation
from module_marketplace import ModuleMarketplace

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModuleManager:
    """Manages module installation and configuration per tenant"""
    
    def __init__(
        self,
        tenant_isolation: TenantIsolation,
        module_marketplace: ModuleMarketplace
    ):
        self.tenant_isolation = tenant_isolation
        self.marketplace = module_marketplace
    
    def install_module(
        self,
        tenant_id: str,
        module_id: str,
        configuration: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Install a module for a tenant"""
        # Check if module exists
        module = self.marketplace.get_module(module_id)
        if not module:
            return {
                "success": False,
                "error": f"Module {module_id} not found"
            }
        
        # Check if tenant has purchased module
        if not self.marketplace.tenant_has_module(tenant_id, module_id):
            return {
                "success": False,
                "error": f"Module {module_id} not purchased for tenant"
            }
        
        # Check dependencies
        for dep in module.dependencies:
            if not self.marketplace.tenant_has_module(tenant_id, dep):
                return {
                    "success": False,
                    "error": f"Module {module_id} requires {dep} to be installed first"
                }
        
        # Install module in tenant database
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                cursor = conn.cursor()
                
                # Create module configuration table if not exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS module_config (
                        module_id VARCHAR(50) NOT NULL,
                        tenant_id VARCHAR(50) NOT NULL,
                        config_key VARCHAR(100) NOT NULL,
                        config_value TEXT,
                        PRIMARY KEY (module_id, tenant_id, config_key)
                    )
                """)
                
                # Save configuration
                if configuration:
                    for key, value in configuration.items():
                        cursor.execute("""
                            INSERT OR REPLACE INTO module_config
                            (module_id, tenant_id, config_key, config_value)
                            VALUES (?, ?, ?, ?)
                        """, (module_id, tenant_id, key, json.dumps(value) if isinstance(value, dict) else str(value)))
                
                # Create module-specific tables based on module type
                self._create_module_tables(cursor, module_id, tenant_id)
                
                conn.commit()
            
            logger.info(f"Module {module_id} installed for tenant {tenant_id}")
            
            return {
                "success": True,
                "tenant_id": tenant_id,
                "module_id": module_id,
                "message": f"Module {module_id} installed successfully"
            }
        except Exception as e:
            logger.error(f"Error installing module {module_id} for tenant {tenant_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_module_tables(self, cursor: sqlite3.Cursor, module_id: str, tenant_id: str):
        """Create module-specific tables"""
        # Sales Agent Module tables
        if module_id == "sales_agent":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales_agent_config (
                    tenant_id VARCHAR(50) PRIMARY KEY,
                    auto_quotation BOOLEAN DEFAULT TRUE,
                    auto_followup BOOLEAN DEFAULT TRUE,
                    quotation_template TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        # Support Agent Module tables
        elif module_id == "support_agent":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS support_agent_config (
                    tenant_id VARCHAR(50) PRIMARY KEY,
                    auto_ticket_assignment BOOLEAN DEFAULT TRUE,
                    response_timeout INTEGER DEFAULT 3600,
                    escalation_rules TEXT, -- JSON
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        # Inventory Agent Module tables
        elif module_id == "inventory_agent":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory_agent_config (
                    tenant_id VARCHAR(50) PRIMARY KEY,
                    low_stock_threshold INTEGER DEFAULT 10,
                    auto_reorder BOOLEAN DEFAULT FALSE,
                    warehouse_monitoring BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        # Add more module-specific tables as needed
    
    def get_module_config(
        self,
        tenant_id: str,
        module_id: str
    ) -> Dict[str, Any]:
        """Get module configuration for tenant"""
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT config_key, config_value FROM module_config
                    WHERE module_id = ? AND tenant_id = ?
                """, (module_id, tenant_id))
                
                rows = cursor.fetchall()
                config = {}
                for row in rows:
                    try:
                        config[row["config_key"]] = json.loads(row["config_value"])
                    except:
                        config[row["config_key"]] = row["config_value"]
                
                return config
        except Exception as e:
            logger.error(f"Error getting module config: {str(e)}")
            return {}
    
    def update_module_config(
        self,
        tenant_id: str,
        module_id: str,
        configuration: Dict[str, Any]
    ) -> bool:
        """Update module configuration"""
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                cursor = conn.cursor()
                
                for key, value in configuration.items():
                    cursor.execute("""
                        INSERT OR REPLACE INTO module_config
                        (module_id, tenant_id, config_key, config_value)
                        VALUES (?, ?, ?, ?)
                    """, (
                        module_id,
                        tenant_id,
                        key,
                        json.dumps(value) if isinstance(value, dict) else str(value)
                    ))
                
                conn.commit()
            
            logger.info(f"Module {module_id} configuration updated for tenant {tenant_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating module config: {str(e)}")
            return False
    
    def uninstall_module(self, tenant_id: str, module_id: str) -> Dict[str, Any]:
        """Uninstall module from tenant"""
        # Check if module is installed
        if not self.marketplace.tenant_has_module(tenant_id, module_id):
            return {
                "success": False,
                "error": f"Module {module_id} not installed for tenant"
            }
        
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                cursor = conn.cursor()
                
                # Remove module configuration
                cursor.execute("""
                    DELETE FROM module_config
                    WHERE module_id = ? AND tenant_id = ?
                """, (module_id, tenant_id))
                
                # Drop module-specific tables (optional - might want to keep data)
                # self._drop_module_tables(cursor, module_id)
                
                conn.commit()
            
            # Remove from tenant_modules
            self.marketplace.uninstall_module(tenant_id, module_id)
            
            logger.info(f"Module {module_id} uninstalled from tenant {tenant_id}")
            
            return {
                "success": True,
                "tenant_id": tenant_id,
                "module_id": module_id,
                "message": f"Module {module_id} uninstalled successfully"
            }
        except Exception as e:
            logger.error(f"Error uninstalling module {module_id} for tenant {tenant_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_module_compatibility(
        self,
        tenant_id: str,
        module_id: str
    ) -> Dict[str, Any]:
        """Check if module is compatible with tenant's current setup"""
        module = self.marketplace.get_module(module_id)
        if not module:
            return {
                "compatible": False,
                "error": "Module not found"
            }
        
        issues = []
        
        # Check dependencies
        for dep in module.dependencies:
            if not self.marketplace.tenant_has_module(tenant_id, dep):
                issues.append(f"Missing dependency: {dep}")
        
        # Check tenant subscription tier (some modules might require specific tiers)
        tenant = self.tenant_isolation.tenant_manager.get_tenant(tenant_id)
        if tenant:
            # Enterprise modules might require enterprise tier
            if module_id == "advanced_analytics" and tenant.subscription_tier != "enterprise":
                issues.append("Module requires Enterprise subscription")
        
        return {
            "compatible": len(issues) == 0,
            "issues": issues,
            "module_id": module_id
        }


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    
    tenant_manager = TenantManager()
    tenant_isolation = TenantIsolation(tenant_manager)
    marketplace = ModuleMarketplace(tenant_manager)
    module_manager = ModuleManager(tenant_isolation, marketplace)
    
    # Install module
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        result = module_manager.install_module(
            tenant.tenant_id,
            "sales_agent",
            {"auto_quotation": True, "auto_followup": True}
        )
        print(f"Install result: {result}")
