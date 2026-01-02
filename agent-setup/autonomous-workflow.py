"""
Autonomous Workflow Automation System
Zero human intervention - fully automated business processes
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import threading
from queue import Queue
import time

from agent_orchestrator import ERPNextClient, AgentOrchestrator
from email_integration import EmailManager, ERPNextEmailIntegration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    PAUSED = "paused"


class TriggerType(Enum):
    SCHEDULED = "scheduled"
    EVENT = "event"
    CONDITION = "condition"
    WEBHOOK = "webhook"
    EMAIL = "email"
    API = "api"


@dataclass
class WorkflowStep:
    """Represents a step in an autonomous workflow"""
    step_id: str
    name: str
    action_type: str  # erpnext_action, email, notification, decision, etc.
    action_config: Dict[str, Any]
    conditions: Optional[Dict[str, Any]] = None
    retry_count: int = 3
    retry_delay: int = 60
    timeout: int = 300
    on_success: Optional[List[str]] = None  # Next step IDs
    on_failure: Optional[List[str]] = None
    depends_on: Optional[List[str]] = None


@dataclass
class AutonomousWorkflow:
    """Autonomous workflow definition"""
    workflow_id: str
    name: str
    description: str
    trigger_type: TriggerType
    trigger_config: Dict[str, Any]
    steps: List[WorkflowStep]
    enabled: bool = True
    max_concurrent: int = 1
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    last_run: Optional[datetime] = None
    run_count: int = 0
    success_count: int = 0
    failure_count: int = 0


class AutonomousWorkflowEngine:
    """Engine for executing autonomous workflows"""

    def __init__(
        self,
        erpnext_client: ERPNextClient,
        email_manager: EmailManager,
        orchestrator: AgentOrchestrator
    ):
        self.erpnext = erpnext_client
        self.email_manager = email_manager
        self.orchestrator = orchestrator
        self.workflows: Dict[str, AutonomousWorkflow] = {}
        self.running_workflows: Dict[str, Dict] = {}
        self.workflow_queue = Queue()
        self.running = False
        self.lock = threading.Lock()

        # Initialize email integration
        self.email_integration = ERPNextEmailIntegration(erpnext_client, email_manager)

    def register_workflow(self, workflow: AutonomousWorkflow):
        """Register a workflow"""
        with self.lock:
            self.workflows[workflow.workflow_id] = workflow
            logger.info(f"Workflow registered: {workflow.name} ({workflow.workflow_id})")

    def execute_step(self, step: WorkflowStep, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow step"""
        try:
            logger.info(f"Executing step: {step.name} ({step.step_id})")

            # Check conditions
            if step.conditions:
                if not self._evaluate_conditions(step.conditions, context):
                    return {"success": False, "skipped": True, "reason": "Conditions not met"}

            # Execute based on action type
            if step.action_type == "erpnext_create":
                result = self._execute_erpnext_create(step.action_config, context)
            elif step.action_type == "erpnext_update":
                result = self._execute_erpnext_update(step.action_config, context)
            elif step.action_type == "erpnext_get":
                result = self._execute_erpnext_get(step.action_config, context)
            elif step.action_type == "send_email":
                result = self._execute_send_email(step.action_config, context)
            elif step.action_type == "send_notification":
                result = self._execute_send_notification(step.action_config, context)
            elif step.action_type == "decision":
                result = self._execute_decision(step.action_config, context)
            elif step.action_type == "wait":
                result = self._execute_wait(step.action_config, context)
            elif step.action_type == "process_incoming_emails":
                result = self._execute_process_emails(step.action_config, context)
            elif step.action_type == "create_lead_from_email":
                result = self._execute_create_lead_from_email(step.action_config, context)
            else:
                result = {"success": False, "error": f"Unknown action type: {step.action_type}"}

            # Update context with result
            context[f"step_{step.step_id}_result"] = result
            return result

        except Exception as e:
            logger.error(f"Error executing step {step.step_id}: {str(e)}")
            return {"success": False, "error": str(e)}

    def _execute_erpnext_create(self, config: Dict, context: Dict) -> Dict:
        """Execute ERPNext create action"""
        resource_type = config.get("resource_type")
        data = self._resolve_template(config.get("data", {}), context)
        result = self.erpnext.post(resource_type, data)
        return {"success": True, "data": result}

    def _execute_erpnext_update(self, config: Dict, context: Dict) -> Dict:
        """Execute ERPNext update action"""
        resource_type = config.get("resource_type")
        name = self._resolve_template(config.get("name"), context)
        data = self._resolve_template(config.get("data", {}), context)
        result = self.erpnext.put(resource_type, name, data)
        return {"success": True, "data": result}

    def _execute_erpnext_get(self, config: Dict, context: Dict) -> Dict:
        """Execute ERPNext get action"""
        resource_type = config.get("resource_type")
        filters = self._resolve_template(config.get("filters", {}), context)
        fields = config.get("fields")
        result = self.erpnext.get(resource_type, filters=filters, fields=fields)
        context[f"{resource_type}_data"] = result.get("data", [])
        return {"success": True, "data": result}

    def _execute_send_email(self, config: Dict, context: Dict) -> Dict:
        """Execute send email action"""
        to = self._resolve_template(config.get("to"), context)
        subject = self._resolve_template(config.get("subject"), context)
        body = self._resolve_template(config.get("body"), context)
        result = self.email_manager.send_email(to, subject, body, html=config.get("html", False))
        return result

    def _execute_send_notification(self, config: Dict, context: Dict) -> Dict:
        """Execute send notification action"""
        recipient = self._resolve_template(config.get("recipient"), context)
        notification_type = config.get("notification_type", "custom")
        message = self._resolve_template(config.get("message"), context)
        result = self.email_integration.send_notification_email(
            recipient, notification_type, message,
            config.get("reference_doctype"), config.get("reference_name")
        )
        return result

    def _execute_decision(self, config: Dict, context: Dict) -> Dict:
        """Execute decision step"""
        condition = config.get("condition")
        if self._evaluate_condition(condition, context):
            return {"success": True, "decision": "true", "next_step": config.get("on_true")}
        else:
            return {"success": True, "decision": "false", "next_step": config.get("on_false")}

    def _execute_wait(self, config: Dict, context: Dict) -> Dict:
        """Execute wait step"""
        duration = config.get("duration", 60)
        time.sleep(duration)
        return {"success": True, "waited": duration}

    def _execute_process_emails(self, config: Dict, context: Dict) -> Dict:
        """Process incoming emails"""
        processed = self.email_integration.process_incoming_emails()
        context["processed_emails"] = processed
        return {"success": True, "processed": processed}

    def _execute_create_lead_from_email(self, config: Dict, context: Dict) -> Dict:
        """Create lead from email data"""
        email_data = context.get("email_data", {})
        lead_data = {
            "lead_name": email_data.get("from", "Unknown").split("@")[0],
            "email_id": email_data.get("from"),
            "source": "Email",
            "status": "Open"
        }
        result = self.erpnext.post("Lead", lead_data)
        return {"success": True, "data": result}

    def _resolve_template(self, template: Any, context: Dict) -> Any:
        """Resolve template variables in context"""
        if isinstance(template, str):
            # Simple template resolution: {{variable}}
            for key, value in context.items():
                template = template.replace(f"{{{{{key}}}}}", str(value))
            return template
        elif isinstance(template, dict):
            return {k: self._resolve_template(v, context) for k, v in template.items()}
        elif isinstance(template, list):
            return [self._resolve_template(item, context) for item in template]
        return template

    def _evaluate_conditions(self, conditions: Dict, context: Dict) -> bool:
        """Evaluate workflow conditions"""
        # Simple condition evaluation
        # Supports: field == value, field != value, field > value, etc.
        for condition in conditions.get("all", []):
            if not self._evaluate_condition(condition, context):
                return False
        return True

    def _evaluate_condition(self, condition: Dict, context: Dict) -> bool:
        """Evaluate a single condition"""
        field = condition.get("field")
        operator = condition.get("operator", "==")
        value = condition.get("value")

        field_value = context.get(field)

        if operator == "==":
            return field_value == value
        elif operator == "!=":
            return field_value != value
        elif operator == ">":
            return field_value > value
        elif operator == "<":
            return field_value < value
        elif operator == "in":
            return field_value in value
        elif operator == "not_in":
            return field_value not in value
        return False

    async def execute_workflow(self, workflow_id: str, trigger_data: Optional[Dict] = None):
        """Execute a workflow"""
        workflow = self.workflows.get(workflow_id)
        if not workflow or not workflow.enabled:
            logger.warning(f"Workflow {workflow_id} not found or disabled")
            return

        if workflow.max_concurrent > 1:
            # Check concurrent execution limit
            running = sum(1 for w in self.running_workflows.values() if w.get("workflow_id") == workflow_id)
            if running >= workflow.max_concurrent:
                logger.warning(f"Workflow {workflow_id} already running (max concurrent: {workflow.max_concurrent})")
                return

        # Initialize context
        context = {
            "workflow_id": workflow_id,
            "trigger_data": trigger_data or {},
            "started_at": datetime.now().isoformat()
        }

        # Mark as running
        execution_id = f"{workflow_id}_{datetime.now().timestamp()}"
        self.running_workflows[execution_id] = {
            "workflow_id": workflow_id,
            "status": "running",
            "started_at": datetime.now(),
            "context": context
        }

        workflow.status = WorkflowStatus.RUNNING
        workflow.last_run = datetime.now()
        workflow.run_count += 1

        try:
            # Execute steps
            executed_steps = set()
            current_step_ids = [step.step_id for step in workflow.steps if not step.depends_on]

            while current_step_ids:
                step_id = current_step_ids.pop(0)
                if step_id in executed_steps:
                    continue

                step = next((s for s in workflow.steps if s.step_id == step_id), None)
                if not step:
                    continue

                # Check dependencies
                if step.depends_on:
                    if not all(dep in executed_steps for dep in step.depends_on):
                        current_step_ids.append(step_id)  # Retry later
                        continue

                # Execute step
                result = self.execute_step(step, context)
                executed_steps.add(step_id)

                # Determine next steps
                if result.get("success"):
                    if step.on_success:
                        current_step_ids.extend(step.on_success)
                else:
                    # Retry logic
                    retry_count = context.get(f"{step_id}_retry_count", 0)
                    if retry_count < step.retry_count:
                        context[f"{step_id}_retry_count"] = retry_count + 1
                        await asyncio.sleep(step.retry_delay)
                        current_step_ids.append(step_id)
                    else:
                        if step.on_failure:
                            current_step_ids.extend(step.on_failure)
                        else:
                            workflow.status = WorkflowStatus.FAILED
                            workflow.failure_count += 1
                            break

            if workflow.status != WorkflowStatus.FAILED:
                workflow.status = WorkflowStatus.COMPLETED
                workflow.success_count += 1

        except Exception as e:
            logger.error(f"Error executing workflow {workflow_id}: {str(e)}")
            workflow.status = WorkflowStatus.FAILED
            workflow.failure_count += 1

        finally:
            # Cleanup
            self.running_workflows.pop(execution_id, None)
            context["completed_at"] = datetime.now().isoformat()

    def start_scheduler(self):
        """Start the workflow scheduler"""
        self.running = True
        scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        scheduler_thread.start()
        logger.info("Workflow scheduler started")

    def _scheduler_loop(self):
        """Scheduler loop for scheduled workflows"""
        while self.running:
            try:
                current_time = datetime.now()

                for workflow in self.workflows.values():
                    if not workflow.enabled:
                        continue

                    if workflow.trigger_type == TriggerType.SCHEDULED:
                        schedule = workflow.trigger_config.get("schedule")
                        if self._should_run_schedule(schedule, workflow.last_run):
                            asyncio.run(self.execute_workflow(workflow.workflow_id))

                    elif workflow.trigger_type == TriggerType.EVENT:
                        # Event-driven workflows are triggered externally
                        pass

                time.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
                time.sleep(60)

    def _should_run_schedule(self, schedule: Dict, last_run: Optional[datetime]) -> bool:
        """Check if schedule should run"""
        if not last_run:
            return True

        schedule_type = schedule.get("type")
        interval = schedule.get("interval", 60)  # minutes

        if schedule_type == "interval":
            return (datetime.now() - last_run).total_seconds() >= (interval * 60)
        elif schedule_type == "daily":
            return datetime.now().date() > last_run.date()
        elif schedule_type == "hourly":
            return (datetime.now() - last_run).total_seconds() >= 3600
        return False

    def trigger_workflow(self, workflow_id: str, trigger_data: Optional[Dict] = None):
        """Manually trigger a workflow"""
        asyncio.run(self.execute_workflow(workflow_id, trigger_data))

    def get_workflow_status(self, workflow_id: str) -> Dict:
        """Get workflow status"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"error": "Workflow not found"}

        return {
            "workflow_id": workflow.workflow_id,
            "name": workflow.name,
            "status": workflow.status.value,
            "enabled": workflow.enabled,
            "last_run": workflow.last_run.isoformat() if workflow.last_run else None,
            "run_count": workflow.run_count,
            "success_count": workflow.success_count,
            "failure_count": workflow.failure_count
        }
