"""
Bridge between Claude Code subagents and ERPNext
Allows Claude Code agents to work as ERP employees
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from anthropic import Anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SubagentEmployee:
    """Represents a Claude Code subagent configured as an ERP employee"""
    employee_id: str
    employee_name: str
    role: str
    department: str
    subagent_type: str  # 'Explore', 'Plan', 'general-purpose'
    capabilities: List[str]
    system_prompt: str
    created_at: str
    status: str = "available"


@dataclass
class TaskExecution:
    """Represents a task execution by a subagent employee"""
    task_id: str
    employee_id: str
    employee_name: str
    task_description: str
    subagent_type: str
    status: str  # 'pending', 'in_progress', 'completed', 'failed'
    created_at: str
    completed_at: Optional[str] = None
    result: Optional[Dict] = None
    error: Optional[str] = None


class SubagentERPNextBridge:
    """
    Bridges Claude Code subagents with ERPNext
    Translates natural language tasks into ERPNext operations
    """

    def __init__(self, erpnext_base_url: str, erpnext_api_key: str = None, erpnext_api_secret: str = None):
        self.erpnext_base_url = erpnext_base_url
        self.erpnext_api_key = erpnext_api_key or os.getenv("ERPNEXT_API_KEY")
        self.erpnext_api_secret = erpnext_api_secret or os.getenv("ERPNEXT_API_SECRET")

        # Storage for employees and tasks
        self.employees: Dict[str, SubagentEmployee] = {}
        self.task_history: List[TaskExecution] = []

        # Initialize default employees
        self._create_default_employees()

    def _create_default_employees(self):
        """Create default subagent employees"""
        # System Analyst (Explore agent)
        self.create_explorer_employee(
            employee_name="Sarah Al-Mutairi",
            department="IT",
            employee_id="emp_explorer_001"
        )

        # Business Process Architect (Plan agent)
        self.create_planner_employee(
            employee_name="Mohammed Al-Ahmad",
            department="Operations",
            employee_id="emp_planner_001"
        )

        # Operations Manager (general-purpose agent)
        self.create_operations_employee(
            employee_name="Fatima Al-Saud",
            department="Sales",
            employee_id="emp_operations_001"
        )

        logger.info(f"Created {len(self.employees)} default subagent employees")

    def create_explorer_employee(
        self,
        employee_name: str,
        department: str,
        employee_id: Optional[str] = None
    ) -> SubagentEmployee:
        """
        Create an Explore agent configured as ERP System Analyst
        """
        employee_id = employee_id or f"emp_explorer_{len([e for e in self.employees.values() if e.subagent_type == 'Explore']) + 1:03d}"

        employee = SubagentEmployee(
            employee_id=employee_id,
            employee_name=employee_name,
            role="System Analyst",
            department=department,
            subagent_type="Explore",
            capabilities=[
                "codebase_exploration",
                "configuration_analysis",
                "workflow_mapping",
                "customization_discovery",
                "doctype_analysis",
                "field_mapping"
            ],
            system_prompt=f"""You are {employee_name}, a System Analyst in the {department} department.

Your role is to explore and understand the ERPNext system configuration.
You have deep knowledge of Frappe framework and ERPNext structure.

Key responsibilities:
- Explore ERPNext codebase and configurations
- Find and analyze doctypes, custom fields, and workflows
- Map data relationships and dependencies
- Identify customization points
- Document system architecture

ERPNext Details:
- Base URL: {self.erpnext_base_url}
- Framework: Frappe + ERPNext v16
- Primary Language: Python (backend), JavaScript (frontend)
- Database: MariaDB

Use your exploration tools to thoroughly investigate the ERPNext system.
Always provide detailed findings with file paths and line numbers.""",
            created_at=datetime.now().isoformat(),
            status="available"
        )

        self.employees[employee_id] = employee
        logger.info(f"Created Explorer employee: {employee_name} ({employee_id})")
        return employee

    def create_planner_employee(
        self,
        employee_name: str,
        department: str,
        employee_id: Optional[str] = None
    ) -> SubagentEmployee:
        """
        Create a Plan agent configured as Business Process Architect
        """
        employee_id = employee_id or f"emp_planner_{len([e for e in self.employees.values() if e.subagent_type == 'Plan']) + 1:03d}"

        employee = SubagentEmployee(
            employee_id=employee_id,
            employee_name=employee_name,
            role="Business Process Architect",
            department=department,
            subagent_type="Plan",
            capabilities=[
                "process_design",
                "workflow_planning",
                "implementation_strategy",
                "risk_assessment",
                "architecture_design",
                "migration_planning"
            ],
            system_prompt=f"""You are {employee_name}, a Business Process Architect in the {department} department.

Your role is to design and plan complex ERP operations and implementations.
You understand ERPNext modules, data flows, and business processes deeply.

Key responsibilities:
- Design multi-step business processes
- Create detailed implementation plans
- Identify dependencies and risks
- Plan data migrations
- Design workflow automations
- Optimize business operations

ERPNext Context:
- Base URL: {self.erpnext_base_url}
- Available Modules: CRM, Sales, Buying, Stock, Accounts, HR, Projects, Manufacturing
- Customization: Supports custom fields, scripts, print formats, workflows

Create detailed, actionable plans with:
1. Clear step-by-step instructions
2. Risk assessment and mitigation
3. Resource requirements
4. Timeline estimates
5. Success criteria

Always consider ERPNext best practices and Frappe framework patterns.""",
            created_at=datetime.now().isoformat(),
            status="available"
        )

        self.employees[employee_id] = employee
        logger.info(f"Created Planner employee: {employee_name} ({employee_id})")
        return employee

    def create_operations_employee(
        self,
        employee_name: str,
        department: str,
        employee_id: Optional[str] = None
    ) -> SubagentEmployee:
        """
        Create a general-purpose agent configured as Operations Manager
        """
        employee_id = employee_id or f"emp_ops_{len([e for e in self.employees.values() if e.subagent_type == 'general-purpose']) + 1:03d}"

        employee = SubagentEmployee(
            employee_id=employee_id,
            employee_name=employee_name,
            role="Operations Manager",
            department=department,
            subagent_type="general-purpose",
            capabilities=[
                "data_operations",
                "workflow_execution",
                "bulk_processing",
                "report_generation",
                "multi_module_coordination",
                "email_automation",
                "document_processing"
            ],
            system_prompt=f"""You are {employee_name}, an Operations Manager in the {department} department.

Your role is to execute complex multi-step ERP operations efficiently and accurately.
You have access to ERPNext API and can perform various data operations.

Key responsibilities:
- Execute multi-step workflows
- Perform bulk data operations
- Generate and analyze reports
- Coordinate operations across modules
- Automate business processes
- Handle email notifications
- Process documents and forms

ERPNext Access:
- Base URL: {self.erpnext_base_url}
- API Authentication: Available
- Modules: Full access to all ERPNext modules

Operation Guidelines:
1. Always validate data before making changes
2. Log all significant actions
3. Handle errors gracefully
4. Provide detailed execution reports
5. Follow ERPNext permissions and validations

You can use ERPNext REST API endpoints for all operations.
Always confirm destructive operations before execution.""",
            created_at=datetime.now().isoformat(),
            status="available"
        )

        self.employees[employee_id] = employee
        logger.info(f"Created Operations employee: {employee_name} ({employee_id})")
        return employee

    def assign_task(
        self,
        employee_id: str,
        task_description: str,
        task_context: Optional[Dict] = None
    ) -> TaskExecution:
        """
        Assign a task to a subagent employee

        Args:
            employee_id: ID of the employee to assign task to
            task_description: Natural language description of the task
            task_context: Additional context (credentials, specific data, etc.)

        Returns:
            TaskExecution object representing the task
        """
        employee = self.employees.get(employee_id)
        if not employee:
            raise ValueError(f"Employee not found: {employee_id}")

        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.task_history) + 1}"

        task = TaskExecution(
            task_id=task_id,
            employee_id=employee.employee_id,
            employee_name=employee.employee_name,
            task_description=task_description,
            subagent_type=employee.subagent_type,
            status="pending",
            created_at=datetime.now().isoformat()
        )

        self.task_history.append(task)

        # Update employee status
        employee.status = "busy"

        logger.info(f"Task {task_id} assigned to {employee.employee_name}")
        return task

    def get_task_prompt(self, task: TaskExecution) -> str:
        """
        Generate the full prompt for the subagent to execute the task
        """
        employee = self.employees[task.employee_id]

        prompt = f"""
=== EMPLOYEE INFORMATION ===
Name: {employee.employee_name}
Role: {employee.role}
Department: {employee.department}
Employee ID: {employee.employee_id}

=== TASK ASSIGNMENT ===
Task ID: {task.task_id}
Assigned: {task.created_at}

=== TASK DESCRIPTION ===
{task.task_description}

=== ERPNext CONTEXT ===
Base URL: {self.erpnext_base_url}
API Key: {self.erpnext_api_key[:10]}... (available in environment)
API Secret: [AVAILABLE]

Available Capabilities:
{chr(10).join(f"  - {cap}" for cap in employee.capabilities)}

=== YOUR ROLE ===
{employee.system_prompt}

=== INSTRUCTIONS ===
Please complete the task described above using your available tools and capabilities.
Document all steps taken and provide a detailed summary of results.

If you need to access ERPNext API, use these credentials from environment:
- ERPNEXT_BASE_URL: {self.erpnext_base_url}
- ERPNEXT_API_KEY: [from environment]
- ERPNEXT_API_SECRET: [from environment]
"""
        return prompt

    def mark_task_completed(
        self,
        task_id: str,
        result: Dict,
        error: Optional[str] = None
    ):
        """Mark a task as completed with results"""
        task = next((t for t in self.task_history if t.task_id == task_id), None)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        task.status = "completed" if not error else "failed"
        task.completed_at = datetime.now().isoformat()
        task.result = result
        task.error = error

        # Update employee status
        employee = self.employees[task.employee_id]
        employee.status = "available"

        logger.info(f"Task {task_id} marked as {task.status}")

    def get_employee_by_role(self, role: str) -> Optional[SubagentEmployee]:
        """Get an available employee by role"""
        for employee in self.employees.values():
            if employee.role == role and employee.status == "available":
                return employee
        return None

    def get_employee_by_type(self, subagent_type: str) -> Optional[SubagentEmployee]:
        """Get an available employee by subagent type"""
        for employee in self.employees.values():
            if employee.subagent_type == subagent_type and employee.status == "available":
                return employee
        return None

    def list_employees(
        self,
        department: Optional[str] = None,
        status: Optional[str] = None,
        subagent_type: Optional[str] = None
    ) -> List[SubagentEmployee]:
        """List employees with optional filters"""
        employees = list(self.employees.values())

        if department:
            employees = [e for e in employees if e.department == department]
        if status:
            employees = [e for e in employees if e.status == status]
        if subagent_type:
            employees = [e for e in employees if e.subagent_type == subagent_type]

        return employees

    def get_task_history(
        self,
        employee_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[TaskExecution]:
        """Get task history with optional filters"""
        tasks = self.task_history

        if employee_id:
            tasks = [t for t in tasks if t.employee_id == employee_id]
        if status:
            tasks = [t for t in tasks if t.status == status]

        return tasks

    def get_system_status(self) -> Dict:
        """Get overall system status"""
        total_employees = len(self.employees)
        available_employees = len([e for e in self.employees.values() if e.status == "available"])
        busy_employees = len([e for e in self.employees.values() if e.status == "busy"])

        total_tasks = len(self.task_history)
        completed_tasks = len([t for t in self.task_history if t.status == "completed"])
        failed_tasks = len([t for t in self.task_history if t.status == "failed"])
        pending_tasks = len([t for t in self.task_history if t.status in ["pending", "in_progress"]])

        return {
            "timestamp": datetime.now().isoformat(),
            "erpnext_url": self.erpnext_base_url,
            "employees": {
                "total": total_employees,
                "available": available_employees,
                "busy": busy_employees,
                "by_type": {
                    "explorer": len([e for e in self.employees.values() if e.subagent_type == "Explore"]),
                    "planner": len([e for e in self.employees.values() if e.subagent_type == "Plan"]),
                    "operations": len([e for e in self.employees.values() if e.subagent_type == "general-purpose"])
                }
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "failed": failed_tasks,
                "pending": pending_tasks
            }
        }

    def save_state(self, filepath: str = "subagent_bridge_state.json"):
        """Save current state to file"""
        state = {
            "employees": {eid: asdict(emp) for eid, emp in self.employees.items()},
            "task_history": [asdict(task) for task in self.task_history],
            "saved_at": datetime.now().isoformat()
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        logger.info(f"State saved to {filepath}")

    def load_state(self, filepath: str = "subagent_bridge_state.json"):
        """Load state from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)

            # Restore employees
            self.employees = {
                eid: SubagentEmployee(**emp_data)
                for eid, emp_data in state["employees"].items()
            }

            # Restore task history
            self.task_history = [
                TaskExecution(**task_data)
                for task_data in state["task_history"]
            ]

            logger.info(f"State loaded from {filepath}")
            logger.info(f"Loaded {len(self.employees)} employees and {len(self.task_history)} tasks")
        except FileNotFoundError:
            logger.warning(f"State file not found: {filepath}")
        except Exception as e:
            logger.error(f"Error loading state: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Initialize bridge
    bridge = SubagentERPNextBridge(
        erpnext_base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    )

    print("\n=== SUBAGENT ERP EMPLOYEES ===\n")

    # List all employees
    employees = bridge.list_employees()
    for emp in employees:
        print(f"  {emp.employee_name}")
        print(f"    Role: {emp.role}")
        print(f"    Department: {emp.department}")
        print(f"    Type: {emp.subagent_type}")
        print(f"    Status: {emp.status}")
        print(f"    Capabilities: {', '.join(emp.capabilities[:3])}...")
        print()

    # Example task assignment
    print("=== TASK ASSIGNMENT EXAMPLE ===\n")

    # Get the explorer employee
    explorer = bridge.get_employee_by_type("Explore")
    if explorer:
        task = bridge.assign_task(
            employee_id=explorer.employee_id,
            task_description="""
            Explore the ERPNext Sales module and provide:
            1. All custom fields added to Sales Order doctype
            2. Custom print formats for quotations
            3. Workflow states for sales orders
            """
        )

        print(f"Task {task.task_id} assigned to {task.employee_name}")
        print(f"\nTask Prompt Preview:")
        print(bridge.get_task_prompt(task)[:500] + "...")

    # System status
    print("\n=== SYSTEM STATUS ===\n")
    status = bridge.get_system_status()
    print(json.dumps(status, indent=2))

    # Save state
    bridge.save_state()
    print("\nState saved to subagent_bridge_state.json")
