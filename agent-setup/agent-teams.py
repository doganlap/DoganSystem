"""
Agent Teams - Team creation and management per tenant
"""

import sqlite3
import logging
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

from tenant_isolation import TenantIsolation
from employee_agent_system import EmployeeAgentSystem, EmployeeAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgentTeam:
    """Agent team"""
    team_id: str
    tenant_id: str
    team_name: str
    department: Optional[str] = None
    manager_id: Optional[str] = None
    created_at: Optional[datetime] = None


class AgentTeams:
    """Manages agent teams per tenant"""
    
    def __init__(
        self,
        tenant_isolation: TenantIsolation,
        agent_system: EmployeeAgentSystem
    ):
        self.tenant_isolation = tenant_isolation
        self.agent_system = agent_system
    
    def create_team(
        self,
        tenant_id: str,
        team_name: str,
        department: Optional[str] = None,
        manager_id: Optional[str] = None
    ) -> AgentTeam:
        """Create a new team"""
        team_id = f"team_{uuid.uuid4().hex[:12]}"
        
        # Verify manager exists if provided
        if manager_id:
            manager = self.agent_system.get_agent(tenant_id, manager_id)
            if not manager:
                raise ValueError(f"Manager agent {manager_id} not found")
        
        team = AgentTeam(
            team_id=team_id,
            tenant_id=tenant_id,
            team_name=team_name,
            department=department,
            manager_id=manager_id,
            created_at=datetime.now()
        )
        
        # Save to tenant database
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            cursor = conn.cursor()
            
            # Ensure teams table exists
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
            
            cursor.execute("""
                INSERT INTO agent_teams
                (team_id, tenant_id, team_name, department, manager_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                team.team_id,
                team.tenant_id,
                team.team_name,
                team.department,
                team.manager_id,
                team.created_at.isoformat()
            ))
            
            conn.commit()
        
        logger.info(f"Team created: {team_name} ({team_id}) for tenant {tenant_id}")
        return team
    
    def get_team(self, tenant_id: str, team_id: str) -> Optional[AgentTeam]:
        """Get team by ID"""
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM agent_teams WHERE team_id = ? AND tenant_id = ?
            """, (team_id, tenant_id))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return self._row_to_team(row)
    
    def list_teams(
        self,
        tenant_id: str,
        department: Optional[str] = None
    ) -> List[AgentTeam]:
        """List teams for a tenant"""
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM agent_teams WHERE tenant_id = ?"
            params = [tenant_id]
            
            if department:
                query += " AND department = ?"
                params.append(department)
            
            query += " ORDER BY team_name"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [self._row_to_team(row) for row in rows]
    
    def add_agent_to_team(
        self,
        tenant_id: str,
        agent_id: str,
        team_id: str
    ) -> bool:
        """Add an agent to a team"""
        # Verify team exists
        team = self.get_team(tenant_id, team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")
        
        # Update agent's team_id
        return self.agent_system.update_agent(tenant_id, agent_id, team_id=team_id)
    
    def remove_agent_from_team(
        self,
        tenant_id: str,
        agent_id: str
    ) -> bool:
        """Remove an agent from their team"""
        return self.agent_system.update_agent(tenant_id, agent_id, team_id=None)
    
    def get_team_members(self, tenant_id: str, team_id: str) -> List[EmployeeAgent]:
        """Get all agents in a team"""
        return self.agent_system.get_agents_by_team(tenant_id, team_id)
    
    def get_team_performance(
        self,
        tenant_id: str,
        team_id: str
    ) -> Dict[str, Any]:
        """Get team performance metrics"""
        members = self.get_team_members(tenant_id, team_id)
        team = self.get_team(tenant_id, team_id)
        
        if not team:
            return {}
        
        return {
            "team_id": team_id,
            "team_name": team.team_name,
            "department": team.department,
            "member_count": len(members),
            "available_members": sum(1 for m in members if m.status == "available"),
            "busy_members": sum(1 for m in members if m.status == "busy"),
            "members": [
                {
                    "agent_id": m.agent_id,
                    "employee_name": m.employee_name,
                    "role": m.role,
                    "status": m.status
                }
                for m in members
            ]
        }
    
    def delete_team(self, tenant_id: str, team_id: str) -> bool:
        """Delete a team (agents are not deleted, just removed from team)"""
        # Remove all agents from team first
        members = self.get_team_members(tenant_id, team_id)
        for member in members:
            self.remove_agent_from_team(tenant_id, member.agent_id)
        
        # Delete team
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM agent_teams WHERE team_id = ? AND tenant_id = ?
            """, (team_id, tenant_id))
            
            conn.commit()
            
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Team {team_id} deleted from tenant {tenant_id}")
            
            return success
    
    def _row_to_team(self, row: sqlite3.Row) -> AgentTeam:
        """Convert database row to AgentTeam"""
        return AgentTeam(
            team_id=row["team_id"],
            tenant_id=row["tenant_id"],
            team_name=row["team_name"],
            department=row["department"],
            manager_id=row["manager_id"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None
        )


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    from employee_agent_system import EmployeeAgentSystem
    
    tenant_manager = TenantManager()
    tenant_isolation = TenantIsolation(tenant_manager)
    agent_system = EmployeeAgentSystem(tenant_isolation)
    teams = AgentTeams(tenant_isolation, agent_system)
    
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        # Create team
        team = teams.create_team(
            tenant_id=tenant.tenant_id,
            team_name="Sales Team A",
            department="Sales"
        )
        print(f"Created team: {team.team_name} ({team.team_id})")
        
        # Get team performance
        performance = teams.get_team_performance(tenant.tenant_id, team.team_id)
        print(f"Team performance: {performance}")
