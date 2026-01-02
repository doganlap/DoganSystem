"""
Tenant Manager - Multi-Tenant SaaS Platform
Manages tenant lifecycle, configuration, and resources
"""

import os
import logging
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TenantStatus(Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


@dataclass
class Tenant:
    """Represents a tenant in the SaaS platform"""
    tenant_id: str
    name: str
    domain: Optional[str] = None
    subdomain: Optional[str] = None
    status: str = TenantStatus.TRIAL.value
    subscription_tier: str = "starter"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    trial_end_date: Optional[datetime] = None
    metadata: Optional[Dict] = None


class TenantManager:
    """Manages tenants in the multi-tenant SaaS platform"""
    
    def __init__(self, platform_db_path: str = "platform.db"):
        self.platform_db_path = platform_db_path
        self._init_platform_database()
    
    def _init_platform_database(self):
        """Initialize platform database with schema"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        # Read and execute schema
        schema_path = Path(__file__).parent / "tenant-schema.sql"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema = f.read()
                # SQLite doesn't support all PostgreSQL features, adapt as needed
                # Execute statements one by one
                for statement in schema.split(';'):
                    statement = statement.strip()
                    if statement and not statement.startswith('--'):
                        try:
                            # Adapt PostgreSQL syntax to SQLite
                            statement = statement.replace('SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
                            statement = statement.replace('JSONB', 'TEXT')  # Store JSON as TEXT in SQLite
                            statement = statement.replace('TIMESTAMP DEFAULT CURRENT_TIMESTAMP', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
                            # Remove unsupported features
                            if 'INDEX' in statement and 'CREATE' not in statement.upper():
                                continue  # Skip standalone index creation
                            cursor.execute(statement)
                        except sqlite3.OperationalError as e:
                            if "already exists" not in str(e).lower():
                                logger.warning(f"Schema execution warning: {e}")
        
        conn.commit()
        conn.close()
        logger.info("Platform database initialized")
    
    def create_tenant(
        self,
        name: str,
        subdomain: Optional[str] = None,
        domain: Optional[str] = None,
        subscription_tier: str = "starter",
        trial_days: int = 14
    ) -> Tenant:
        """Create a new tenant"""
        tenant_id = f"tenant_{uuid.uuid4().hex[:12]}"
        
        # Generate subdomain if not provided
        if not subdomain:
            subdomain = name.lower().replace(' ', '-').replace('_', '-')[:50]
            # Ensure uniqueness
            existing = self.get_tenant_by_subdomain(subdomain)
            if existing:
                subdomain = f"{subdomain}-{uuid.uuid4().hex[:6]}"
        
        trial_end = datetime.now() + timedelta(days=trial_days)
        
        tenant = Tenant(
            tenant_id=tenant_id,
            name=name,
            subdomain=subdomain,
            domain=domain,
            status=TenantStatus.TRIAL.value,
            subscription_tier=subscription_tier,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            trial_end_date=trial_end,
            metadata={}
        )
        
        # Save to database
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tenants (tenant_id, name, domain, subdomain, status, subscription_tier, 
                                created_at, updated_at, trial_end_date, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tenant.tenant_id,
            tenant.name,
            tenant.domain,
            tenant.subdomain,
            tenant.status,
            tenant.subscription_tier,
            tenant.created_at.isoformat() if tenant.created_at else None,
            tenant.updated_at.isoformat() if tenant.updated_at else None,
            tenant.trial_end_date.isoformat() if tenant.trial_end_date else None,
            str(tenant.metadata) if tenant.metadata else None
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Tenant created: {tenant_id} ({name})")
        return tenant
    
    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """Get tenant by ID"""
        conn = sqlite3.connect(self.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM tenants WHERE tenant_id = ?
        """, (tenant_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_tenant(row)
    
    def get_tenant_by_subdomain(self, subdomain: str) -> Optional[Tenant]:
        """Get tenant by subdomain"""
        conn = sqlite3.connect(self.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM tenants WHERE subdomain = ?
        """, (subdomain,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_tenant(row)
    
    def get_tenant_by_domain(self, domain: str) -> Optional[Tenant]:
        """Get tenant by domain"""
        conn = sqlite3.connect(self.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM tenants WHERE domain = ?
        """, (domain,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_tenant(row)
    
    def list_tenants(
        self,
        status: Optional[str] = None,
        subscription_tier: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Tenant]:
        """List tenants with filters"""
        conn = sqlite3.connect(self.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM tenants WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if subscription_tier:
            query += " AND subscription_tier = ?"
            params.append(subscription_tier)
        
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_tenant(row) for row in rows]
    
    def update_tenant(
        self,
        tenant_id: str,
        name: Optional[str] = None,
        status: Optional[str] = None,
        subscription_tier: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Update tenant information"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if name:
            updates.append("name = ?")
            params.append(name)
        
        if status:
            updates.append("status = ?")
            params.append(status)
        
        if subscription_tier:
            updates.append("subscription_tier = ?")
            params.append(subscription_tier)
        
        if metadata:
            updates.append("metadata = ?")
            params.append(str(metadata))
        
        if not updates:
            conn.close()
            return False
        
        updates.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        params.append(tenant_id)
        
        query = f"UPDATE tenants SET {', '.join(updates)} WHERE tenant_id = ?"
        cursor.execute(query, params)
        
        conn.commit()
        conn.close()
        
        logger.info(f"Tenant updated: {tenant_id}")
        return True
    
    def suspend_tenant(self, tenant_id: str) -> bool:
        """Suspend a tenant"""
        return self.update_tenant(tenant_id, status=TenantStatus.SUSPENDED.value)
    
    def activate_tenant(self, tenant_id: str) -> bool:
        """Activate a tenant"""
        return self.update_tenant(tenant_id, status=TenantStatus.ACTIVE.value)
    
    def cancel_tenant(self, tenant_id: str) -> bool:
        """Cancel a tenant"""
        return self.update_tenant(tenant_id, status=TenantStatus.CANCELLED.value)
    
    def delete_tenant(self, tenant_id: str) -> bool:
        """Delete a tenant (cascade deletes related data)"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tenants WHERE tenant_id = ?", (tenant_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Tenant deleted: {tenant_id}")
        return True
    
    def get_tenant_quota(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant resource quotas based on subscription tier"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return {}
        
        # Get subscription plan details
        conn = sqlite3.connect(self.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM subscription_plans WHERE tier = ?
        """, (tenant.subscription_tier,))
        
        plan = cursor.fetchone()
        conn.close()
        
        if not plan:
            # Default quotas
            return {
                "max_agents": 5,
                "max_workflows": 10,
                "max_api_calls": 10000,
                "max_storage_gb": 10
            }
        
        return {
            "max_agents": plan["max_agents"],
            "max_workflows": plan["max_workflows"],
            "max_api_calls": plan["max_api_calls"],
            "max_storage_gb": plan["max_storage_gb"],
            "included_modules": plan["included_modules"] if plan["included_modules"] else []
        }
    
    def check_trial_expiry(self) -> List[str]:
        """Check for expired trials and return tenant IDs"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT tenant_id FROM tenants 
            WHERE status = 'trial' 
            AND trial_end_date < datetime('now')
        """)
        
        expired = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Update expired tenants
        for tenant_id in expired:
            self.update_tenant(tenant_id, status=TenantStatus.EXPIRED.value)
        
        return expired
    
    def _row_to_tenant(self, row: sqlite3.Row) -> Tenant:
        """Convert database row to Tenant object"""
        import json
        
        metadata = None
        if row["metadata"]:
            try:
                metadata = json.loads(row["metadata"])
            except:
                metadata = {}
        
        return Tenant(
            tenant_id=row["tenant_id"],
            name=row["name"],
            domain=row["domain"],
            subdomain=row["subdomain"],
            status=row["status"],
            subscription_tier=row["subscription_tier"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
            updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None,
            trial_end_date=datetime.fromisoformat(row["trial_end_date"]) if row["trial_end_date"] else None,
            metadata=metadata
        )


# Example usage
if __name__ == "__main__":
    manager = TenantManager()
    
    # Create a tenant
    tenant = manager.create_tenant(
        name="Acme Corporation",
        subdomain="acme",
        subscription_tier="professional"
    )
    
    print(f"Created tenant: {tenant.tenant_id}")
    print(f"Subdomain: {tenant.subdomain}")
    print(f"Trial ends: {tenant.trial_end_date}")
    
    # Get tenant
    retrieved = manager.get_tenant(tenant.tenant_id)
    print(f"Retrieved tenant: {retrieved.name}")
    
    # Get quota
    quota = manager.get_tenant_quota(tenant.tenant_id)
    print(f"Quota: {quota}")
