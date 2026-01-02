"""
Module Marketplace - ERPNext modules sold as services
"""

import sqlite3
import logging
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import json

from tenant_manager import TenantManager
from tenant_isolation import TenantIsolation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModuleCategory(Enum):
    SALES = "sales"
    SUPPORT = "support"
    INVENTORY = "inventory"
    ACCOUNTING = "accounting"
    AUTOMATION = "automation"
    ANALYTICS = "analytics"
    INTEGRATION = "integration"


@dataclass
class Module:
    """ERPNext module definition"""
    module_id: str
    name: str
    display_name: str
    description: str
    category: ModuleCategory
    price_monthly: float
    price_yearly: Optional[float] = None
    features: List[str] = None
    dependencies: List[str] = None
    version: str = "1.0.0"
    enabled: bool = True
    
    def __post_init__(self):
        if self.features is None:
            self.features = []
        if self.dependencies is None:
            self.dependencies = []


class ModuleMarketplace:
    """Manages ERPNext module marketplace"""
    
    def __init__(self, tenant_manager: TenantManager, platform_db_path: str = "platform.db"):
        self.tenant_manager = tenant_manager
        self.platform_db_path = platform_db_path
        self.modules: Dict[str, Module] = {}
        self._init_marketplace_tables()
        self._initialize_default_modules()
    
    def _init_marketplace_tables(self):
        """Initialize marketplace tables"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        # Modules catalog table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS modules_catalog (
                module_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                display_name VARCHAR(255) NOT NULL,
                description TEXT,
                category VARCHAR(50),
                price_monthly DECIMAL(10, 2) NOT NULL,
                price_yearly DECIMAL(10, 2),
                features TEXT, -- JSON array
                dependencies TEXT, -- JSON array
                version VARCHAR(20),
                enabled BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tenant modules table (already exists in tenant-schema.sql, but ensure it exists)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tenant_modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id VARCHAR(50) NOT NULL,
                module_name VARCHAR(100) NOT NULL,
                enabled BOOLEAN DEFAULT TRUE,
                purchased_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expiry_date TIMESTAMP,
                configuration TEXT, -- JSON
                UNIQUE(tenant_id, module_name)
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tenant_modules ON tenant_modules(tenant_id, enabled)")
        
        conn.commit()
        conn.close()
    
    def _initialize_default_modules(self):
        """Initialize default modules in marketplace"""
        
        # Sales Agent Module
        sales_module = Module(
            module_id="sales_agent",
            name="sales_agent",
            display_name="Sales Agent Module",
            description="AI-powered sales agents for customer management, quotations, and sales orders",
            category=ModuleCategory.SALES,
            price_monthly=49.00,
            price_yearly=490.00,
            features=[
                "Customer management",
                "Quotation automation",
                "Sales order processing",
                "Customer communication",
                "Sales analytics"
            ],
            dependencies=[]
        )
        self.modules["sales_agent"] = sales_module
        self._save_module_to_db(sales_module)
        
        # Support Agent Module
        support_module = Module(
            module_id="support_agent",
            name="support_agent",
            display_name="Support Agent Module",
            description="AI customer support agents for ticket management and troubleshooting",
            category=ModuleCategory.SUPPORT,
            price_monthly=49.00,
            price_yearly=490.00,
            features=[
                "Ticket management",
                "Customer support automation",
                "Knowledge base integration",
                "Support analytics"
            ],
            dependencies=[]
        )
        self.modules["support_agent"] = support_module
        self._save_module_to_db(support_module)
        
        # Inventory Agent Module
        inventory_module = Module(
            module_id="inventory_agent",
            name="inventory_agent",
            display_name="Inventory Agent Module",
            description="AI inventory management agents for stock control and warehouse operations",
            category=ModuleCategory.INVENTORY,
            price_monthly=59.00,
            price_yearly=590.00,
            features=[
                "Stock level monitoring",
                "Warehouse management",
                "Inventory optimization",
                "Stock alerts"
            ],
            dependencies=[]
        )
        self.modules["inventory_agent"] = inventory_module
        self._save_module_to_db(inventory_module)
        
        # Accounting Agent Module
        accounting_module = Module(
            module_id="accounting_agent",
            name="accounting_agent",
            display_name="Accounting Agent Module",
            description="AI accounting agents for financial management and reporting",
            category=ModuleCategory.ACCOUNTING,
            price_monthly=69.00,
            price_yearly=690.00,
            features=[
                "Invoice processing",
                "Payment tracking",
                "Financial reporting",
                "Compliance management"
            ],
            dependencies=[]
        )
        self.modules["accounting_agent"] = accounting_module
        self._save_module_to_db(accounting_module)
        
        # Email Automation Module
        email_module = Module(
            module_id="email_automation",
            name="email_automation",
            display_name="Email Automation Module",
            description="Automated email processing, sending, and lead generation",
            category=ModuleCategory.AUTOMATION,
            price_monthly=29.00,
            price_yearly=290.00,
            features=[
                "Email processing",
                "Auto-responders",
                "Lead generation",
                "Email templates"
            ],
            dependencies=[]
        )
        self.modules["email_automation"] = email_module
        self._save_module_to_db(email_module)
        
        # Workflow Automation Module
        workflow_module = Module(
            module_id="workflow_automation",
            name="workflow_automation",
            display_name="Workflow Automation Module",
            description="Advanced workflow automation and business process management",
            category=ModuleCategory.AUTOMATION,
            price_monthly=79.00,
            price_yearly=790.00,
            features=[
                "Custom workflows",
                "Process automation",
                "Workflow templates",
                "Advanced scheduling"
            ],
            dependencies=[]
        )
        self.modules["workflow_automation"] = workflow_module
        self._save_module_to_db(workflow_module)
        
        # Advanced Analytics Module
        analytics_module = Module(
            module_id="advanced_analytics",
            name="advanced_analytics",
            display_name="Advanced Analytics Module",
            description="Advanced business analytics and reporting with AI insights",
            category=ModuleCategory.ANALYTICS,
            price_monthly=99.00,
            price_yearly=990.00,
            features=[
                "Business intelligence",
                "Predictive analytics",
                "Custom reports",
                "Data visualization"
            ],
            dependencies=[]
        )
        self.modules["advanced_analytics"] = analytics_module
        self._save_module_to_db(analytics_module)
    
    def _save_module_to_db(self, module: Module):
        """Save module to database"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO modules_catalog
            (module_id, name, display_name, description, category, price_monthly, price_yearly,
             features, dependencies, version, enabled)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            module.module_id,
            module.name,
            module.display_name,
            module.description,
            module.category.value,
            module.price_monthly,
            module.price_yearly,
            json.dumps(module.features),
            json.dumps(module.dependencies),
            module.version,
            module.enabled
        ))
        
        conn.commit()
        conn.close()
    
    def list_modules(
        self,
        category: Optional[ModuleCategory] = None,
        enabled_only: bool = True
    ) -> List[Module]:
        """List available modules"""
        modules = list(self.modules.values())
        
        if category:
            modules = [m for m in modules if m.category == category]
        
        if enabled_only:
            modules = [m for m in modules if m.enabled]
        
        return modules
    
    def get_module(self, module_id: str) -> Optional[Module]:
        """Get module by ID"""
        return self.modules.get(module_id)
    
    def purchase_module(
        self,
        tenant_id: str,
        module_id: str,
        billing_cycle: str = "monthly"
    ) -> Dict[str, Any]:
        """Purchase a module for a tenant"""
        module = self.get_module(module_id)
        if not module:
            raise ValueError(f"Module {module_id} not found")
        
        # Check if tenant already has module
        if self.tenant_has_module(tenant_id, module_id):
            return {
                "success": False,
                "error": f"Tenant already has module {module_id}"
            }
        
        # Check dependencies
        for dep in module.dependencies:
            if not self.tenant_has_module(tenant_id, dep):
                return {
                    "success": False,
                    "error": f"Module {module_id} requires {dep} to be installed first"
                }
        
        # Save tenant module
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tenant_modules
            (tenant_id, module_name, enabled, purchased_date, configuration)
            VALUES (?, ?, ?, ?, ?)
        """, (
            tenant_id,
            module_id,
            True,
            datetime.now().isoformat(),
            json.dumps({})
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Module {module_id} purchased for tenant {tenant_id}")
        
        return {
            "success": True,
            "tenant_id": tenant_id,
            "module_id": module_id,
            "module_name": module.display_name,
            "purchased_date": datetime.now().isoformat()
        }
    
    def tenant_has_module(self, tenant_id: str, module_id: str) -> bool:
        """Check if tenant has a module"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM tenant_modules
            WHERE tenant_id = ? AND module_name = ? AND enabled = TRUE
        """, (tenant_id, module_id))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def get_tenant_modules(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all modules for a tenant"""
        conn = sqlite3.connect(self.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT tm.*, mc.display_name, mc.description, mc.category
            FROM tenant_modules tm
            LEFT JOIN modules_catalog mc ON tm.module_name = mc.module_id
            WHERE tm.tenant_id = ? AND tm.enabled = TRUE
        """, (tenant_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def enable_module(self, tenant_id: str, module_id: str) -> bool:
        """Enable a module for tenant"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tenant_modules
            SET enabled = TRUE
            WHERE tenant_id = ? AND module_name = ?
        """, (tenant_id, module_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            logger.info(f"Module {module_id} enabled for tenant {tenant_id}")
        
        return success
    
    def disable_module(self, tenant_id: str, module_id: str) -> bool:
        """Disable a module for tenant"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tenant_modules
            SET enabled = FALSE
            WHERE tenant_id = ? AND module_name = ?
        """, (tenant_id, module_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            logger.info(f"Module {module_id} disabled for tenant {tenant_id}")
        
        return success
    
    def uninstall_module(self, tenant_id: str, module_id: str) -> bool:
        """Uninstall module from tenant"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM tenant_modules
            WHERE tenant_id = ? AND module_name = ?
        """, (tenant_id, module_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            logger.info(f"Module {module_id} uninstalled from tenant {tenant_id}")
        
        return success


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    
    manager = TenantManager()
    marketplace = ModuleMarketplace(manager)
    
    # List modules
    modules = marketplace.list_modules()
    print("Available modules:")
    for module in modules:
        print(f"  - {module.display_name}: ${module.price_monthly}/month")
    
    # Purchase module
    tenant = manager.get_tenant_by_subdomain("testco")
    if tenant:
        result = marketplace.purchase_module(tenant.tenant_id, "sales_agent")
        print(f"Purchase result: {result}")
        
        # Get tenant modules
        tenant_modules = marketplace.get_tenant_modules(tenant.tenant_id)
        print(f"Tenant modules: {[m['module_name'] for m in tenant_modules]}")
