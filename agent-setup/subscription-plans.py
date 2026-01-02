"""
Subscription Plans - Plan definitions and management
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PlanFeature:
    """Plan feature definition"""
    name: str
    enabled: bool
    limit: Optional[int] = None
    value: Optional[Any] = None


@dataclass
class SubscriptionPlan:
    """Subscription plan definition"""
    plan_id: str
    name: str
    tier: str  # starter, professional, enterprise
    price_monthly: float
    price_yearly: Optional[float] = None
    max_agents: Optional[int] = None  # None = unlimited
    max_workflows: Optional[int] = None
    max_api_calls: Optional[int] = None
    max_storage_gb: Optional[int] = None
    included_modules: List[str] = None
    features: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.included_modules is None:
            self.included_modules = []
        if self.features is None:
            self.features = {}


class SubscriptionPlanManager:
    """Manages subscription plans"""
    
    def __init__(self):
        self.plans: Dict[str, SubscriptionPlan] = {}
        self._initialize_default_plans()
    
    def _initialize_default_plans(self):
        """Initialize default subscription plans"""
        
        # Starter Plan
        starter = SubscriptionPlan(
            plan_id="starter",
            name="Starter Plan",
            tier="starter",
            price_monthly=99.00,
            price_yearly=990.00,  # 10% discount
            max_agents=5,
            max_workflows=10,
            max_api_calls=10000,
            max_storage_gb=10,
            included_modules=["email_automation"],
            features={
                "support": "email",
                "custom_workflows": False,
                "advanced_analytics": False,
                "api_access": True,
                "webhook_support": False
            }
        )
        self.plans["starter"] = starter
        
        # Professional Plan
        professional = SubscriptionPlan(
            plan_id="professional",
            name="Professional Plan",
            tier="professional",
            price_monthly=299.00,
            price_yearly=2990.00,  # 10% discount
            max_agents=20,
            max_workflows=50,
            max_api_calls=100000,
            max_storage_gb=50,
            included_modules=["email_automation", "sales_agent", "support_agent", "workflow_automation"],
            features={
                "support": "priority",
                "custom_workflows": True,
                "advanced_analytics": True,
                "api_access": True,
                "webhook_support": True,
                "custom_integrations": False
            }
        )
        self.plans["professional"] = professional
        
        # Enterprise Plan
        enterprise = SubscriptionPlan(
            plan_id="enterprise",
            name="Enterprise Plan",
            tier="enterprise",
            price_monthly=999.00,
            price_yearly=9990.00,  # 10% discount
            max_agents=None,  # Unlimited
            max_workflows=None,  # Unlimited
            max_api_calls=None,  # Unlimited
            max_storage_gb=500,
            included_modules=["all"],  # All modules
            features={
                "support": "dedicated",
                "custom_workflows": True,
                "advanced_analytics": True,
                "api_access": True,
                "webhook_support": True,
                "custom_integrations": True,
                "sla": True,
                "dedicated_account_manager": True
            }
        )
        self.plans["enterprise"] = enterprise
    
    def get_plan(self, plan_id: str) -> Optional[SubscriptionPlan]:
        """Get plan by ID"""
        return self.plans.get(plan_id)
    
    def list_plans(self) -> List[SubscriptionPlan]:
        """List all plans"""
        return list(self.plans.values())
    
    def get_plan_by_tier(self, tier: str) -> Optional[SubscriptionPlan]:
        """Get plan by tier"""
        for plan in self.plans.values():
            if plan.tier == tier:
                return plan
        return None
    
    def compare_plans(self) -> Dict[str, Any]:
        """Compare all plans"""
        comparison = {
            "plans": [],
            "features": {}
        }
        
        # Get all unique features
        all_features = set()
        for plan in self.plans.values():
            all_features.update(plan.features.keys())
        
        # Build comparison
        for plan in self.plans.values():
            plan_data = {
                "plan_id": plan.plan_id,
                "name": plan.name,
                "tier": plan.tier,
                "price_monthly": plan.price_monthly,
                "price_yearly": plan.price_yearly,
                "limits": {
                    "max_agents": plan.max_agents,
                    "max_workflows": plan.max_workflows,
                    "max_api_calls": plan.max_api_calls,
                    "max_storage_gb": plan.max_storage_gb
                },
                "included_modules": plan.included_modules,
                "features": plan.features
            }
            comparison["plans"].append(plan_data)
        
        return comparison
    
    def check_feature_access(self, plan_id: str, feature: str) -> bool:
        """Check if plan has access to a feature"""
        plan = self.get_plan(plan_id)
        if not plan:
            return False
        
        return plan.features.get(feature, False)
    
    def check_module_access(self, plan_id: str, module_name: str) -> bool:
        """Check if plan includes a module"""
        plan = self.get_plan(plan_id)
        if not plan:
            return False
        
        if "all" in plan.included_modules:
            return True
        
        return module_name in plan.included_modules
    
    def check_limit(self, plan_id: str, resource: str, current_usage: int) -> Dict[str, Any]:
        """Check if usage is within plan limits"""
        plan = self.get_plan(plan_id)
        if not plan:
            return {"within_limit": False, "limit": None, "usage": current_usage}
        
        limit_map = {
            "agents": plan.max_agents,
            "workflows": plan.max_workflows,
            "api_calls": plan.max_api_calls,
            "storage_gb": plan.max_storage_gb
        }
        
        limit = limit_map.get(resource)
        
        if limit is None:  # Unlimited
            return {"within_limit": True, "limit": None, "usage": current_usage, "remaining": None}
        
        within_limit = current_usage < limit
        remaining = max(0, limit - current_usage) if within_limit else 0
        
        return {
            "within_limit": within_limit,
            "limit": limit,
            "usage": current_usage,
            "remaining": remaining,
            "exceeded": not within_limit
        }


# Example usage
if __name__ == "__main__":
    manager = SubscriptionPlanManager()
    
    # List all plans
    plans = manager.list_plans()
    for plan in plans:
        print(f"{plan.name}: ${plan.price_monthly}/month")
        print(f"  Agents: {plan.max_agents or 'Unlimited'}")
        print(f"  Workflows: {plan.max_workflows or 'Unlimited'}")
        print(f"  Modules: {', '.join(plan.included_modules)}")
        print()
    
    # Compare plans
    comparison = manager.compare_plans()
    print("Plan Comparison:")
    print(comparison)
