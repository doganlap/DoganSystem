"""
Agent Delegation - Agent-to-agent task delegation and collaboration
"""

import sqlite3
import logging
import uuid
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from tenant_isolation import TenantIsolation
from employee_agent_system import EmployeeAgentSystem, EmployeeAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DelegationStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Delegation:
    """Agent task delegation"""
    delegation_id: str
    tenant_id: str
    from_agent_id: str
    to_agent_id: str
    task_description: str
    task_type: str  # erpnext_action, email, notification, etc.
    task_config: Dict[str, Any]
    priority: int = 5
    status: str = DelegationStatus.PENDING.value
    created_at: datetime = None
    accepted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict] = None
    notes: Optional[str] = None


class AgentDelegation:
    """Manages agent-to-agent task delegation"""
    
    def __init__(
        self,
        tenant_isolation: TenantIsolation,
        agent_system: EmployeeAgentSystem
    ):
        self.tenant_isolation = tenant_isolation
        self.agent_system = agent_system
        self._init_delegation_tables()
    
    def _init_delegation_tables(self):
        """Initialize delegation tables in tenant databases"""
        # Tables will be created per tenant when needed
        pass
    
    def delegate_task(
        self,
        tenant_id: str,
        from_agent_id: str,
        to_agent_id: str,
        task_description: str,
        task_type: str,
        task_config: Dict[str, Any],
        priority: int = 5
    ) -> Delegation:
        """Delegate a task from one agent to another"""
        # Verify both agents exist
        from_agent = self.agent_system.get_agent(tenant_id, from_agent_id)
        to_agent = self.agent_system.get_agent(tenant_id, to_agent_id)
        
        if not from_agent:
            raise ValueError(f"From agent {from_agent_id} not found")
        if not to_agent:
            raise ValueError(f"To agent {to_agent_id} not found")
        
        # Check if to_agent is available
        if to_agent.status not in ["available", "idle"]:
            logger.warning(f"Agent {to_agent_id} is not available (status: {to_agent.status})")
        
        delegation_id = f"deleg_{uuid.uuid4().hex[:12]}"
        
        delegation = Delegation(
            delegation_id=delegation_id,
            tenant_id=tenant_id,
            from_agent_id=from_agent_id,
            to_agent_id=to_agent_id,
            task_description=task_description,
            task_type=task_type,
            task_config=task_config,
            priority=priority,
            status=DelegationStatus.PENDING.value,
            created_at=datetime.now()
        )
        
        # Save to tenant database
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            cursor = conn.cursor()
            
            # Create delegations table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_delegations (
                    delegation_id VARCHAR(50) PRIMARY KEY,
                    tenant_id VARCHAR(50) NOT NULL,
                    from_agent_id VARCHAR(50) NOT NULL,
                    to_agent_id VARCHAR(50) NOT NULL,
                    task_description TEXT NOT NULL,
                    task_type VARCHAR(50),
                    task_config TEXT, -- JSON
                    priority INTEGER DEFAULT 5,
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at TIMESTAMP,
                    accepted_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    result TEXT, -- JSON
                    notes TEXT
                )
            """)
            
            cursor.execute("""
                INSERT INTO agent_delegations
                (delegation_id, tenant_id, from_agent_id, to_agent_id, task_description,
                 task_type, task_config, priority, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                delegation.delegation_id,
                delegation.tenant_id,
                delegation.from_agent_id,
                delegation.to_agent_id,
                delegation.task_description,
                delegation.task_type,
                json.dumps(delegation.task_config),
                delegation.priority,
                delegation.status,
                delegation.created_at.isoformat()
            ))
            
            conn.commit()
        
        logger.info(f"Task delegated from {from_agent.employee_name} to {to_agent.employee_name}")
        return delegation
    
    def accept_delegation(
        self,
        tenant_id: str,
        delegation_id: str,
        agent_id: str
    ) -> bool:
        """Accept a delegated task"""
        delegation = self.get_delegation(tenant_id, delegation_id)
        if not delegation:
            return False
        
        if delegation.to_agent_id != agent_id:
            raise ValueError("Only the assigned agent can accept this delegation")
        
        if delegation.status != DelegationStatus.PENDING.value:
            raise ValueError(f"Delegation is not pending (status: {delegation.status})")
        
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE agent_delegations
                SET status = ?, accepted_at = ?
                WHERE delegation_id = ? AND tenant_id = ?
            """, (
                DelegationStatus.IN_PROGRESS.value,
                datetime.now().isoformat(),
                delegation_id,
                tenant_id
            ))
            
            conn.commit()
        
        # Update agent status
        self.agent_system.update_agent(tenant_id, agent_id, status="busy")
        
        logger.info(f"Delegation {delegation_id} accepted by agent {agent_id}")
        return True
    
    def complete_delegation(
        self,
        tenant_id: str,
        delegation_id: str,
        result: Dict[str, Any],
        notes: Optional[str] = None
    ) -> bool:
        """Complete a delegated task"""
        delegation = self.get_delegation(tenant_id, delegation_id)
        if not delegation:
            return False
        
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE agent_delegations
                SET status = ?, completed_at = ?, result = ?, notes = ?
                WHERE delegation_id = ? AND tenant_id = ?
            """, (
                DelegationStatus.COMPLETED.value,
                datetime.now().isoformat(),
                json.dumps(result),
                notes,
                delegation_id,
                tenant_id
            ))
            
            conn.commit()
        
        # Update agent status back to available
        self.agent_system.update_agent(tenant_id, delegation.to_agent_id, status="available")
        
        logger.info(f"Delegation {delegation_id} completed")
        return True
    
    def get_delegation(self, tenant_id: str, delegation_id: str) -> Optional[Delegation]:
        """Get delegation by ID"""
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM agent_delegations
                WHERE delegation_id = ? AND tenant_id = ?
            """, (delegation_id, tenant_id))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return self._row_to_delegation(row)
    
    def list_delegations(
        self,
        tenant_id: str,
        agent_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Delegation]:
        """List delegations for a tenant"""
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM agent_delegations WHERE tenant_id = ?"
            params = [tenant_id]
            
            if agent_id:
                query += " AND (from_agent_id = ? OR to_agent_id = ?)"
                params.extend([agent_id, agent_id])
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            query += " ORDER BY created_at DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [self._row_to_delegation(row) for row in rows]
    
    def find_best_agent_for_task(
        self,
        tenant_id: str,
        task_type: str,
        required_capabilities: List[str],
        exclude_agent_id: Optional[str] = None
    ) -> Optional[EmployeeAgent]:
        """Find the best available agent for a task"""
        agents = self.agent_system.list_agents(tenant_id, status="available")
        
        if exclude_agent_id:
            agents = [a for a in agents if a.agent_id != exclude_agent_id]
        
        # Score agents based on capabilities match
        best_agent = None
        best_score = 0
        
        for agent in agents:
            score = 0
            for cap in required_capabilities:
                if cap in agent.capabilities:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_agent = agent
        
        return best_agent
    
    def _row_to_delegation(self, row: sqlite3.Row) -> Delegation:
        """Convert database row to Delegation"""
        task_config = {}
        if row["task_config"]:
            try:
                task_config = json.loads(row["task_config"])
            except:
                task_config = {}
        
        result = None
        if row["result"]:
            try:
                result = json.loads(row["result"])
            except:
                result = {}
        
        return Delegation(
            delegation_id=row["delegation_id"],
            tenant_id=row["tenant_id"],
            from_agent_id=row["from_agent_id"],
            to_agent_id=row["to_agent_id"],
            task_description=row["task_description"],
            task_type=row["task_type"],
            task_config=task_config,
            priority=row["priority"],
            status=row["status"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
            accepted_at=datetime.fromisoformat(row["accepted_at"]) if row["accepted_at"] else None,
            completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
            result=result,
            notes=row["notes"]
        )


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    from employee_agent_system import EmployeeAgentSystem
    
    tenant_manager = TenantManager()
    tenant_isolation = TenantIsolation(tenant_manager)
    agent_system = EmployeeAgentSystem(tenant_isolation)
    delegation = AgentDelegation(tenant_isolation, agent_system)
    
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        # Find best agent for task
        best_agent = delegation.find_best_agent_for_task(
            tenant.tenant_id,
            "quotation",
            ["customer_management", "quotation"]
        )
        
        if best_agent:
            print(f"Best agent: {best_agent.employee_name}")
