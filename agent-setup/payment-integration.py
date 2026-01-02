"""
Payment Integration - Payment gateway integration for SaaS platform
Supports Stripe, PayPal, and KSA payment methods (Mada)
"""

import os
import logging
from typing import Dict, Optional, Any
from datetime import datetime
from decimal import Decimal

try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None

from billing_system import BillingSystem, Invoice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PaymentIntegration:
    """Payment gateway integration"""
    
    def __init__(
        self,
        billing_system: BillingSystem,
        provider: str = "stripe",
        stripe_secret_key: Optional[str] = None
    ):
        self.billing_system = billing_system
        self.provider = provider
        
        if provider == "stripe" and STRIPE_AVAILABLE:
            stripe.api_key = stripe_secret_key or os.getenv("STRIPE_SECRET_KEY")
            if not stripe.api_key:
                logger.warning("Stripe secret key not configured")
        elif provider == "stripe" and not STRIPE_AVAILABLE:
            logger.warning("Stripe library not installed. Install with: pip install stripe")
    
    def create_payment_intent(
        self,
        invoice: Invoice,
        payment_method: Optional[str] = None,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create payment intent for invoice"""
        if self.provider == "stripe" and STRIPE_AVAILABLE:
            return self._create_stripe_payment_intent(invoice, payment_method, customer_id)
        else:
            # Fallback: return payment details for manual processing
            return {
                "provider": self.provider,
                "invoice_id": invoice.invoice_id,
                "amount": float(invoice.amount),
                "currency": invoice.currency,
                "status": "pending",
                "payment_method": "manual",
                "message": "Payment gateway not configured. Please process manually."
            }
    
    def _create_stripe_payment_intent(
        self,
        invoice: Invoice,
        payment_method: Optional[str],
        customer_id: Optional[str]
    ) -> Dict[str, Any]:
        """Create Stripe payment intent"""
        try:
            # Convert amount to cents
            amount_cents = int(float(invoice.amount) * 100)
            
            intent_params = {
                "amount": amount_cents,
                "currency": invoice.currency.lower(),
                "metadata": {
                    "invoice_id": invoice.invoice_id,
                    "tenant_id": invoice.tenant_id,
                    "invoice_number": invoice.invoice_number
                }
            }
            
            if customer_id:
                intent_params["customer"] = customer_id
            
            if payment_method:
                intent_params["payment_method"] = payment_method
                intent_params["confirmation_method"] = "manual"
                intent_params["confirm"] = True
            
            intent = stripe.PaymentIntent.create(**intent_params)
            
            return {
                "provider": "stripe",
                "payment_intent_id": intent.id,
                "client_secret": intent.client_secret,
                "status": intent.status,
                "amount": float(invoice.amount),
                "currency": invoice.currency
            }
        except Exception as e:
            logger.error(f"Error creating Stripe payment intent: {str(e)}")
            raise
    
    def confirm_payment(
        self,
        payment_intent_id: str,
        invoice_id: str
    ) -> Dict[str, Any]:
        """Confirm payment after customer payment"""
        if self.provider == "stripe" and STRIPE_AVAILABLE:
            try:
                intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                
                if intent.status == "succeeded":
                    # Record payment in billing system
                    payment = self.billing_system.record_payment(
                        invoice_id=invoice_id,
                        amount=Decimal(str(intent.amount / 100)),
                        payment_method="stripe",
                        payment_provider_id=payment_intent_id,
                        transaction_date=datetime.fromtimestamp(intent.created)
                    )
                    
                    return {
                        "success": True,
                        "payment_id": payment["payment_id"],
                        "status": "completed"
                    }
                else:
                    return {
                        "success": False,
                        "status": intent.status,
                        "message": f"Payment not succeeded. Status: {intent.status}"
                    }
            except Exception as e:
                logger.error(f"Error confirming payment: {str(e)}")
                return {
                    "success": False,
                    "error": str(e)
                }
        else:
            return {
                "success": False,
                "error": "Payment provider not configured"
            }
    
    def create_customer(
        self,
        tenant_id: str,
        email: str,
        name: str,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Create customer in payment provider"""
        if self.provider == "stripe" and STRIPE_AVAILABLE:
            try:
                customer = stripe.Customer.create(
                    email=email,
                    name=name,
                    metadata={
                        "tenant_id": tenant_id,
                        **(metadata or {})
                    }
                )
                
                return {
                    "provider": "stripe",
                    "customer_id": customer.id,
                    "email": customer.email
                }
            except Exception as e:
                logger.error(f"Error creating customer: {str(e)}")
                raise
        else:
            return {
                "provider": self.provider,
                "customer_id": None,
                "message": "Customer creation not supported for this provider"
            }
    
    def create_subscription(
        self,
        customer_id: str,
        plan_id: str,
        billing_cycle: str = "monthly"
    ) -> Dict[str, Any]:
        """Create subscription in payment provider"""
        if self.provider == "stripe" and STRIPE_AVAILABLE:
            try:
                # Map plan to Stripe price ID (would be configured)
                price_id_map = {
                    "starter_monthly": os.getenv("STRIPE_STARTER_MONTHLY_PRICE_ID"),
                    "starter_yearly": os.getenv("STRIPE_STARTER_YEARLY_PRICE_ID"),
                    "professional_monthly": os.getenv("STRIPE_PROFESSIONAL_MONTHLY_PRICE_ID"),
                    "professional_yearly": os.getenv("STRIPE_PROFESSIONAL_YEARLY_PRICE_ID"),
                    "enterprise_monthly": os.getenv("STRIPE_ENTERPRISE_MONTHLY_PRICE_ID"),
                    "enterprise_yearly": os.getenv("STRIPE_ENTERPRISE_YEARLY_PRICE_ID"),
                }
                
                price_key = f"{plan_id}_{billing_cycle}"
                price_id = price_id_map.get(price_key)
                
                if not price_id:
                    logger.warning(f"Stripe price ID not configured for {price_key}")
                    return {
                        "success": False,
                        "error": f"Price ID not configured for {price_key}"
                    }
                
                subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=[{"price": price_id}],
                    metadata={
                        "plan_id": plan_id,
                        "billing_cycle": billing_cycle
                    }
                )
                
                return {
                    "provider": "stripe",
                    "subscription_id": subscription.id,
                    "status": subscription.status,
                    "current_period_end": datetime.fromtimestamp(subscription.current_period_end).isoformat()
                }
            except Exception as e:
                logger.error(f"Error creating subscription: {str(e)}")
                raise
        else:
            return {
                "provider": self.provider,
                "subscription_id": None,
                "message": "Subscription creation not supported for this provider"
            }
    
    def handle_webhook(self, payload: bytes, signature: str) -> Dict[str, Any]:
        """Handle payment webhook from provider"""
        if self.provider == "stripe" and STRIPE_AVAILABLE:
            try:
                webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
                if not webhook_secret:
                    logger.warning("Stripe webhook secret not configured")
                    return {"error": "Webhook secret not configured"}
                
                event = stripe.Webhook.construct_event(
                    payload, signature, webhook_secret
                )
                
                # Handle different event types
                if event["type"] == "payment_intent.succeeded":
                    payment_intent = event["data"]["object"]
                    # Update invoice status
                    return {
                        "event_type": event["type"],
                        "payment_intent_id": payment_intent["id"],
                        "status": "processed"
                    }
                elif event["type"] == "invoice.payment_succeeded":
                    invoice = event["data"]["object"]
                    return {
                        "event_type": event["type"],
                        "invoice_id": invoice["id"],
                        "status": "processed"
                    }
                elif event["type"] == "customer.subscription.deleted":
                    subscription = event["data"]["object"]
                    return {
                        "event_type": event["type"],
                        "subscription_id": subscription["id"],
                        "status": "cancelled"
                    }
                
                return {
                    "event_type": event["type"],
                    "status": "received"
                }
            except ValueError as e:
                logger.error(f"Invalid webhook payload: {str(e)}")
                return {"error": "Invalid payload"}
            except stripe.error.SignatureVerificationError as e:
                logger.error(f"Invalid webhook signature: {str(e)}")
                return {"error": "Invalid signature"}
        else:
            return {
                "error": "Webhook handling not supported for this provider"
            }
    
    def process_ksa_payment(
        self,
        invoice: Invoice,
        payment_method: str,  # mada, bank_transfer, etc.
        transaction_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process KSA-specific payment methods"""
        # For Mada or other KSA payment methods
        # This would integrate with local payment providers
        
        return {
            "provider": "ksa_local",
            "payment_method": payment_method,
            "invoice_id": invoice.invoice_id,
            "amount": float(invoice.amount),
            "currency": invoice.currency,
            "status": "pending_verification",
            "message": f"Payment via {payment_method} requires manual verification"
        }


# Example usage
if __name__ == "__main__":
    from billing_system import BillingSystem
    from tenant_manager import TenantManager
    from subscription_plans import SubscriptionPlanManager
    from usage_tracker import UsageTracker
    
    tenant_manager = TenantManager()
    plan_manager = SubscriptionPlanManager()
    usage_tracker = UsageTracker(tenant_manager)
    billing = BillingSystem(tenant_manager, plan_manager, usage_tracker)
    
    # Create payment integration
    payment = PaymentIntegration(
        billing_system=billing,
        provider="stripe",
        stripe_secret_key=os.getenv("STRIPE_SECRET_KEY")
    )
    
    # Generate invoice
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        invoice = billing.generate_invoice(tenant.tenant_id)
        
        # Create payment intent
        intent = payment.create_payment_intent(invoice)
        print(f"Payment intent: {intent}")
