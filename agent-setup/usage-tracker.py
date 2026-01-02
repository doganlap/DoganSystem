"""
Usage Tracker - Track tenant usage for billing
"""

import sqlite3
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from tenant_manager import TenantManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UsageMetric(Enum):
    AGENTS = "agents"
    WORKFLOWS = "workflows"
    API_CALLS = "api_calls"
    EMAILS = "emails"
    STORAGE_GB = "storage_gb"
    WORKFLOW_EXECUTIONS = "workflow_executions"
    AGENT_MESSAGES = "agent_messages"


@dataclass
class UsageRecord:
    """Usage record"""
    tenant_id: str
    metric_name: str
    usage_count: int
    period_start: datetime
    period_end: datetime


class UsageTracker:
    """Tracks usage per tenant for billing"""
    
    def __init__(self, tenant_manager: TenantManager, platform_db_path: str = "platform.db"):
        self.tenant_manager = tenant_manager
        self.platform_db_path = platform_db_path
        self._init_usage_tables()
    
    def _init_usage_tables(self):
        """Initialize usage tracking tables"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        # Usage records table (already in schema, but ensure it exists)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id VARCHAR(50) NOT NULL,
                metric_name VARCHAR(100) NOT NULL,
                usage_count INTEGER NOT NULL DEFAULT 0,
                period_start TIMESTAMP NOT NULL,
                period_end TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_usage_tenant_period 
            ON usage_records(tenant_id, period_start, period_end)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_usage_metric 
            ON usage_records(metric_name, period_start)
        """)
        
        conn.commit()
        conn.close()
    
    def record_usage(
        self,
        tenant_id: str,
        metric: UsageMetric,
        count: int = 1,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None
    ):
        """Record usage for a tenant"""
        if period_start is None:
            # Current month
            now = datetime.now()
            period_start = datetime(now.year, now.month, 1)
            period_end = (period_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        # Check if record exists for this period
        cursor.execute("""
            SELECT id, usage_count FROM usage_records
            WHERE tenant_id = ? AND metric_name = ? 
            AND period_start = ? AND period_end = ?
        """, (tenant_id, metric.value, period_start.isoformat(), period_end.isoformat()))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing record
            new_count = existing[1] + count
            cursor.execute("""
                UPDATE usage_records 
                SET usage_count = ?
                WHERE id = ?
            """, (new_count, existing[0]))
        else:
            # Create new record
            cursor.execute("""
                INSERT INTO usage_records 
                (tenant_id, metric_name, usage_count, period_start, period_end)
                VALUES (?, ?, ?, ?, ?)
            """, (
                tenant_id,
                metric.value,
                count,
                period_start.isoformat(),
                period_end.isoformat()
            ))
        
        conn.commit()
        conn.close()
        
        logger.debug(f"Recorded usage: {tenant_id} - {metric.value} = {count}")
    
    def get_usage(
        self,
        tenant_id: str,
        metric: Optional[UsageMetric] = None,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get usage for a tenant"""
        if period_start is None:
            # Current month
            now = datetime.now()
            period_start = datetime(now.year, now.month, 1)
            period_end = (period_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        conn = sqlite3.connect(self.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT metric_name, SUM(usage_count) as total_usage
            FROM usage_records
            WHERE tenant_id = ? 
            AND period_start >= ? AND period_end <= ?
        """
        params = [tenant_id, period_start.isoformat(), period_end.isoformat()]
        
        if metric:
            query += " AND metric_name = ?"
            params.append(metric.value)
        
        query += " GROUP BY metric_name"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        usage = {}
        for row in rows:
            usage[row["metric_name"]] = row["total_usage"]
        
        return {
            "tenant_id": tenant_id,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "usage": usage
        }
    
    def get_current_month_usage(self, tenant_id: str) -> Dict[str, int]:
        """Get current month usage"""
        now = datetime.now()
        period_start = datetime(now.year, now.month, 1)
        period_end = (period_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        result = self.get_usage(tenant_id, period_start=period_start, period_end=period_end)
        return result.get("usage", {})
    
    def increment_agent_usage(self, tenant_id: str, count: int = 1):
        """Increment agent usage"""
        self.record_usage(tenant_id, UsageMetric.AGENTS, count)
    
    def increment_workflow_usage(self, tenant_id: str, count: int = 1):
        """Increment workflow usage"""
        self.record_usage(tenant_id, UsageMetric.WORKFLOWS, count)
    
    def increment_api_call(self, tenant_id: str, count: int = 1):
        """Increment API call usage"""
        self.record_usage(tenant_id, UsageMetric.API_CALLS, count)
    
    def increment_email_usage(self, tenant_id: str, count: int = 1):
        """Increment email usage"""
        self.record_usage(tenant_id, UsageMetric.EMAILS, count)
    
    def set_storage_usage(self, tenant_id: str, storage_gb: float):
        """Set storage usage (replaces, doesn't increment)"""
        now = datetime.now()
        period_start = datetime(now.year, now.month, 1)
        period_end = (period_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        # Delete existing record for this period
        cursor.execute("""
            DELETE FROM usage_records
            WHERE tenant_id = ? AND metric_name = ?
            AND period_start = ? AND period_end = ?
        """, (tenant_id, UsageMetric.STORAGE_GB.value, period_start.isoformat(), period_end.isoformat()))
        
        # Insert new record
        cursor.execute("""
            INSERT INTO usage_records 
            (tenant_id, metric_name, usage_count, period_start, period_end)
            VALUES (?, ?, ?, ?, ?)
        """, (
            tenant_id,
            UsageMetric.STORAGE_GB.value,
            int(storage_gb * 100) / 100,  # Round to 2 decimals
            period_start.isoformat(),
            period_end.isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def check_quota_exceeded(self, tenant_id: str) -> Dict[str, Any]:
        """Check if tenant has exceeded any quotas"""
        quota = self.tenant_manager.get_tenant_quota(tenant_id)
        if not quota:
            return {"exceeded": False, "violations": []}
        
        current_usage = self.get_current_month_usage(tenant_id)
        violations = []
        
        # Check each quota
        if quota.get("max_agents"):
            agent_usage = current_usage.get("agents", 0)
            if agent_usage >= quota["max_agents"]:
                violations.append({
                    "metric": "agents",
                    "limit": quota["max_agents"],
                    "usage": agent_usage
                })
        
        if quota.get("max_workflows"):
            workflow_usage = current_usage.get("workflows", 0)
            if workflow_usage >= quota["max_workflows"]:
                violations.append({
                    "metric": "workflows",
                    "limit": quota["max_workflows"],
                    "usage": workflow_usage
                })
        
        if quota.get("max_api_calls"):
            api_usage = current_usage.get("api_calls", 0)
            if api_usage >= quota["max_api_calls"]:
                violations.append({
                    "metric": "api_calls",
                    "limit": quota["max_api_calls"],
                    "usage": api_usage
                })
        
        if quota.get("max_storage_gb"):
            storage_usage = current_usage.get("storage_gb", 0)
            if storage_usage >= quota["max_storage_gb"]:
                violations.append({
                    "metric": "storage_gb",
                    "limit": quota["max_storage_gb"],
                    "usage": storage_usage
                })
        
        return {
            "exceeded": len(violations) > 0,
            "violations": violations
        }


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    
    manager = TenantManager()
    tracker = UsageTracker(manager)
    
    # Create test tenant
    tenant = manager.create_tenant("Test Company", "testco")
    
    # Record usage
    tracker.increment_api_call(tenant.tenant_id, 100)
    tracker.increment_email_usage(tenant.tenant_id, 5)
    
    # Get usage
    usage = tracker.get_current_month_usage(tenant.tenant_id)
    print(f"Current usage: {usage}")
    
    # Check quota
    quota_check = tracker.check_quota_exceeded(tenant.tenant_id)
    print(f"Quota check: {quota_check}")
