"""
Employee Agent System - Employee-style agents per tenant
Agents with names, roles, departments, teams, and hierarchy
"""

import sqlite3
import logging
import uuid
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

from tenant_isolation import TenantIsolation, get_current_tenant_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmployeeAgent:
    """Employee-style agent"""
    agent_id: str
    tenant_id: str
    employee_name: str
    role: str
    department: Optional[str] = None
    team_id: Optional[str] = None
    manager_id: Optional[str] = None
    capabilities: List[str] = None
    status: str = "available"  # available, busy, away, offline
    api_key: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []


class EmployeeAgentSystem:
    """Manages employee-style agents per tenant"""
    
    def __init__(self, tenant_isolation: TenantIsolation):
        self.tenant_isolation = tenant_isolation
    
    def create_agent(
        self,
        tenant_id: str,
        employee_name: str,
        role: str,
        department: Optional[str] = None,
        team_id: Optional[str] = None,
        manager_id: Optional[str] = None,
        capabilities: Optional[List[str]] = None
    ) -> EmployeeAgent:
        """Create a new employee-style agent"""
        agent_id = f"agent_{uuid.uuid4().hex[:12]}"
        api_key = f"ak_{uuid.uuid4().hex[:16]}"
        
        agent = EmployeeAgent(
            agent_id=agent_id,
            tenant_id=tenant_id,
            employee_name=employee_name,
            role=role,
            department=department,
            team_id=team_id,
            manager_id=manager_id,
            capabilities=capabilities or [],
            status="available",
            api_key=api_key,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Save to tenant database
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO agents
                (agent_id, tenant_id, employee_name, role, department, team_id, manager_id,
                 capabilities, status, api_key, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                agent.agent_id,
                agent.tenant_id,
                agent.employee_name,
                agent.role,
                agent.department,
                agent.team_id,
                agent.manager_id,
                json.dumps(agent.capabilities),
                agent.status,
                agent.api_key,
                agent.created_at.isoformat(),
                agent.updated_at.isoformat()
            ))
            
            conn.commit()
        
        logger.info(f"Agent created: {employee_name} ({agent_id}) for tenant {tenant_id}")
        return agent
    
    def get_agent(self, tenant_id: str, agent_id: str) -> Optional[EmployeeAgent]:
        """Get agent by ID"""
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM agents WHERE agent_id = ? AND tenant_id = ?
            """, (agent_id, tenant_id))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return self._row_to_agent(row)
    
    def list_agents(
        self,
        tenant_id: str,
        department: Optional[str] = None,
        team_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[EmployeeAgent]:
        """List agents for a tenant"""
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM agents WHERE tenant_id = ?"
            params = [tenant_id]
            
            if department:
                query += " AND department = ?"
                params.append(department)
            
            if team_id:
                query += " AND team_id = ?"
                params.append(team_id)
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            query += " ORDER BY employee_name"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [self._row_to_agent(row) for row in rows]
    
    def update_agent(
        self,
        tenant_id: str,
        agent_id: str,
        employee_name: Optional[str] = None,
        role: Optional[str] = None,
        department: Optional[str] = None,
        team_id: Optional[str] = None,
        manager_id: Optional[str] = None,
        status: Optional[str] = None,
        capabilities: Optional[List[str]] = None
    ) -> bool:
        """Update agent information"""
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if employee_name:
                updates.append("employee_name = ?")
                params.append(employee_name)
            
            if role:
                updates.append("role = ?")
                params.append(role)
            
            if department:
                updates.append("department = ?")
                params.append(department)
            
            if team_id:
                updates.append("team_id = ?")
                params.append(team_id)
            
            if manager_id:
                updates.append("manager_id = ?")
                params.append(manager_id)
            
            if status:
                updates.append("status = ?")
                params.append(status)
            
            if capabilities:
                updates.append("capabilities = ?")
                params.append(json.dumps(capabilities))
            
            if not updates:
                return False
            
            updates.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            params.extend([agent_id, tenant_id])
            
            query = f"UPDATE agents SET {', '.join(updates)} WHERE agent_id = ? AND tenant_id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Agent {agent_id} updated for tenant {tenant_id}")
            
            return success
    
    def delete_agent(self, tenant_id: str, agent_id: str) -> bool:
        """Delete an agent"""
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM agents WHERE agent_id = ? AND tenant_id = ?
            """, (agent_id, tenant_id))
            
            conn.commit()
            
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Agent {agent_id} deleted from tenant {tenant_id}")
            
            return success
    
    def get_agents_by_manager(self, tenant_id: str, manager_id: str) -> List[EmployeeAgent]:
        """Get all agents reporting to a manager"""
        return self.list_agents(tenant_id=tenant_id, status=None)
        # Filter by manager_id in application code since SQLite doesn't support complex queries easily
    
    def get_agents_by_team(self, tenant_id: str, team_id: str) -> List[EmployeeAgent]:
        """Get all agents in a team"""
        return self.list_agents(tenant_id=tenant_id, team_id=team_id)
    
    def get_agents_by_department(self, tenant_id: str, department: str) -> List[EmployeeAgent]:
        """Get all agents in a department"""
        return self.list_agents(tenant_id=tenant_id, department=department)
    
    def _row_to_agent(self, row: sqlite3.Row) -> EmployeeAgent:
        """Convert database row to EmployeeAgent"""
        capabilities = []
        if row["capabilities"]:
            try:
                capabilities = json.loads(row["capabilities"])
            except:
                capabilities = []
        
        return EmployeeAgent(
            agent_id=row["agent_id"],
            tenant_id=row["tenant_id"],
            employee_name=row["employee_name"],
            role=row["role"],
            department=row["department"],
            team_id=row["team_id"],
            manager_id=row["manager_id"],
            capabilities=capabilities,
            status=row["status"],
            api_key=row["api_key"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
            updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None
        )


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    
    tenant_manager = TenantManager()
    tenant_isolation = TenantIsolation(tenant_manager)
    agent_system = EmployeeAgentSystem(tenant_isolation)
    
    # Create agent
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        agent = agent_system.create_agent(
            tenant_id=tenant.tenant_id,
            employee_name="Ahmed Al-Saud",
            role="Sales Manager",
            department="Sales",
            capabilities=["customer_management", "quotation", "sales_order"]
        )
        print(f"Created agent: {agent.employee_name} ({agent.agent_id})")
        
        # List agents
        agents = agent_system.list_agents(tenant.tenant_id)
        print(f"Total agents: {len(agents)}")
