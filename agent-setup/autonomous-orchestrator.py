"""
Autonomous Orchestrator - Zero Human Intervention System
Coordinates all autonomous systems for fully automated operations
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import threading
from dataclasses import dataclass

from agent_orchestrator import ERPNextClient, AgentOrchestrator
from email_integration import EmailManager, ERPNextEmailIntegration
from autonomous_workflow import AutonomousWorkflowEngine, AutonomousWorkflow, WorkflowStep, TriggerType
from self_healing_system import SelfHealingSystem, HealthCheck, AutoFixAction, IssueSeverity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AutonomousSystemConfig:
    """Configuration for autonomous system"""
    erpnext_url: str
    erpnext_api_key: str
    erpnext_api_secret: str
    email_smtp_server: str
    email_smtp_port: int
    email_username: str
    email_password: str
    claude_api_key: str
    enable_workflows: bool = True
    enable_self_healing: bool = True
    enable_email_processing: bool = True
    enable_auto_agents: bool = True


class AutonomousOrchestrator:
    """Main orchestrator for zero-human-intervention system"""

    def __init__(self, config: AutonomousSystemConfig):
        self.config = config

        # Initialize core components
        self.erpnext = ERPNextClient(
            base_url=config.erpnext_url,
            api_key=config.erpnext_api_key,
            api_secret=config.erpnext_api_secret
        )

        self.email_manager = EmailManager(
            smtp_server=config.email_smtp_server,
            smtp_port=config.email_smtp_port,
            smtp_username=config.email_username,
            smtp_password=config.email_password
        )

        self.email_integration = ERPNextEmailIntegration(self.erpnext, self.email_manager)

        self.orchestrator = AgentOrchestrator(self.erpnext, max_agents=20)

        # Initialize autonomous systems
        self.workflow_engine = AutonomousWorkflowEngine(
            self.erpnext,
            self.email_manager,
            self.orchestrator
        )

        self.self_healing = SelfHealingSystem(self.erpnext)

        # System status
        self.running = False
        self.start_time: Optional[datetime] = None

        # Initialize default autonomous workflows
        self._initialize_default_workflows()

    def _initialize_default_workflows(self):
        """Initialize default autonomous workflows"""

        # 1. Auto-process incoming emails workflow
        email_workflow = AutonomousWorkflow(
            workflow_id="auto_process_emails",
            name="Auto-Process Incoming Emails",
            description="Automatically process incoming emails and create leads",
            trigger_type=TriggerType.SCHEDULED,
            trigger_config={"schedule": {"type": "interval", "interval": 15}},  # Every 15 minutes
            steps=[
                WorkflowStep(
                    step_id="read_emails",
                    name="Read Incoming Emails",
                    action_type="process_incoming_emails",
                    action_config={}
                ),
                WorkflowStep(
                    step_id="create_leads",
                    name="Create Leads from Emails",
                    action_type="create_lead_from_email",
                    action_config={},
                    depends_on=["read_emails"]
                )
            ],
            enabled=True
        )
        self.workflow_engine.register_workflow(email_workflow)

        # 2. Auto-send quotation workflow
        quotation_workflow = AutonomousWorkflow(
            workflow_id="auto_send_quotation",
            name="Auto-Send Quotations",
            description="Automatically send quotations to customers",
            trigger_type=TriggerType.EVENT,
            trigger_config={"event": "quotation_created"},
            steps=[
                WorkflowStep(
                    step_id="get_quotation",
                    name="Get Quotation Details",
                    action_type="erpnext_get",
                    action_config={
                        "resource_type": "Quotation",
                        "filters": {"status": "Submitted"}
                    }
                ),
                WorkflowStep(
                    step_id="send_quotation_email",
                    name="Send Quotation Email",
                    action_type="send_email",
                    action_config={
                        "to": "{{customer_email}}",
                        "subject": "Quotation: {{quotation_name}}",
                        "body": "Please find attached our quotation."
                    },
                    depends_on=["get_quotation"]
                )
            ],
            enabled=True
        )
        self.workflow_engine.register_workflow(quotation_workflow)

        # 3. Auto-send invoice workflow
        invoice_workflow = AutonomousWorkflow(
            workflow_id="auto_send_invoice",
            name="Auto-Send Invoices",
            description="Automatically send invoices to customers",
            trigger_type=TriggerType.EVENT,
            trigger_config={"event": "invoice_created"},
            steps=[
                WorkflowStep(
                    step_id="get_invoice",
                    name="Get Invoice Details",
                    action_type="erpnext_get",
                    action_config={
                        "resource_type": "Sales Invoice",
                        "filters": {"status": "Submitted"}
                    }
                ),
                WorkflowStep(
                    step_id="send_invoice_email",
                    name="Send Invoice Email",
                    action_type="send_email",
                    action_config={
                        "to": "{{customer_email}}",
                        "subject": "Invoice: {{invoice_name}}",
                        "body": "Please find attached invoice for payment."
                    },
                    depends_on=["get_invoice"]
                )
            ],
            enabled=True
        )
        self.workflow_engine.register_workflow(invoice_workflow)

        # 4. Auto-follow-up workflow
        followup_workflow = AutonomousWorkflow(
            workflow_id="auto_followup",
            name="Auto-Follow-up on Quotations",
            description="Automatically follow up on pending quotations",
            trigger_type=TriggerType.SCHEDULED,
            trigger_config={"schedule": {"type": "daily", "time": "09:00"}},
            steps=[
                WorkflowStep(
                    step_id="get_pending_quotations",
                    name="Get Pending Quotations",
                    action_type="erpnext_get",
                    action_config={
                        "resource_type": "Quotation",
                        "filters": {
                            "status": "Submitted",
                            "valid_till": ["<", "today"]
                        }
                    }
                ),
                WorkflowStep(
                    step_id="send_followup",
                    name="Send Follow-up Email",
                    action_type="send_notification",
                    action_config={
                        "recipient": "{{customer_email}}",
                        "notification_type": "custom",
                        "message": "We wanted to follow up on your quotation..."
                    },
                    depends_on=["get_pending_quotations"]
                )
            ],
            enabled=True
        )
        self.workflow_engine.register_workflow(followup_workflow)

    def start(self):
        """Start the autonomous system"""
        logger.info("="*60)
        logger.info("Starting Autonomous Workplace System")
        logger.info("Zero Human Intervention Mode")
        logger.info("="*60)

        self.running = True
        self.start_time = datetime.now()

        # Start workflow engine
        if self.config.enable_workflows:
            self.workflow_engine.start_scheduler()
            logger.info("✓ Workflow engine started")

        # Start self-healing system
        if self.config.enable_self_healing:
            self.self_healing.start_monitoring()
            logger.info("✓ Self-healing system started")

        # Start email processing
        if self.config.enable_email_processing:
            self._start_email_processor()
            logger.info("✓ Email processor started")

        # Start agent orchestrator
        if self.config.enable_auto_agents:
            self.orchestrator.start(num_workers=10)
            logger.info("✓ Agent orchestrator started")

        logger.info("="*60)
        logger.info("Autonomous system fully operational")
        logger.info("="*60)

    def _start_email_processor(self):
        """Start autonomous email processing"""
        def email_processor_loop():
            while self.running:
                try:
                    # Process incoming emails every 15 minutes
                    processed = self.email_integration.process_incoming_emails()
                    if processed:
                        logger.info(f"Processed {len(processed)} emails automatically")
                    asyncio.sleep(900)  # 15 minutes
                except Exception as e:
                    logger.error(f"Error in email processor: {str(e)}")
                    asyncio.sleep(60)

        email_thread = threading.Thread(target=email_processor_loop, daemon=True)
        email_thread.start()

    def stop(self):
        """Stop the autonomous system"""
        logger.info("Stopping autonomous system...")
        self.running = False
        self.workflow_engine.running = False
        self.self_healing.running = False
        logger.info("Autonomous system stopped")

    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0

        return {
            "status": "running" if self.running else "stopped",
            "uptime_seconds": uptime,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "workflows": {
                "enabled": self.config.enable_workflows,
                "total": len(self.workflow_engine.workflows),
                "running": len(self.workflow_engine.running_workflows)
            },
            "self_healing": {
                "enabled": self.config.enable_self_healing,
                "health": self.self_healing.get_system_health() if self.config.enable_self_healing else None
            },
            "email_processing": {
                "enabled": self.config.enable_email_processing
            },
            "agents": {
                "enabled": self.config.enable_auto_agents,
                "total": len(self.orchestrator.agents),
                "active": sum(1 for agent in self.orchestrator.agents.values() if agent.status == "busy")
            }
        }

    def trigger_workflow(self, workflow_id: str, trigger_data: Optional[Dict] = None):
        """Trigger a workflow manually"""
        self.workflow_engine.trigger_workflow(workflow_id, trigger_data)

    def register_custom_workflow(self, workflow: AutonomousWorkflow):
        """Register a custom autonomous workflow"""
        self.workflow_engine.register_workflow(workflow)
        logger.info(f"Custom workflow registered: {workflow.name}")


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    config = AutonomousSystemConfig(
        erpnext_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000"),
        erpnext_api_key=os.getenv("ERPNEXT_API_KEY"),
        erpnext_api_secret=os.getenv("ERPNEXT_API_SECRET"),
        email_smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        email_smtp_port=int(os.getenv("SMTP_PORT", "587")),
        email_username=os.getenv("SMTP_USERNAME"),
        email_password=os.getenv("SMTP_PASSWORD"),
        claude_api_key=os.getenv("CLAUDE_API_KEY"),
        enable_workflows=True,
        enable_self_healing=True,
        enable_email_processing=True,
        enable_auto_agents=True
    )

    orchestrator = AutonomousOrchestrator(config)
    orchestrator.start()

    # Keep running
    try:
        while True:
            status = orchestrator.get_system_status()
            print(f"\nSystem Status: {status['status']}")
            print(f"Uptime: {status['uptime_seconds']} seconds")
            asyncio.sleep(60)
    except KeyboardInterrupt:
        orchestrator.stop()
