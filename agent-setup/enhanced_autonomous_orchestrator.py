"""
Enhanced Autonomous Orchestrator with Claude Code Subagent Integration
Combines autonomous workflows with Claude Code subagent employees
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from claude_code_bridge import SubagentERPNextBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedAutonomousOrchestrator:
    """
    Enhanced autonomous orchestrator that leverages Claude Code subagents
    for complex ERP operations
    """

    def __init__(self, erpnext_base_url: str):
        self.erpnext_base_url = erpnext_base_url

        # Initialize the subagent bridge
        self.subagent_bridge = SubagentERPNextBridge(erpnext_base_url)

        # Workflow registry
        self.autonomous_workflows: Dict[str, Dict] = {}

        # Initialize default workflows
        self._register_default_workflows()

        logger.info("Enhanced Autonomous Orchestrator initialized")

    def _register_default_workflows(self):
        """Register default autonomous workflows using subagents"""

        # Workflow 1: Daily System Health Check
        self.register_workflow(
            workflow_id="daily_health_check",
            name="Daily System Health Check",
            description="Explore ERPNext configuration daily to identify issues",
            schedule="daily_9am",
            subagent_type="Explore",
            task_template="""
            Perform daily ERPNext system health check:

            1. Check for configuration errors
            2. Identify any broken customizations
            3. Review system error logs
            4. Verify all modules are functioning
            5. Check database integrity
            6. Report any issues found

            Provide a health status report.
            """
        )

        # Workflow 2: Weekly Process Optimization
        self.register_workflow(
            workflow_id="weekly_optimization",
            name="Weekly Process Optimization Review",
            description="Analyze and optimize business processes weekly",
            schedule="weekly_monday",
            subagent_type="Plan",
            task_template="""
            Review and optimize business processes:

            1. Analyze last week's sales workflow performance
            2. Identify bottlenecks or inefficiencies
            3. Review automated workflows
            4. Suggest improvements
            5. Plan optimization implementations

            Provide optimization recommendations.
            """
        )

        # Workflow 3: Monthly Closing Automation
        self.register_workflow(
            workflow_id="monthly_closing",
            name="Monthly Sales Closing",
            description="Automate month-end sales closing process",
            schedule="monthly_last_day",
            subagent_type="general-purpose",
            task_template="""
            Execute monthly sales closing:

            1. Generate all pending invoices
            2. Send invoices to customers
            3. Update payment statuses
            4. Send payment reminders for overdue invoices
            5. Generate monthly reports
            6. Archive completed transactions

            Provide execution summary.
            """
        )

        # Workflow 4: Customer Follow-up Automation
        self.register_workflow(
            workflow_id="customer_followup",
            name="Automated Customer Follow-up",
            description="Follow up on pending quotations and orders",
            schedule="daily_10am",
            subagent_type="general-purpose",
            task_template="""
            Execute customer follow-up workflow:

            1. Find quotations pending for >3 days
            2. Find sales orders awaiting confirmation
            3. Send follow-up emails to customers
            4. Update quotation/order status
            5. Log all communications
            6. Generate follow-up report

            Provide follow-up summary.
            """
        )

        logger.info(f"Registered {len(self.autonomous_workflows)} default workflows")

    def register_workflow(
        self,
        workflow_id: str,
        name: str,
        description: str,
        schedule: str,
        subagent_type: str,
        task_template: str
    ):
        """Register a new autonomous workflow"""
        workflow = {
            "workflow_id": workflow_id,
            "name": name,
            "description": description,
            "schedule": schedule,
            "subagent_type": subagent_type,
            "task_template": task_template,
            "enabled": True,
            "last_run": None,
            "next_run": None,
            "execution_count": 0
        }

        self.autonomous_workflows[workflow_id] = workflow
        logger.info(f"Workflow registered: {name} ({workflow_id})")

    def delegate_to_subagent(
        self,
        task_description: str,
        task_type: str = "auto",
        employee_id: Optional[str] = None
    ) -> Dict:
        """
        Delegate a task to the appropriate Claude Code subagent

        Args:
            task_description: Natural language description of the task
            task_type: Type of task ('explore', 'plan', 'execute', or 'auto')
            employee_id: Specific employee ID (optional, auto-selects if not provided)

        Returns:
            Task execution details
        """
        # Auto-detect task type if not specified
        if task_type == "auto":
            task_type = self._detect_task_type(task_description)

        # Map task type to subagent type
        subagent_type_mapping = {
            "explore": "Explore",
            "plan": "Plan",
            "execute": "general-purpose"
        }

        subagent_type = subagent_type_mapping.get(task_type, "general-purpose")

        # Get appropriate employee
        if employee_id:
            employee = self.subagent_bridge.employees.get(employee_id)
        else:
            employee = self.subagent_bridge.get_employee_by_type(subagent_type)

        if not employee:
            raise ValueError(f"No available employee for task type: {task_type}")

        # Assign task
        task = self.subagent_bridge.assign_task(
            employee_id=employee.employee_id,
            task_description=task_description
        )

        logger.info(f"Task {task.task_id} delegated to {employee.employee_name}")

        return {
            "task_id": task.task_id,
            "employee_name": employee.employee_name,
            "employee_role": employee.role,
            "subagent_type": subagent_type,
            "task_description": task_description,
            "status": task.status,
            "prompt": self.subagent_bridge.get_task_prompt(task)
        }

    def _detect_task_type(self, task_description: str) -> str:
        """Auto-detect task type from description"""
        description_lower = task_description.lower()

        # Keywords for exploration tasks
        explore_keywords = ["explore", "find", "analyze", "investigate", "map", "discover", "identify"]
        if any(keyword in description_lower for keyword in explore_keywords):
            return "explore"

        # Keywords for planning tasks
        plan_keywords = ["plan", "design", "strategy", "implement", "architecture", "roadmap"]
        if any(keyword in description_lower for keyword in plan_keywords):
            return "plan"

        # Default to execution
        return "execute"

    def execute_workflow(self, workflow_id: str) -> Dict:
        """Execute a registered autonomous workflow"""
        workflow = self.autonomous_workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_id}")

        if not workflow["enabled"]:
            logger.warning(f"Workflow {workflow_id} is disabled")
            return {"status": "skipped", "reason": "workflow_disabled"}

        logger.info(f"Executing workflow: {workflow['name']}")

        # Delegate to appropriate subagent
        result = self.delegate_to_subagent(
            task_description=workflow["task_template"],
            task_type=self._subagent_type_to_task_type(workflow["subagent_type"])
        )

        # Update workflow metadata
        workflow["last_run"] = datetime.now().isoformat()
        workflow["execution_count"] += 1

        logger.info(f"Workflow {workflow_id} executed successfully")

        return {
            "workflow_id": workflow_id,
            "workflow_name": workflow["name"],
            "execution_time": workflow["last_run"],
            "execution_count": workflow["execution_count"],
            "task_details": result
        }

    def _subagent_type_to_task_type(self, subagent_type: str) -> str:
        """Convert subagent type to task type"""
        mapping = {
            "Explore": "explore",
            "Plan": "plan",
            "general-purpose": "execute"
        }
        return mapping.get(subagent_type, "execute")

    def run_scheduled_workflows(self):
        """Run all scheduled workflows (would be called by scheduler)"""
        logger.info("Checking scheduled workflows...")

        executed = []
        for workflow_id, workflow in self.autonomous_workflows.items():
            if workflow["enabled"] and self._should_run_now(workflow):
                try:
                    result = self.execute_workflow(workflow_id)
                    executed.append(result)
                except Exception as e:
                    logger.error(f"Error executing workflow {workflow_id}: {e}")

        logger.info(f"Executed {len(executed)} scheduled workflows")
        return executed

    def _should_run_now(self, workflow: Dict) -> bool:
        """Check if workflow should run now (simplified logic)"""
        # This is a simplified version
        # In production, implement proper cron-like scheduling
        schedule = workflow["schedule"]

        # For demo purposes, return False (manual triggering only)
        return False

    def get_system_overview(self) -> Dict:
        """Get complete system overview"""
        subagent_status = self.subagent_bridge.get_system_status()

        workflow_summary = {
            "total_workflows": len(self.autonomous_workflows),
            "enabled_workflows": len([w for w in self.autonomous_workflows.values() if w["enabled"]]),
            "total_executions": sum(w["execution_count"] for w in self.autonomous_workflows.values())
        }

        return {
            "timestamp": datetime.now().isoformat(),
            "erpnext_url": self.erpnext_base_url,
            "subagent_employees": subagent_status["employees"],
            "tasks": subagent_status["tasks"],
            "workflows": workflow_summary,
            "workflows_detail": list(self.autonomous_workflows.values())
        }

    def create_custom_workflow(
        self,
        workflow_id: str,
        name: str,
        description: str,
        task_description: str,
        task_type: str = "execute",
        schedule: str = "manual"
    ):
        """Create a custom workflow"""
        subagent_type_mapping = {
            "explore": "Explore",
            "plan": "Plan",
            "execute": "general-purpose"
        }

        self.register_workflow(
            workflow_id=workflow_id,
            name=name,
            description=description,
            schedule=schedule,
            subagent_type=subagent_type_mapping.get(task_type, "general-purpose"),
            task_template=task_description
        )

        logger.info(f"Custom workflow created: {name}")


# Example usage and testing
if __name__ == "__main__":
    print("\n" + "="*70)
    print("ENHANCED AUTONOMOUS ORCHESTRATOR")
    print("="*70 + "\n")

    # Initialize
    orchestrator = EnhancedAutonomousOrchestrator(
        erpnext_base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    )

    # Example 1: Manual task delegation
    print("EXAMPLE 1: Manual Task Delegation")
    print("-" * 70)

    task1 = orchestrator.delegate_to_subagent(
        task_description="Explore all custom fields in the Customer doctype",
        task_type="explore"
    )

    print(f"Task delegated to: {task1['employee_name']}")
    print(f"Role: {task1['employee_role']}")
    print(f"Task ID: {task1['task_id']}")
    print()

    # Example 2: Execute a workflow
    print("EXAMPLE 2: Execute Autonomous Workflow")
    print("-" * 70)

    result = orchestrator.execute_workflow("daily_health_check")
    print(f"Workflow: {result['workflow_name']}")
    print(f"Executed: {result['execution_time']}")
    print(f"Total executions: {result['execution_count']}")
    print()

    # Example 3: Create custom workflow
    print("EXAMPLE 3: Create Custom Workflow")
    print("-" * 70)

    orchestrator.create_custom_workflow(
        workflow_id="inventory_restock",
        name="Automated Inventory Restocking",
        description="Check inventory levels and create purchase requests",
        task_description="""
        Check all warehouses for items below reorder level.
        Generate purchase requests for items that need restocking.
        Email purchase requests to procurement team.
        """,
        task_type="execute",
        schedule="daily_8am"
    )

    print("Custom workflow created: Automated Inventory Restocking")
    print()

    # Example 4: System overview
    print("EXAMPLE 4: System Overview")
    print("-" * 70)

    overview = orchestrator.get_system_overview()
    print(json.dumps(overview, indent=2))
