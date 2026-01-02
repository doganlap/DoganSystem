"""
Tenant Provisioning - Automatic tenant setup
Creates database, initializes schema, sets up default agents and workflows
"""

import os
import sqlite3
import logging
from typing import Dict, Optional, Any
from pathlib import Path
from datetime import datetime

from tenant_manager import TenantManager, Tenant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TenantProvisioner:
    """Handles automatic provisioning of new tenants"""
    
    def __init__(self, tenant_manager: TenantManager, tenant_db_dir: str = "tenant_databases"):
        self.tenant_manager = tenant_manager
        self.tenant_db_dir = Path(tenant_db_dir)
        self.tenant_db_dir.mkdir(exist_ok=True)
    
    def provision_tenant(self, tenant: Tenant) -> Dict[str, Any]:
        """Provision a complete tenant environment"""
        logger.info(f"Provisioning tenant: {tenant.tenant_id}")
        
        result = {
            "tenant_id": tenant.tenant_id,
            "database_created": False,
            "schema_initialized": False,
            "default_agents_created": False,
            "default_workflows_created": False,
            "erpnext_configured": False,
            "errors": []
        }
        
        try:
            # 1. Create tenant database
            db_path = self._create_tenant_database(tenant)
            result["database_created"] = True
            result["database_path"] = str(db_path)
            
            # 2. Initialize database schema
            self._initialize_tenant_schema(db_path)
            result["schema_initialized"] = True
            
            # 3. Create default agents
            self._create_default_agents(tenant, db_path)
            result["default_agents_created"] = True
            
            # 4. Create default workflows
            self._create_default_workflows(tenant, db_path)
            result["default_workflows_created"] = True
            
            # 5. Setup ERPNext connection placeholder
            self._setup_erpnext_connection(tenant, db_path)
            result["erpnext_configured"] = True
            
            # 6. Setup default KSA configuration
            self._setup_tenant_config(tenant, db_path)
            result["ksa_config_created"] = True
            
            # 7. Register database in platform DB
            self._register_tenant_database(tenant, db_path)
            
            logger.info(f"Tenant {tenant.tenant_id} provisioned successfully")
            
        except Exception as e:
            logger.error(f"Error provisioning tenant {tenant.tenant_id}: {str(e)}")
            result["errors"].append(str(e))
        
        return result
    
    def _create_tenant_database(self, tenant: Tenant) -> Path:
        """Create SQLite database for tenant"""
        db_path = self.tenant_db_dir / f"{tenant.tenant_id}.db"
        
        if db_path.exists():
            logger.warning(f"Database already exists for tenant {tenant.tenant_id}")
            return db_path
        
        # Create database file
        conn = sqlite3.connect(str(db_path))
        conn.close()
        
        logger.info(f"Created database: {db_path}")
        return db_path
    
    def _initialize_tenant_schema(self, db_path: Path):
        """Initialize tenant database schema"""
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create agents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                agent_id VARCHAR(50) PRIMARY KEY,
                tenant_id VARCHAR(50) NOT NULL,
                employee_name VARCHAR(255) NOT NULL,
                role VARCHAR(100),
                department VARCHAR(100),
                team_id VARCHAR(50),
                manager_id VARCHAR(50),
                capabilities TEXT, -- JSON array as text
                status VARCHAR(20) DEFAULT 'available',
                api_key VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create agent_teams table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_teams (
                team_id VARCHAR(50) PRIMARY KEY,
                tenant_id VARCHAR(50) NOT NULL,
                team_name VARCHAR(255) NOT NULL,
                department VARCHAR(100),
                manager_id VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create workflows table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflows (
                workflow_id VARCHAR(50) PRIMARY KEY,
                tenant_id VARCHAR(50) NOT NULL,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                trigger_type VARCHAR(50),
                trigger_config TEXT, -- JSON as text
                steps TEXT, -- JSON array as text
                enabled BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create workflow_executions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflow_executions (
                execution_id VARCHAR(50) PRIMARY KEY,
                tenant_id VARCHAR(50) NOT NULL,
                workflow_id VARCHAR(50) NOT NULL,
                status VARCHAR(20),
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                result TEXT, -- JSON as text
                error TEXT
            )
        """)
        
        # Create erpnext_config table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS erpnext_config (
                tenant_id VARCHAR(50) PRIMARY KEY,
                base_url VARCHAR(255),
                api_key VARCHAR(255),
                api_secret VARCHAR(255),
                site_name VARCHAR(255),
                configured BOOLEAN DEFAULT FALSE,
                configured_at TIMESTAMP
            )
        """)
        
        # Create tenant_config table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tenant_config (
                tenant_id VARCHAR(50) PRIMARY KEY,
                locale VARCHAR(10) DEFAULT 'ar_SA',
                timezone VARCHAR(50) DEFAULT 'Asia/Riyadh',
                currency VARCHAR(3) DEFAULT 'SAR',
                work_week_start VARCHAR(10) DEFAULT 'Saturday',
                work_week_end VARCHAR(10) DEFAULT 'Wednesday',
                language VARCHAR(10) DEFAULT 'ar',
                enable_hijri_calendar BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agents_tenant ON agents(tenant_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_workflows_tenant ON workflows(tenant_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_executions_tenant ON workflow_executions(tenant_id)")
        
        conn.commit()
        conn.close()
        
        logger.info(f"Schema initialized for tenant database: {db_path}")
    
    def _create_default_agents(self, tenant: Tenant, db_path: Path):
        """Create default employee-style agents for tenant"""
        import uuid
        import json
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Default agents based on subscription tier
        default_agents = []
        
        if tenant.subscription_tier == "starter":
            default_agents = [
                {
                    "employee_name": "Sales Agent",
                    "role": "Sales Specialist",
                    "department": "Sales",
                    "capabilities": ["customer_management", "quotation", "sales_order"]
                },
                {
                    "employee_name": "Support Agent",
                    "role": "Customer Support",
                    "department": "Support",
                    "capabilities": ["support", "troubleshooting", "customer_service"]
                }
            ]
        elif tenant.subscription_tier == "professional":
            default_agents = [
                {
                    "employee_name": "Sales Manager",
                    "role": "Sales Manager",
                    "department": "Sales",
                    "capabilities": ["customer_management", "quotation", "sales_order", "team_management"]
                },
                {
                    "employee_name": "Sales Agent 1",
                    "role": "Sales Specialist",
                    "department": "Sales",
                    "capabilities": ["customer_management", "quotation", "sales_order"]
                },
                {
                    "employee_name": "Support Manager",
                    "role": "Support Manager",
                    "department": "Support",
                    "capabilities": ["support", "troubleshooting", "team_management"]
                },
                {
                    "employee_name": "Support Agent 1",
                    "role": "Customer Support",
                    "department": "Support",
                    "capabilities": ["support", "troubleshooting"]
                }
            ]
        else:  # enterprise
            default_agents = [
                {
                    "employee_name": "Sales Director",
                    "role": "Sales Director",
                    "department": "Sales",
                    "capabilities": ["customer_management", "quotation", "sales_order", "team_management", "strategy"]
                },
                {
                    "employee_name": "Sales Manager",
                    "role": "Sales Manager",
                    "department": "Sales",
                    "capabilities": ["customer_management", "quotation", "sales_order", "team_management"]
                },
                {
                    "employee_name": "Sales Agent 1",
                    "role": "Sales Specialist",
                    "department": "Sales",
                    "capabilities": ["customer_management", "quotation", "sales_order"]
                },
                {
                    "employee_name": "Support Manager",
                    "role": "Support Manager",
                    "department": "Support",
                    "capabilities": ["support", "troubleshooting", "team_management"]
                },
                {
                    "employee_name": "Support Agent 1",
                    "role": "Customer Support",
                    "department": "Support",
                    "capabilities": ["support", "troubleshooting"]
                }
            ]
        
        for agent_data in default_agents:
            agent_id = f"agent_{uuid.uuid4().hex[:12]}"
            cursor.execute("""
                INSERT INTO agents (agent_id, tenant_id, employee_name, role, department, capabilities, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                agent_id,
                tenant.tenant_id,
                agent_data["employee_name"],
                agent_data["role"],
                agent_data["department"],
                json.dumps(agent_data["capabilities"]),
                "available"
            ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Created {len(default_agents)} default agents for tenant {tenant.tenant_id}")
    
    def _create_default_workflows(self, tenant: Tenant, db_path: Path):
        """Create default workflows for tenant"""
        import uuid
        import json
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        default_workflows = [
            {
                "name": "Auto-Process Incoming Emails",
                "description": "Automatically process incoming emails and create leads",
                "trigger_type": "scheduled",
                "trigger_config": {"schedule": {"type": "interval", "interval": 15}},
                "steps": [
                    {
                        "step_id": "read_emails",
                        "name": "Read Incoming Emails",
                        "action_type": "process_incoming_emails"
                    },
                    {
                        "step_id": "create_leads",
                        "name": "Create Leads from Emails",
                        "action_type": "create_lead_from_email",
                        "depends_on": ["read_emails"]
                    }
                ],
                "enabled": True
            },
            {
                "name": "Auto-Send Quotations",
                "description": "Automatically send quotations to customers",
                "trigger_type": "event",
                "trigger_config": {"event": "quotation_created"},
                "steps": [
                    {
                        "step_id": "get_quotation",
                        "name": "Get Quotation Details",
                        "action_type": "erpnext_get",
                        "action_config": {"resource_type": "Quotation"}
                    },
                    {
                        "step_id": "send_email",
                        "name": "Send Quotation Email",
                        "action_type": "send_email",
                        "depends_on": ["get_quotation"]
                    }
                ],
                "enabled": True
            }
        ]
        
        for workflow_data in default_workflows:
            workflow_id = f"workflow_{uuid.uuid4().hex[:12]}"
            cursor.execute("""
                INSERT INTO workflows (workflow_id, tenant_id, name, description, trigger_type, trigger_config, steps, enabled)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                workflow_id,
                tenant.tenant_id,
                workflow_data["name"],
                workflow_data["description"],
                workflow_data["trigger_type"],
                json.dumps(workflow_data["trigger_config"]),
                json.dumps(workflow_data["steps"]),
                workflow_data["enabled"]
            ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Created {len(default_workflows)} default workflows for tenant {tenant.tenant_id}")
    
    def _setup_erpnext_connection(self, tenant: Tenant, db_path: Path):
        """Setup ERPNext connection placeholder"""
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO erpnext_config (tenant_id, configured)
            VALUES (?, ?)
        """, (tenant.tenant_id, False))
        
        conn.commit()
        conn.close()
        
        logger.info(f"ERPNext connection placeholder created for tenant {tenant.tenant_id}")
    
    def _setup_tenant_config(self, tenant: Tenant, db_path: Path):
        """Setup default tenant configuration (KSA settings)"""
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO tenant_config 
            (tenant_id, locale, timezone, currency, work_week_start, work_week_end, language, enable_hijri_calendar)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tenant.tenant_id,
            "ar_SA",
            "Asia/Riyadh",
            "SAR",
            "Saturday",
            "Wednesday",
            "ar",
            True
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Default KSA configuration set for tenant {tenant.tenant_id}")
    
    def _register_tenant_database(self, tenant: Tenant, db_path: Path):
        """Register tenant database in platform database"""
        import sqlite3
        
        platform_db = sqlite3.connect(self.tenant_manager.platform_db_path)
        cursor = platform_db.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO tenant_databases (tenant_id, database_name, database_type, connection_string)
            VALUES (?, ?, ?, ?)
        """, (
            tenant.tenant_id,
            db_path.name,
            "sqlite",
            str(db_path)
        ))
        
        platform_db.commit()
        platform_db.close()
        
        logger.info(f"Registered database for tenant {tenant.tenant_id}")


# Example usage
if __name__ == "__main__":
    manager = TenantManager()
    provisioner = TenantProvisioner(manager)
    
    # Create and provision a tenant
    tenant = manager.create_tenant(
        name="Test Company",
        subdomain="testco",
        subscription_tier="professional"
    )
    
    result = provisioner.provision_tenant(tenant)
    print(f"Provisioning result: {result}")
