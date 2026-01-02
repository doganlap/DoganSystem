"""
Billing System - Subscription and usage-based billing
"""

import sqlite3
import logging
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from decimal import Decimal
import json

from tenant_manager import TenantManager
from subscription_plans import SubscriptionPlanManager
from usage_tracker import UsageTracker, UsageMetric

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class InvoiceItem:
    """Invoice line item"""
    description: str
    quantity: int
    unit_price: Decimal
    total: Decimal
    item_type: str  # subscription, usage, module, etc.


@dataclass
class Invoice:
    """Invoice"""
    invoice_id: str
    tenant_id: str
    subscription_id: Optional[str]
    amount: Decimal
    currency: str
    status: str  # pending, paid, failed, refunded
    due_date: datetime
    items: List[InvoiceItem]
    invoice_number: str
    created_at: datetime


class BillingSystem:
    """Handles subscription and usage-based billing"""
    
    def __init__(
        self,
        tenant_manager: TenantManager,
        plan_manager: SubscriptionPlanManager,
        usage_tracker: UsageTracker,
        platform_db_path: str = "platform.db"
    ):
        self.tenant_manager = tenant_manager
        self.plan_manager = plan_manager
        self.usage_tracker = usage_tracker
        self.platform_db_path = platform_db_path
        self._init_billing_tables()
    
    def _init_billing_tables(self):
        """Initialize billing tables"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        # Invoices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                invoice_id VARCHAR(50) PRIMARY KEY,
                tenant_id VARCHAR(50) NOT NULL,
                subscription_id VARCHAR(50),
                amount DECIMAL(10, 2) NOT NULL,
                currency VARCHAR(3) DEFAULT 'SAR',
                status VARCHAR(20) DEFAULT 'pending',
                due_date TIMESTAMP,
                paid_date TIMESTAMP,
                invoice_number VARCHAR(100) UNIQUE,
                items TEXT, -- JSON array
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id VARCHAR(50) PRIMARY KEY,
                tenant_id VARCHAR(50) NOT NULL,
                invoice_id VARCHAR(50),
                amount DECIMAL(10, 2) NOT NULL,
                currency VARCHAR(3) DEFAULT 'SAR',
                payment_method VARCHAR(50),
                payment_provider_id VARCHAR(100),
                status VARCHAR(20) DEFAULT 'pending',
                transaction_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Subscriptions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tenant_subscriptions (
                subscription_id VARCHAR(50) PRIMARY KEY,
                tenant_id VARCHAR(50) NOT NULL,
                plan_id VARCHAR(50) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'active',
                start_date TIMESTAMP NOT NULL,
                end_date TIMESTAMP,
                renewal_date TIMESTAMP,
                billing_cycle VARCHAR(20) DEFAULT 'monthly',
                payment_method_id VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_invoice_tenant ON invoices(tenant_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_invoice_status ON invoices(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_payment_tenant ON payments(tenant_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_subscription_tenant ON tenant_subscriptions(tenant_id)")
        
        conn.commit()
        conn.close()
    
    def create_subscription(
        self,
        tenant_id: str,
        plan_id: str,
        billing_cycle: str = "monthly",
        payment_method_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a subscription for a tenant"""
        plan = self.plan_manager.get_plan(plan_id)
        if not plan:
            raise ValueError(f"Plan {plan_id} not found")
        
        subscription_id = f"sub_{uuid.uuid4().hex[:12]}"
        start_date = datetime.now()
        
        if billing_cycle == "monthly":
            end_date = start_date + timedelta(days=30)
            renewal_date = end_date
        else:  # yearly
            end_date = start_date + timedelta(days=365)
            renewal_date = end_date
        
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tenant_subscriptions
            (subscription_id, tenant_id, plan_id, status, start_date, end_date, 
             renewal_date, billing_cycle, payment_method_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            subscription_id,
            tenant_id,
            plan_id,
            "active",
            start_date.isoformat(),
            end_date.isoformat(),
            renewal_date.isoformat(),
            billing_cycle,
            payment_method_id
        ))
        
        # Update tenant subscription tier
        self.tenant_manager.update_tenant(tenant_id, subscription_tier=plan.tier)
        
        conn.commit()
        conn.close()
        
        logger.info(f"Subscription created: {subscription_id} for tenant {tenant_id}")
        
        return {
            "subscription_id": subscription_id,
            "tenant_id": tenant_id,
            "plan_id": plan_id,
            "status": "active",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "billing_cycle": billing_cycle
        }
    
    def generate_invoice(
        self,
        tenant_id: str,
        subscription_id: Optional[str] = None,
        include_usage: bool = True
    ) -> Invoice:
        """Generate invoice for tenant"""
        # Get subscription
        subscription = None
        if subscription_id:
            subscription = self._get_subscription(subscription_id)
        
        if not subscription:
            # Get active subscription for tenant
            subscription = self._get_active_subscription(tenant_id)
        
        if not subscription:
            raise ValueError(f"No active subscription for tenant {tenant_id}")
        
        plan = self.plan_manager.get_plan(subscription["plan_id"])
        if not plan:
            raise ValueError(f"Plan {subscription['plan_id']} not found")
        
        # Calculate subscription cost
        billing_cycle = subscription["billing_cycle"]
        if billing_cycle == "monthly":
            subscription_amount = Decimal(str(plan.price_monthly))
        else:
            subscription_amount = Decimal(str(plan.price_yearly))
        
        items = [
            InvoiceItem(
                description=f"{plan.name} ({billing_cycle})",
                quantity=1,
                unit_price=subscription_amount,
                total=subscription_amount,
                item_type="subscription"
            )
        ]
        
        total_amount = subscription_amount
        
        # Add usage charges if enabled
        if include_usage:
            usage_charges = self._calculate_usage_charges(tenant_id, plan)
            if usage_charges:
                for charge in usage_charges:
                    items.append(charge)
                    total_amount += charge.total
        
        # Generate invoice
        invoice_id = f"inv_{uuid.uuid4().hex[:12]}"
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{invoice_id[-6:]}"
        due_date = datetime.now() + timedelta(days=14)
        
        invoice = Invoice(
            invoice_id=invoice_id,
            tenant_id=tenant_id,
            subscription_id=subscription_id or subscription["subscription_id"],
            amount=total_amount,
            currency="SAR",
            status="pending",
            due_date=due_date,
            items=items,
            invoice_number=invoice_number,
            created_at=datetime.now()
        )
        
        # Save invoice
        self._save_invoice(invoice)
        
        logger.info(f"Invoice generated: {invoice_number} for tenant {tenant_id}, amount: {total_amount} SAR")
        
        return invoice
    
    def _calculate_usage_charges(self, tenant_id: str, plan: Any) -> List[InvoiceItem]:
        """Calculate usage-based charges"""
        charges = []
        
        # Get current usage
        usage = self.usage_tracker.get_current_month_usage(tenant_id)
        quota = self.tenant_manager.get_tenant_quota(tenant_id)
        
        # Usage pricing (example rates)
        usage_rates = {
            "api_calls": Decimal("0.01"),  # 0.01 SAR per 1000 calls over limit
            "emails": Decimal("0.10"),  # 0.10 SAR per 1000 emails over limit
            "storage_gb": Decimal("5.00"),  # 5 SAR per GB over limit
        }
        
        # Check API calls
        if quota.get("max_api_calls"):
            api_usage = usage.get("api_calls", 0)
            api_limit = quota["max_api_calls"]
            if api_usage > api_limit:
                overage = api_usage - api_limit
                overage_1000s = (overage + 999) // 1000  # Round up
                charge = overage_1000s * usage_rates["api_calls"]
                charges.append(InvoiceItem(
                    description=f"API Calls Overage ({overage:,} calls)",
                    quantity=overage_1000s,
                    unit_price=usage_rates["api_calls"],
                    total=charge,
                    item_type="usage"
                ))
        
        # Check storage
        if quota.get("max_storage_gb"):
            storage_usage = usage.get("storage_gb", 0)
            storage_limit = quota["max_storage_gb"]
            if storage_usage > storage_limit:
                overage = storage_usage - storage_limit
                charge = Decimal(str(overage)) * usage_rates["storage_gb"]
                charges.append(InvoiceItem(
                    description=f"Storage Overage ({overage:.2f} GB)",
                    quantity=int(overage * 100) / 100,
                    unit_price=usage_rates["storage_gb"],
                    total=charge,
                    item_type="usage"
                ))
        
        return charges
    
    def _get_subscription(self, subscription_id: str) -> Optional[Dict]:
        """Get subscription by ID"""
        conn = sqlite3.connect(self.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM tenant_subscriptions WHERE subscription_id = ?
        """, (subscription_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return dict(row)
    
    def _get_active_subscription(self, tenant_id: str) -> Optional[Dict]:
        """Get active subscription for tenant"""
        conn = sqlite3.connect(self.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM tenant_subscriptions 
            WHERE tenant_id = ? AND status = 'active'
            ORDER BY created_at DESC LIMIT 1
        """, (tenant_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return dict(row)
    
    def _save_invoice(self, invoice: Invoice):
        """Save invoice to database"""
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        items_json = json.dumps([
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": float(item.unit_price),
                "total": float(item.total),
                "item_type": item.item_type
            }
            for item in invoice.items
        ])
        
        cursor.execute("""
            INSERT INTO invoices
            (invoice_id, tenant_id, subscription_id, amount, currency, status,
             due_date, invoice_number, items, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            invoice.invoice_id,
            invoice.tenant_id,
            invoice.subscription_id,
            float(invoice.amount),
            invoice.currency,
            invoice.status,
            invoice.due_date.isoformat(),
            invoice.invoice_number,
            items_json,
            invoice.created_at.isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def record_payment(
        self,
        invoice_id: str,
        amount: Decimal,
        payment_method: str,
        payment_provider_id: Optional[str] = None,
        transaction_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Record a payment"""
        # Get invoice
        invoice = self._get_invoice(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        payment_id = f"pay_{uuid.uuid4().hex[:12]}"
        
        conn = sqlite3.connect(self.platform_db_path)
        cursor = conn.cursor()
        
        # Record payment
        cursor.execute("""
            INSERT INTO payments
            (payment_id, tenant_id, invoice_id, amount, currency, payment_method,
             payment_provider_id, status, transaction_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            payment_id,
            invoice["tenant_id"],
            invoice_id,
            float(amount),
            invoice["currency"],
            payment_method,
            payment_provider_id,
            "completed",
            (transaction_date or datetime.now()).isoformat()
        ))
        
        # Update invoice status
        cursor.execute("""
            UPDATE invoices
            SET status = 'paid', paid_date = ?
            WHERE invoice_id = ?
        """, (datetime.now().isoformat(), invoice_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Payment recorded: {payment_id} for invoice {invoice_id}")
        
        return {
            "payment_id": payment_id,
            "invoice_id": invoice_id,
            "amount": float(amount),
            "status": "completed"
        }
    
    def _get_invoice(self, invoice_id: str) -> Optional[Dict]:
        """Get invoice by ID"""
        conn = sqlite3.connect(self.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM invoices WHERE invoice_id = ?
        """, (invoice_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return dict(row)
    
    def get_tenant_invoices(
        self,
        tenant_id: str,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """Get invoices for a tenant"""
        conn = sqlite3.connect(self.platform_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM invoices WHERE tenant_id = ?"
        params = [tenant_id]
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from subscription_plans import SubscriptionPlanManager
    from usage_tracker import UsageTracker
    
    tenant_manager = TenantManager()
    plan_manager = SubscriptionPlanManager()
    usage_tracker = UsageTracker(tenant_manager)
    billing = BillingSystem(tenant_manager, plan_manager, usage_tracker)
    
    # Create tenant and subscription
    tenant = tenant_manager.create_tenant("Test Company", "testco")
    subscription = billing.create_subscription(tenant.tenant_id, "professional", "monthly")
    
    # Generate invoice
    invoice = billing.generate_invoice(tenant.tenant_id)
    print(f"Invoice: {invoice.invoice_number}, Amount: {invoice.amount} {invoice.currency}")
    
    # Record payment
    payment = billing.record_payment(
        invoice.invoice_id,
        invoice.amount,
        "stripe",
        "ch_test123"
    )
    print(f"Payment recorded: {payment['payment_id']}")
