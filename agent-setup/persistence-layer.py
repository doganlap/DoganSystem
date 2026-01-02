"""
Persistence Layer - Multi-tenant database persistence
"""

import sqlite3
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from tenant_isolation import TenantIsolation
from tenant_manager import TenantManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PersistenceLayer:
    """Multi-tenant persistence layer"""
    
    def __init__(self, tenant_isolation: TenantIsolation):
        self.tenant_isolation = tenant_isolation
    
    def save_workflow_state(
        self,
        tenant_id: str,
        workflow_id: str,
        execution_id: str,
        state: Dict[str, Any]
    ) -> bool:
        """Save workflow execution state"""
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO workflow_executions
                    (execution_id, tenant_id, workflow_id, status, started_at, result)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    execution_id,
                    tenant_id,
                    workflow_id,
                    state.get("status", "running"),
                    state.get("started_at", datetime.now().isoformat()),
                    json.dumps(state)
                ))
                
                conn.commit()
            
            return True
        except Exception as e:
            logger.error(f"Error saving workflow state: {str(e)}")
            return False
    
    def get_workflow_state(
        self,
        tenant_id: str,
        execution_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get workflow execution state"""
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM workflow_executions
                    WHERE execution_id = ? AND tenant_id = ?
                """, (execution_id, tenant_id))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                result = {}
                if row["result"]:
                    try:
                        result = json.loads(row["result"])
                    except:
                        result = {}
                
                return {
                    "execution_id": row["execution_id"],
                    "workflow_id": row["workflow_id"],
                    "status": row["status"],
                    "started_at": row["started_at"],
                    "completed_at": row["completed_at"],
                    "error": row["error"],
                    "state": result
                }
        except Exception as e:
            logger.error(f"Error getting workflow state: {str(e)}")
            return None
    
    def save_agent_state(
        self,
        tenant_id: str,
        agent_id: str,
        state: Dict[str, Any]
    ) -> bool:
        """Save agent state"""
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                cursor = conn.cursor()
                
                # Update agent status and last_activity
                cursor.execute("""
                    UPDATE agents
                    SET status = ?, updated_at = ?
                    WHERE agent_id = ? AND tenant_id = ?
                """, (
                    state.get("status", "available"),
                    datetime.now().isoformat(),
                    agent_id,
                    tenant_id
                ))
                
                conn.commit()
            
            return True
        except Exception as e:
            logger.error(f"Error saving agent state: {str(e)}")
            return False
    
    def load_workflows(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Load all workflows for tenant"""
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM workflows WHERE tenant_id = ?
                """, (tenant_id,))
                
                rows = cursor.fetchall()
                workflows = []
                
                for row in rows:
                    try:
                        trigger_config = json.loads(row["trigger_config"]) if row["trigger_config"] else {}
                        steps = json.loads(row["steps"]) if row["steps"] else []
                    except:
                        trigger_config = {}
                        steps = []
                    
                    workflows.append({
                        "workflow_id": row["workflow_id"],
                        "name": row["name"],
                        "description": row["description"],
                        "trigger_type": row["trigger_type"],
                        "trigger_config": trigger_config,
                        "steps": steps,
                        "enabled": bool(row["enabled"])
                    })
                
                return workflows
        except Exception as e:
            logger.error(f"Error loading workflows: {str(e)}")
            return []
    
    def save_workflow(
        self,
        tenant_id: str,
        workflow: Dict[str, Any]
    ) -> bool:
        """Save workflow definition"""
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO workflows
                    (workflow_id, tenant_id, name, description, trigger_type, trigger_config, steps, enabled, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    workflow["workflow_id"],
                    tenant_id,
                    workflow["name"],
                    workflow.get("description", ""),
                    workflow.get("trigger_type", "scheduled"),
                    json.dumps(workflow.get("trigger_config", {})),
                    json.dumps(workflow.get("steps", [])),
                    workflow.get("enabled", True),
                    datetime.now().isoformat()
                ))
                
                conn.commit()
            
            return True
        except Exception as e:
            logger.error(f"Error saving workflow: {str(e)}")
            return False
    
    def get_execution_history(
        self,
        tenant_id: str,
        workflow_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get workflow execution history"""
        try:
            with self.tenant_isolation.tenant_database(tenant_id) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                query = "SELECT * FROM workflow_executions WHERE tenant_id = ?"
                params = [tenant_id]
                
                if workflow_id:
                    query += " AND workflow_id = ?"
                    params.append(workflow_id)
                
                query += " ORDER BY started_at DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                executions = []
                for row in rows:
                    result = {}
                    if row["result"]:
                        try:
                            result = json.loads(row["result"])
                        except:
                            result = {}
                    
                    executions.append({
                        "execution_id": row["execution_id"],
                        "workflow_id": row["workflow_id"],
                        "status": row["status"],
                        "started_at": row["started_at"],
                        "completed_at": row["completed_at"],
                        "error": row["error"],
                        "result": result
                    })
                
                return executions
        except Exception as e:
            logger.error(f"Error getting execution history: {str(e)}")
            return []


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    
    tenant_manager = TenantManager()
    tenant_isolation = TenantIsolation(tenant_manager)
    persistence = PersistenceLayer(tenant_isolation)
    
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        workflows = persistence.load_workflows(tenant.tenant_id)
        print(f"Loaded {len(workflows)} workflows")
