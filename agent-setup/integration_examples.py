"""
Integration Examples
Examples for integrating with ERPNext, payment gateways, and webhooks
"""

import os
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_erpnext_integration():
    """Example: Connect tenant to ERPNext"""
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    from erpnext_tenant_integration import ERPNextTenantIntegration
    
    manager = TenantManager()
    tenant_isolation = TenantIsolation(manager)
    erpnext_integration = ERPNextTenantIntegration(tenant_isolation)
    
    tenant = manager.get_tenant_by_subdomain("mycompany")
    
    # Configure ERPNext connection
    success = erpnext_integration.configure_erpnext(
        tenant_id=tenant.tenant_id,
        base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000"),
        api_key=os.getenv("ERPNEXT_API_KEY"),
        api_secret=os.getenv("ERPNEXT_API_SECRET"),
        site_name="your_site"
    )
    
    if success:
        logger.info("ERPNext configured successfully")
        
        # Test connection
        result = erpnext_integration.test_connection(tenant.tenant_id)
        logger.info(f"Connection test: {result}")
    else:
        logger.error("ERPNext configuration failed")


def example_stripe_payment():
    """Example: Process payment with Stripe"""
    from tenant_manager import TenantManager
    from subscription_plans import SubscriptionPlanManager
    from usage_tracker import UsageTracker
    from billing_system import BillingSystem
    from payment_integration import PaymentIntegration
    
    manager = TenantManager()
    plan_manager = SubscriptionPlanManager()
    usage_tracker = UsageTracker(manager)
    billing = BillingSystem(manager, plan_manager, usage_tracker)
    
    # Initialize payment integration
    payment = PaymentIntegration(
        billing_system=billing,
        provider="stripe",
        stripe_secret_key=os.getenv("STRIPE_SECRET_KEY")
    )
    
    tenant = manager.get_tenant_by_subdomain("mycompany")
    
    # Generate invoice
    invoice = billing.generate_invoice(tenant.tenant_id)
    
    # Create payment intent
    intent = payment.create_payment_intent(invoice)
    
    if intent.get("provider") == "stripe":
        logger.info(f"Payment intent created: {intent['payment_intent_id']}")
        logger.info(f"Client secret: {intent['client_secret']}")
        # Use client_secret in frontend to complete payment
    else:
        logger.warning("Payment gateway not configured")


def example_webhook_handler():
    """Example: Handle ERPNext webhook"""
    from fastapi import FastAPI, Request
    from tenant_manager import TenantManager
    from event_bus import EventBus
    from tenant_isolation import TenantIsolation
    
    app = FastAPI()
    manager = TenantManager()
    tenant_isolation = TenantIsolation(manager)
    event_bus = EventBus(tenant_isolation)
    
    @app.post("/webhook/erpnext/{tenant_id}")
    async def handle_webhook(tenant_id: str, request: Request):
        """Handle ERPNext webhook"""
        data = await request.json()
        event_type = data.get("event")
        event_data = data.get("data", {})
        
        # Publish to event bus
        event_id = event_bus.publish_event(
            tenant_id=tenant_id,
            event_type=event_type,
            source="erpnext",
            data=event_data
        )
        
        return {
            "success": True,
            "event_id": event_id,
            "message": "Webhook processed"
        }
    
    return app


def example_workflow_trigger():
    """Example: Trigger workflow from event"""
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    from event_bus import EventBus
    from persistence_layer import PersistenceLayer
    
    manager = TenantManager()
    tenant_isolation = TenantIsolation(manager)
    event_bus = EventBus(tenant_isolation)
    persistence = PersistenceLayer(tenant_isolation)
    
    tenant = manager.get_tenant_by_subdomain("mycompany")
    
    # Subscribe to quotation_created event
    def handle_quotation_created(event):
        """Handle quotation created event"""
        logger.info(f"Quotation created: {event.data}")
        
        # Load workflows that listen to this event
        workflows = persistence.load_workflows(event.tenant_id)
        
        for workflow in workflows:
            if workflow.get("trigger_type") == "event":
                trigger_config = workflow.get("trigger_config", {})
                if trigger_config.get("event") == "quotation_created":
                    # Execute workflow
                    logger.info(f"Triggering workflow: {workflow['name']}")
                    # workflow_engine.execute_workflow(workflow['workflow_id'])
    
    event_bus.subscribe("quotation_created", handle_quotation_created)
    event_bus.start()
    
    # Publish test event
    event_bus.publish_event(
        tenant_id=tenant.tenant_id,
        event_type="quotation_created",
        source="erpnext",
        data={"quotation_id": "QUO-00001"}
    )


def example_agent_delegation_workflow():
    """Example: Agent delegation workflow"""
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    from employee_agent_system import EmployeeAgentSystem
    from agent_delegation import AgentDelegation
    
    manager = TenantManager()
    tenant_isolation = TenantIsolation(manager)
    agent_system = EmployeeAgentSystem(tenant_isolation)
    delegation = AgentDelegation(tenant_isolation, agent_system)
    
    tenant = manager.get_tenant_by_subdomain("mycompany")
    
    # Get agents
    agents = agent_system.list_agents(tenant.tenant_id)
    
    if len(agents) >= 2:
        from_agent = agents[0]
        to_agent = agents[1]
        
        # Delegate complex quotation task
        delegation_result = delegation.delegate_task(
            tenant_id=tenant.tenant_id,
            from_agent_id=from_agent.agent_id,
            to_agent_id=to_agent.agent_id,
            task_description="Create complex quotation for enterprise customer",
            task_type="erpnext_action",
            task_config={
                "action": "create_quotation",
                "customer": "Enterprise Corp",
                "items": [
                    {"item": "Product A", "qty": 100, "rate": 50.00}
                ],
                "priority": "high"
            },
            priority=8
        )
        
        logger.info(f"Task delegated: {delegation_result.delegation_id}")
        
        # Accept delegation
        delegation.accept_delegation(
            tenant.tenant_id,
            delegation_result.delegation_id,
            to_agent.agent_id
        )
        
        # Complete delegation
        delegation.complete_delegation(
            tenant.tenant_id,
            delegation_result.delegation_id,
            {
                "quotation_id": "QUO-00001",
                "status": "created",
                "total": 5000.00
            },
            "Quotation created successfully"
        )


def example_ksa_payment():
    """Example: Process KSA payment (Mada, bank transfer)"""
    from tenant_manager import TenantManager
    from subscription_plans import SubscriptionPlanManager
    from usage_tracker import UsageTracker
    from billing_system import BillingSystem
    from payment_integration import PaymentIntegration
    
    manager = TenantManager()
    plan_manager = SubscriptionPlanManager()
    usage_tracker = UsageTracker(manager)
    billing = BillingSystem(manager, plan_manager, usage_tracker)
    
    payment = PaymentIntegration(billing_system=billing, provider="ksa_local")
    
    tenant = manager.get_tenant_by_subdomain("mycompany")
    invoice = billing.generate_invoice(tenant.tenant_id)
    
    # Process KSA payment
    result = payment.process_ksa_payment(
        invoice=invoice,
        payment_method="mada",
        transaction_id="TXN123456"
    )
    
    logger.info(f"KSA payment processed: {result}")
    
    # Record payment manually (after verification)
    billing.record_payment(
        invoice_id=invoice.invoice_id,
        amount=invoice.amount,
        payment_method="mada",
        payment_provider_id="TXN123456"
    )


if __name__ == "__main__":
    logger.info("Integration Examples")
    logger.info("=" * 80)
    
    # Uncomment to run examples:
    # example_erpnext_integration()
    # example_stripe_payment()
    # example_workflow_trigger()
    # example_agent_delegation_workflow()
    # example_ksa_payment()
    
    logger.info("See function docstrings for usage examples")
