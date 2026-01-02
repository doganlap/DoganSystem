"""
Unified Integrated Orchestrator - Complete System Integration
Integrates multi-tenant, autonomous workflows, employee agents, KSA localization, and API gateway
"""

import asyncio
import logging
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import threading
from dataclasses import dataclass
from pathlib import Path

# Multi-tenant components
from tenant_manager import TenantManager, Tenant
from tenant_isolation import TenantIsolation
from tenant_provisioning import TenantProvisioner

# Employee agents
from employee_agent_system import EmployeeAgentSystem, EmployeeAgent
from agent_delegation import AgentDelegation
from agent_teams import AgentTeams
from agent_hierarchy import AgentHierarchy

# KSA Localization
from ksa_localization import KSALocalizationManager, KSALocalization

# ERPNext integration
from erpnext_tenant_integration import ERPNextTenantIntegration
from agent_orchestrator import ERPNextClient, AgentOrchestrator

# Autonomous systems
from autonomous_workflow import AutonomousWorkflowEngine, AutonomousWorkflow, WorkflowStep, TriggerType
from self_healing_system import SelfHealingSystem
from email_integration import EmailManager, ERPNextEmailIntegration

# Monitoring and metrics
from metrics_collector import MetricsCollector
from usage_tracker import UsageTracker

# Persistence
from persistence_layer import PersistenceLayer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class UnifiedSystemConfig:
    """Configuration for unified integrated system"""
    # Platform settings
    platform_db_path: str = "platform.db"
    tenant_db_dir: str = "tenant_databases"
    
    # ERPNext defaults (can be overridden per tenant)
    default_erpnext_url: Optional[str] = None
    default_erpnext_api_key: Optional[str] = None
    default_erpnext_api_secret: Optional[str] = None
    
    # Email defaults
    default_email_smtp_server: Optional[str] = None
    default_email_smtp_port: int = 587
    default_email_username: Optional[str] = None
    default_email_password: Optional[str] = None
    
    # Claude AI
    claude_api_key: Optional[str] = None
    
    # System features
    enable_multi_tenant: bool = True
    enable_autonomous_workflows: bool = True
    enable_self_healing: bool = True
    enable_email_processing: bool = True
    enable_employee_agents: bool = True
    enable_ksa_localization: bool = True
    enable_monitoring: bool = True
    
    # Auto-provisioning
    auto_provision_new_tenants: bool = True
    default_subscription_tier: str = "starter"


class UnifiedOrchestrator:
    """Unified orchestrator integrating all system components"""
    
    def __init__(self, config: UnifiedSystemConfig):
        self.config = config
        
        # Initialize core managers
        logger.info("Initializing unified orchestrator...")
        
        # Multi-tenant foundation
        self.tenant_manager = TenantManager(config.platform_db_path)
        self.tenant_isolation = TenantIsolation(self.tenant_manager, config.tenant_db_dir)
        self.tenant_provisioner = TenantProvisioner(self.tenant_manager, self.tenant_isolation)
        
        # Employee agent system
        self.employee_agent_system = EmployeeAgentSystem(self.tenant_isolation)
        self.agent_delegation = AgentDelegation(self.tenant_isolation, self.employee_agent_system)
        self.agent_teams = AgentTeams(self.tenant_isolation, self.employee_agent_system)
        self.agent_hierarchy = AgentHierarchy(self.tenant_isolation, self.employee_agent_system)
        
        # KSA Localization
        self.ksa_localization = KSALocalizationManager(self.tenant_isolation)
        
        # ERPNext integration per tenant
        self.erpnext_integration = ERPNextTenantIntegration(self.tenant_isolation)
        
        # Persistence layer
        self.persistence = PersistenceLayer(self.tenant_isolation)
        
        # Monitoring
        self.metrics_collector = MetricsCollector(self.tenant_isolation)
        self.usage_tracker = UsageTracker(self.tenant_manager)
        
        # Per-tenant orchestrators
        self.tenant_orchestrators: Dict[str, 'TenantOrchestrator'] = {}
        
        # System status
        self.running = False
        self.start_time: Optional[datetime] = None
        
        logger.info("Unified orchestrator initialized")
    
    def get_or_create_tenant_orchestrator(self, tenant_id: str) -> 'TenantOrchestrator':
        """Get or create orchestrator for a specific tenant"""
        if tenant_id not in self.tenant_orchestrators:
            tenant = self.tenant_manager.get_tenant(tenant_id)
            if not tenant:
                raise ValueError(f"Tenant {tenant_id} not found")
            
            orchestrator = TenantOrchestrator(
                tenant=tenant,
                unified_orchestrator=self,
                config=self.config
            )
            self.tenant_orchestrators[tenant_id] = orchestrator
            orchestrator.initialize()
        
        return self.tenant_orchestrators[tenant_id]
    
    def start(self):
        """Start the unified system"""
        logger.info("="*60)
        logger.info("Starting Unified DoganSystem")
        logger.info("Multi-Tenant + Autonomous + Employee Agents + KSA")
        logger.info("="*60)
        
        self.running = True
        self.start_time = datetime.now()
        
        # Initialize all active tenants
        active_tenants = self.tenant_manager.list_tenants(status="active")
        logger.info(f"Found {len(active_tenants)} active tenants")
        
        for tenant in active_tenants:
            try:
                orchestrator = self.get_or_create_tenant_orchestrator(tenant.tenant_id)
                orchestrator.start()
                logger.info(f"✓ Started orchestrator for tenant: {tenant.name} ({tenant.tenant_id})")
            except Exception as e:
                logger.error(f"Error starting tenant {tenant.tenant_id}: {str(e)}")
        
        logger.info("="*60)
        logger.info("Unified system fully operational")
        logger.info("="*60)
    
    def stop(self):
        """Stop the unified system"""
        logger.info("Stopping unified system...")
        self.running = False
        
        for tenant_id, orchestrator in self.tenant_orchestrators.items():
            try:
                orchestrator.stop()
            except Exception as e:
                logger.error(f"Error stopping tenant {tenant_id}: {str(e)}")
        
        logger.info("Unified system stopped")
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        tenant_statuses = {}
        for tenant_id, orchestrator in self.tenant_orchestrators.items():
            tenant_statuses[tenant_id] = orchestrator.get_status()
        
        return {
            "status": "running" if self.running else "stopped",
            "uptime_seconds": uptime,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "tenants": {
                "total": len(self.tenant_orchestrators),
                "statuses": tenant_statuses
            },
            "features": {
                "multi_tenant": self.config.enable_multi_tenant,
                "autonomous_workflows": self.config.enable_autonomous_workflows,
                "self_healing": self.config.enable_self_healing,
                "email_processing": self.config.enable_email_processing,
                "employee_agents": self.config.enable_employee_agents,
                "ksa_localization": self.config.enable_ksa_localization,
                "monitoring": self.config.enable_monitoring
            }
        }


class TenantOrchestrator:
    """Orchestrator for a specific tenant"""
    
    def __init__(
        self,
        tenant: Tenant,
        unified_orchestrator: UnifiedOrchestrator,
        config: UnifiedSystemConfig
    ):
        self.tenant = tenant
        self.unified = unified_orchestrator
        self.config = config
        
        # Tenant-specific components
        self.erpnext_client: Optional[ERPNextClient] = None
        self.email_manager: Optional[EmailManager] = None
        self.email_integration: Optional[ERPNextEmailIntegration] = None
        self.agent_orchestrator: Optional[AgentOrchestrator] = None
        self.workflow_engine: Optional[AutonomousWorkflowEngine] = None
        self.self_healing: Optional[SelfHealingSystem] = None
        
        # KSA localization
        self.localization: Optional[KSALocalization] = None
        
        # Status
        self.running = False
        self.start_time: Optional[datetime] = None
    
    def initialize(self):
        """Initialize tenant-specific components"""
        logger.info(f"Initializing orchestrator for tenant: {self.tenant.name}")
        
        # Load KSA localization
        if self.config.enable_ksa_localization:
            self.localization = self.unified.ksa_localization.get_localization(self.tenant.tenant_id)
            logger.info(f"✓ KSA localization loaded: {self.localization.locale}, {self.localization.timezone}")
        
        # Initialize ERPNext client
        self.erpnext_client = self.unified.erpnext_integration.get_erpnext_client(self.tenant.tenant_id)
        if not self.erpnext_client:
            # Use defaults if tenant-specific config not found
            if self.config.default_erpnext_url:
                self.unified.erpnext_integration.configure_erpnext(
                    tenant_id=self.tenant.tenant_id,
                    base_url=self.config.default_erpnext_url,
                    api_key=self.config.default_erpnext_api_key or "",
                    api_secret=self.config.default_erpnext_api_secret or ""
                )
                self.erpnext_client = self.unified.erpnext_integration.get_erpnext_client(self.tenant.tenant_id)
        
        if not self.erpnext_client:
            logger.warning(f"ERPNext not configured for tenant {self.tenant.tenant_id}")
        else:
            logger.info(f"✓ ERPNext client initialized for tenant {self.tenant.tenant_id}")
        
        # Initialize email manager
        if self.config.enable_email_processing and self.config.default_email_smtp_server:
            self.email_manager = EmailManager(
                smtp_server=self.config.default_email_smtp_server,
                smtp_port=self.config.default_email_smtp_port,
                smtp_username=self.config.default_email_username or "",
                smtp_password=self.config.default_email_password or ""
            )
            
            if self.erpnext_client:
                self.email_integration = ERPNextEmailIntegration(self.erpnext_client, self.email_manager)
            logger.info(f"✓ Email manager initialized for tenant {self.tenant.tenant_id}")
        
        # Initialize agent orchestrator
        if self.config.enable_employee_agents and self.erpnext_client:
            self.agent_orchestrator = AgentOrchestrator(self.erpnext_client, max_agents=20)
            logger.info(f"✓ Agent orchestrator initialized for tenant {self.tenant.tenant_id}")
        
        # Initialize workflow engine
        if self.config.enable_autonomous_workflows and self.erpnext_client:
            self.workflow_engine = AutonomousWorkflowEngine(
                self.erpnext_client,
                self.email_manager,
                self.agent_orchestrator
            )
            self._initialize_tenant_workflows()
            logger.info(f"✓ Workflow engine initialized for tenant {self.tenant.tenant_id}")
        
        # Initialize self-healing
        if self.config.enable_self_healing and self.erpnext_client:
            self.self_healing = SelfHealingSystem(self.erpnext_client)
            logger.info(f"✓ Self-healing system initialized for tenant {self.tenant.tenant_id}")
    
    def _initialize_tenant_workflows(self):
        """Initialize workflows for this tenant with KSA context"""
        if not self.workflow_engine:
            return
        
        # Apply KSA localization to workflow schedules
        work_start = "09:00"  # Default, can be overridden by localization
        if self.localization:
            # KSA work week: Saturday-Wednesday
            # Adjust schedules based on KSA timezone
            pass
        
        # Email processing workflow
        email_workflow = AutonomousWorkflow(
            workflow_id=f"auto_process_emails_{self.tenant.tenant_id}",
            name="Auto-Process Incoming Emails",
            description="Automatically process incoming emails and create leads",
            trigger_type=TriggerType.SCHEDULED,
            trigger_config={"schedule": {"type": "interval", "interval": 15}},
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
        
        # Quotation workflow
        quotation_workflow = AutonomousWorkflow(
            workflow_id=f"auto_send_quotation_{self.tenant.tenant_id}",
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
        
        # Invoice workflow
        invoice_workflow = AutonomousWorkflow(
            workflow_id=f"auto_send_invoice_{self.tenant.tenant_id}",
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
        
        # Follow-up workflow (adjusted for KSA work week)
        followup_time = work_start
        followup_workflow = AutonomousWorkflow(
            workflow_id=f"auto_followup_{self.tenant.tenant_id}",
            name="Auto-Follow-up on Quotations",
            description="Automatically follow up on pending quotations",
            trigger_type=TriggerType.SCHEDULED,
            trigger_config={"schedule": {"type": "daily", "time": followup_time}},
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
        """Start tenant orchestrator"""
        logger.info(f"Starting orchestrator for tenant: {self.tenant.name}")
        
        self.running = True
        self.start_time = datetime.now()
        
        # Start workflow engine
        if self.workflow_engine and self.config.enable_autonomous_workflows:
            self.workflow_engine.start_scheduler()
            logger.info(f"  ✓ Workflow engine started")
        
        # Start self-healing
        if self.self_healing and self.config.enable_self_healing:
            self.self_healing.start_monitoring()
            logger.info(f"  ✓ Self-healing system started")
        
        # Start email processing
        if self.email_integration and self.config.enable_email_processing:
            self._start_email_processor()
            logger.info(f"  ✓ Email processor started")
        
        # Start agent orchestrator
        if self.agent_orchestrator and self.config.enable_employee_agents:
            self.agent_orchestrator.start(num_workers=10)
            logger.info(f"  ✓ Agent orchestrator started")
        
        logger.info(f"✓ Tenant orchestrator started: {self.tenant.name}")
    
    def _start_email_processor(self):
        """Start autonomous email processing for tenant"""
        def email_processor_loop():
            while self.running:
                try:
                    if self.email_integration:
                        processed = self.email_integration.process_incoming_emails()
                        if processed:
                            logger.info(f"[{self.tenant.name}] Processed {len(processed)} emails automatically")
                    asyncio.sleep(900)  # 15 minutes
                except Exception as e:
                    logger.error(f"[{self.tenant.name}] Error in email processor: {str(e)}")
                    asyncio.sleep(60)
        
        email_thread = threading.Thread(target=email_processor_loop, daemon=True)
        email_thread.start()
    
    def stop(self):
        """Stop tenant orchestrator"""
        logger.info(f"Stopping orchestrator for tenant: {self.tenant.name}")
        self.running = False
        
        if self.workflow_engine:
            self.workflow_engine.running = False
        
        if self.self_healing:
            self.self_healing.running = False
        
        logger.info(f"✓ Tenant orchestrator stopped: {self.tenant.name}")
    
    def get_status(self) -> Dict:
        """Get tenant orchestrator status"""
        uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        return {
            "tenant_id": self.tenant.tenant_id,
            "tenant_name": self.tenant.name,
            "status": "running" if self.running else "stopped",
            "uptime_seconds": uptime,
            "localization": {
                "locale": self.localization.locale if self.localization else None,
                "timezone": self.localization.timezone if self.localization else None,
                "currency": self.localization.currency if self.localization else None
            } if self.localization else None,
            "workflows": {
                "enabled": self.config.enable_autonomous_workflows,
                "total": len(self.workflow_engine.workflows) if self.workflow_engine else 0,
                "running": len(self.workflow_engine.running_workflows) if self.workflow_engine else 0
            },
            "agents": {
                "enabled": self.config.enable_employee_agents,
                "total": len(self.agent_orchestrator.agents) if self.agent_orchestrator else 0
            }
        }


# Main entry point
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    config = UnifiedSystemConfig(
        platform_db_path=os.getenv("PLATFORM_DB_PATH", "platform.db"),
        tenant_db_dir=os.getenv("TENANT_DB_DIR", "tenant_databases"),
        default_erpnext_url=os.getenv("ERPNEXT_BASE_URL"),
        default_erpnext_api_key=os.getenv("ERPNEXT_API_KEY"),
        default_erpnext_api_secret=os.getenv("ERPNEXT_API_SECRET"),
        default_email_smtp_server=os.getenv("SMTP_SERVER"),
        default_email_smtp_port=int(os.getenv("SMTP_PORT", "587")),
        default_email_username=os.getenv("SMTP_USERNAME"),
        default_email_password=os.getenv("SMTP_PASSWORD"),
        claude_api_key=os.getenv("CLAUDE_API_KEY"),
        enable_multi_tenant=True,
        enable_autonomous_workflows=True,
        enable_self_healing=True,
        enable_email_processing=True,
        enable_employee_agents=True,
        enable_ksa_localization=True,
        enable_monitoring=True
    )
    
    orchestrator = UnifiedOrchestrator(config)
    orchestrator.start()
    
    # Keep running
    try:
        while True:
            status = orchestrator.get_system_status()
            print(f"\nSystem Status: {status['status']}")
            print(f"Uptime: {status['uptime_seconds']} seconds")
            print(f"Active Tenants: {status['tenants']['total']}")
            asyncio.sleep(60)
    except KeyboardInterrupt:
        orchestrator.stop()
