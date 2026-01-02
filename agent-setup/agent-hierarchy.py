"""
Agent Hierarchy - Manager-worker relationships and organizational structure
"""

import sqlite3
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from tenant_isolation import TenantIsolation
from employee_agent_system import EmployeeAgentSystem, EmployeeAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class HierarchyLevel:
    """Hierarchy level in organization"""
    level: int
    title: str
    description: str


class AgentHierarchy:
    """Manages agent hierarchy and reporting structure"""
    
    def __init__(
        self,
        tenant_isolation: TenantIsolation,
        agent_system: EmployeeAgentSystem
    ):
        self.tenant_isolation = tenant_isolation
        self.agent_system = agent_system
    
    def set_manager(
        self,
        tenant_id: str,
        agent_id: str,
        manager_id: str
    ) -> bool:
        """Set an agent's manager"""
        # Verify both agents exist
        agent = self.agent_system.get_agent(tenant_id, agent_id)
        manager = self.agent_system.get_agent(tenant_id, manager_id)
        
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        if not manager:
            raise ValueError(f"Manager {manager_id} not found")
        
        # Prevent circular references
        if self._would_create_circle(tenant_id, agent_id, manager_id):
            raise ValueError("Setting this manager would create a circular reference")
        
        return self.agent_system.update_agent(tenant_id, agent_id, manager_id=manager_id)
    
    def _would_create_circle(
        self,
        tenant_id: str,
        agent_id: str,
        potential_manager_id: str
    ) -> bool:
        """Check if setting manager would create circular reference"""
        # If potential manager's manager chain leads to agent_id, it's a circle
        current = potential_manager_id
        visited = set()
        
        while current:
            if current == agent_id:
                return True
            if current in visited:
                break
            
            visited.add(current)
            agent = self.agent_system.get_agent(tenant_id, current)
            if not agent or not agent.manager_id:
                break
            current = agent.manager_id
        
        return False
    
    def get_direct_reports(self, tenant_id: str, manager_id: str) -> List[EmployeeAgent]:
        """Get all agents directly reporting to a manager"""
        all_agents = self.agent_system.list_agents(tenant_id)
        return [a for a in all_agents if a.manager_id == manager_id]
    
    def get_all_reports(self, tenant_id: str, manager_id: str) -> List[EmployeeAgent]:
        """Get all agents in manager's reporting chain (recursive)"""
        direct_reports = self.get_direct_reports(tenant_id, manager_id)
        all_reports = list(direct_reports)
        
        # Recursively get reports of reports
        for report in direct_reports:
            all_reports.extend(self.get_all_reports(tenant_id, report.agent_id))
        
        return all_reports
    
    def get_management_chain(self, tenant_id: str, agent_id: str) -> List[EmployeeAgent]:
        """Get the management chain from agent to top (all managers up the chain)"""
        chain = []
        current = agent_id
        
        while current:
            agent = self.agent_system.get_agent(tenant_id, current)
            if not agent:
                break
            
            if agent.manager_id:
                manager = self.agent_system.get_agent(tenant_id, agent.manager_id)
                if manager:
                    chain.append(manager)
                    current = manager.agent_id
                else:
                    break
            else:
                break
        
        return chain
    
    def get_org_chart(self, tenant_id: str) -> Dict[str, Any]:
        """Get organizational chart for tenant"""
        all_agents = self.agent_system.list_agents(tenant_id)
        
        # Find top-level agents (no manager)
        top_level = [a for a in all_agents if not a.manager_id]
        
        def build_tree(agent: EmployeeAgent) -> Dict[str, Any]:
            """Recursively build agent tree"""
            reports = self.get_direct_reports(tenant_id, agent.agent_id)
            
            return {
                "agent_id": agent.agent_id,
                "employee_name": agent.employee_name,
                "role": agent.role,
                "department": agent.department,
                "status": agent.status,
                "reports": [build_tree(r) for r in reports]
            }
        
        org_chart = {
            "tenant_id": tenant_id,
            "top_level": [build_tree(a) for a in top_level],
            "total_agents": len(all_agents),
            "departments": {}
        }
        
        # Group by department
        for agent in all_agents:
            dept = agent.department or "Unassigned"
            if dept not in org_chart["departments"]:
                org_chart["departments"][dept] = []
            org_chart["departments"][dept].append({
                "agent_id": agent.agent_id,
                "employee_name": agent.employee_name,
                "role": agent.role
            })
        
        return org_chart
    
    def assign_task_to_team(
        self,
        tenant_id: str,
        manager_id: str,
        task_description: str,
        task_type: str,
        task_config: Dict[str, Any]
    ) -> List[str]:
        """Assign task to manager's team (delegates to all direct reports)"""
        from agent_delegation import AgentDelegation
        
        delegation = AgentDelegation(self.tenant_isolation, self.agent_system)
        reports = self.get_direct_reports(tenant_id, manager_id)
        
        delegation_ids = []
        for report in reports:
            if report.status == "available":
                delg = delegation.delegate_task(
                    tenant_id=tenant_id,
                    from_agent_id=manager_id,
                    to_agent_id=report.agent_id,
                    task_description=task_description,
                    task_type=task_type,
                    task_config=task_config
                )
                delegation_ids.append(delg.delegation_id)
        
        return delegation_ids
    
    def escalate_to_manager(
        self,
        tenant_id: str,
        agent_id: str,
        task_description: str,
        task_type: str,
        task_config: Dict[str, Any]
    ) -> Optional[str]:
        """Escalate task to agent's manager"""
        agent = self.agent_system.get_agent(tenant_id, agent_id)
        if not agent or not agent.manager_id:
            return None  # No manager to escalate to
        
        from agent_delegation import AgentDelegation
        delegation = AgentDelegation(self.tenant_isolation, self.agent_system)
        
        delg = delegation.delegate_task(
            tenant_id=tenant_id,
            from_agent_id=agent_id,
            to_agent_id=agent.manager_id,
            task_description=f"[ESCALATED] {task_description}",
            task_type=task_type,
            task_config=task_config,
            priority=8  # Higher priority for escalations
        )
        
        return delg.delegation_id


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    from employee_agent_system import EmployeeAgentSystem
    
    tenant_manager = TenantManager()
    tenant_isolation = TenantIsolation(tenant_manager)
    agent_system = EmployeeAgentSystem(tenant_isolation)
    hierarchy = AgentHierarchy(tenant_isolation, agent_system)
    
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        # Get org chart
        org_chart = hierarchy.get_org_chart(tenant.tenant_id)
        print(f"Org chart: {org_chart}")
