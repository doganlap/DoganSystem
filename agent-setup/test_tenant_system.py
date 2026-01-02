"""
Comprehensive Test Suite for Multi-Tenant SaaS Platform
Tests tenant creation, provisioning, agents, billing, modules, and localization
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tenant_manager import TenantManager, TenantStatus
from tenant_provisioning import TenantProvisioner
from tenant_isolation import TenantIsolation
from employee_agent_system import EmployeeAgentSystem
from agent_delegation import AgentDelegation
from agent_teams import AgentTeams
from agent_hierarchy import AgentHierarchy
from subscription_plans import SubscriptionPlanManager
from usage_tracker import UsageTracker, UsageMetric
from billing_system import BillingSystem
from module_marketplace import ModuleMarketplace, ModuleCategory
from module_manager import ModuleManager
from ksa_localization import KSALocalizationManager
from erpnext_tenant_integration import ERPNextTenantIntegration
from tenant_security import TenantSecurity
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestSuite:
    """Comprehensive test suite"""
    
    def __init__(self):
        self.tenant_manager = TenantManager(platform_db_path="test_platform.db")
        self.tenant_provisioner = TenantProvisioner(self.tenant_manager, tenant_db_dir="test_tenant_databases")
        self.tenant_isolation = TenantIsolation(self.tenant_manager, tenant_db_dir="test_tenant_databases")
        self.agent_system = EmployeeAgentSystem(self.tenant_isolation)
        self.delegation = AgentDelegation(self.tenant_isolation, self.agent_system)
        self.teams = AgentTeams(self.tenant_isolation, self.agent_system)
        self.hierarchy = AgentHierarchy(self.tenant_isolation, self.agent_system)
        self.plan_manager = SubscriptionPlanManager()
        self.usage_tracker = UsageTracker(self.tenant_manager, platform_db_path="test_platform.db")
        self.billing = BillingSystem(self.tenant_manager, self.plan_manager, self.usage_tracker, platform_db_path="test_platform.db")
        self.marketplace = ModuleMarketplace(self.tenant_manager, platform_db_path="test_platform.db")
        self.module_manager = ModuleManager(self.tenant_isolation, self.marketplace)
        self.ksa_local = KSALocalizationManager(self.tenant_isolation)
        self.erpnext_integration = ERPNextTenantIntegration(self.tenant_isolation)
        self.security = TenantSecurity(self.tenant_manager, self.tenant_isolation)
        
        self.test_tenant = None
        self.test_results = []
    
    def run_all_tests(self):
        """Run all tests"""
        logger.info("=" * 80)
        logger.info("STARTING COMPREHENSIVE TEST SUITE")
        logger.info("=" * 80)
        
        try:
            # Test 1: Tenant Creation and Provisioning
            self.test_tenant_creation()
            
            # Test 2: Agent Creation and Management
            self.test_agent_creation()
            
            # Test 3: Agent Delegation
            self.test_agent_delegation()
            
            # Test 4: Teams and Hierarchy
            self.test_teams_and_hierarchy()
            
            # Test 5: Subscription and Billing
            self.test_billing_system()
            
            # Test 6: Module Marketplace
            self.test_module_marketplace()
            
            # Test 7: KSA Localization
            self.test_ksa_localization()
            
            # Test 8: Usage Tracking
            self.test_usage_tracking()
            
            # Test 9: Security
            self.test_security()
            
            # Test 10: ERPNext Integration
            self.test_erpnext_integration()
            
            logger.info("=" * 80)
            logger.info("ALL TESTS COMPLETED")
            logger.info("=" * 80)
            self.print_summary()
            
        except Exception as e:
            logger.error(f"Test suite failed: {str(e)}", exc_info=True)
            raise
    
    def test_tenant_creation(self):
        """Test 1: Tenant Creation and Provisioning"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 1: Tenant Creation and Provisioning")
        logger.info("=" * 80)
        
        try:
            # Create tenant
            tenant = self.tenant_manager.create_tenant(
                name="Test Company KSA",
                subdomain="testksa",
                subscription_tier="professional",
                trial_days=14
            )
            self.test_tenant = tenant
            
            assert tenant is not None, "Tenant creation failed"
            assert tenant.status == TenantStatus.TRIAL.value, f"Expected trial status, got {tenant.status}"
            assert tenant.subscription_tier == "professional", "Wrong subscription tier"
            
            logger.info(f"✅ Tenant created: {tenant.tenant_id} ({tenant.name})")
            
            # Provision tenant
            result = self.tenant_provisioner.provision_tenant(tenant)
            
            assert result["database_created"], "Database creation failed"
            assert result["schema_initialized"], "Schema initialization failed"
            assert result["default_agents_created"], "Default agents creation failed"
            assert result["default_workflows_created"], "Default workflows creation failed"
            assert result["ksa_config_created"], "KSA config creation failed"
            
            logger.info(f"✅ Tenant provisioned successfully")
            logger.info(f"   - Database: {result.get('database_path', 'N/A')}")
            logger.info(f"   - Default agents: Created")
            logger.info(f"   - Default workflows: Created")
            logger.info(f"   - KSA config: Created")
            
            # Verify tenant retrieval
            retrieved = self.tenant_manager.get_tenant(tenant.tenant_id)
            assert retrieved is not None, "Tenant retrieval failed"
            assert retrieved.name == tenant.name, "Tenant name mismatch"
            
            logger.info(f"✅ Tenant retrieval verified")
            
            # Test quota
            quota = self.tenant_manager.get_tenant_quota(tenant.tenant_id)
            assert quota is not None, "Quota retrieval failed"
            assert "max_agents" in quota, "Quota missing max_agents"
            
            logger.info(f"✅ Quota retrieved: {quota}")
            
            self.test_results.append(("Tenant Creation and Provisioning", True, ""))
            
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
            self.test_results.append(("Tenant Creation and Provisioning", False, str(e)))
            raise
    
    def test_agent_creation(self):
        """Test 2: Agent Creation and Management"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 2: Agent Creation and Management")
        logger.info("=" * 80)
        
        try:
            tenant_id = self.test_tenant.tenant_id
            
            # Create agent
            agent = self.agent_system.create_agent(
                tenant_id=tenant_id,
                employee_name="أحمد السعود",
                role="Sales Manager",
                department="Sales",
                capabilities=["customer_management", "quotation", "sales_order"]
            )
            
            assert agent is not None, "Agent creation failed"
            assert agent.employee_name == "أحمد السعود", "Agent name mismatch"
            assert agent.role == "Sales Manager", "Agent role mismatch"
            assert len(agent.capabilities) == 3, "Agent capabilities mismatch"
            
            logger.info(f"✅ Agent created: {agent.employee_name} ({agent.agent_id})")
            
            # Retrieve agent
            retrieved = self.agent_system.get_agent(tenant_id, agent.agent_id)
            assert retrieved is not None, "Agent retrieval failed"
            assert retrieved.employee_name == agent.employee_name, "Retrieved agent name mismatch"
            
            logger.info(f"✅ Agent retrieval verified")
            
            # List agents
            agents = self.agent_system.list_agents(tenant_id)
            assert len(agents) > 0, "No agents found"
            assert any(a.agent_id == agent.agent_id for a in agents), "Created agent not in list"
            
            logger.info(f"✅ Agent listing verified: {len(agents)} agents found")
            
            # Update agent
            success = self.agent_system.update_agent(
                tenant_id, agent.agent_id,
                status="busy"
            )
            assert success, "Agent update failed"
            
            updated = self.agent_system.get_agent(tenant_id, agent.agent_id)
            assert updated.status == "busy", "Agent status not updated"
            
            logger.info(f"✅ Agent update verified")
            
            self.test_results.append(("Agent Creation and Management", True, ""))
            
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
            self.test_results.append(("Agent Creation and Management", False, str(e)))
            raise
    
    def test_agent_delegation(self):
        """Test 3: Agent Delegation"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 3: Agent Delegation")
        logger.info("=" * 80)
        
        try:
            tenant_id = self.test_tenant.tenant_id
            
            # Get agents
            agents = self.agent_system.list_agents(tenant_id)
            assert len(agents) >= 2, "Need at least 2 agents for delegation test"
            
            from_agent = agents[0]
            to_agent = agents[1]
            
            # Delegate task
            delegation = self.delegation.delegate_task(
                tenant_id=tenant_id,
                from_agent_id=from_agent.agent_id,
                to_agent_id=to_agent.agent_id,
                task_description="Create quotation for customer ABC",
                task_type="erpnext_action",
                task_config={"action": "create_quotation", "customer": "ABC Corp"}
            )
            
            assert delegation is not None, "Delegation creation failed"
            assert delegation.status == "pending", "Delegation status should be pending"
            
            logger.info(f"✅ Task delegated from {from_agent.employee_name} to {to_agent.employee_name}")
            
            # Accept delegation
            success = self.delegation.accept_delegation(tenant_id, delegation.delegation_id, to_agent.agent_id)
            assert success, "Delegation acceptance failed"
            
            accepted = self.delegation.get_delegation(tenant_id, delegation.delegation_id)
            assert accepted.status == "in_progress", "Delegation should be in_progress"
            
            logger.info(f"✅ Delegation accepted")
            
            # Complete delegation
            success = self.delegation.complete_delegation(
                tenant_id,
                delegation.delegation_id,
                {"quotation_id": "QUO-00001", "status": "created"},
                "Quotation created successfully"
            )
            assert success, "Delegation completion failed"
            
            completed = self.delegation.get_delegation(tenant_id, delegation.delegation_id)
            assert completed.status == "completed", "Delegation should be completed"
            
            logger.info(f"✅ Delegation completed")
            
            self.test_results.append(("Agent Delegation", True, ""))
            
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
            self.test_results.append(("Agent Delegation", False, str(e)))
            raise
    
    def test_teams_and_hierarchy(self):
        """Test 4: Teams and Hierarchy"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 4: Teams and Hierarchy")
        logger.info("=" * 80)
        
        try:
            tenant_id = self.test_tenant.tenant_id
            
            # Create team
            team = self.teams.create_team(
                tenant_id=tenant_id,
                team_name="Sales Team A",
                department="Sales"
            )
            
            assert team is not None, "Team creation failed"
            assert team.team_name == "Sales Team A", "Team name mismatch"
            
            logger.info(f"✅ Team created: {team.team_name} ({team.team_id})")
            
            # Add agent to team
            agents = self.agent_system.list_agents(tenant_id)
            if agents:
                agent = agents[0]
                success = self.teams.add_agent_to_team(tenant_id, agent.agent_id, team.team_id)
                assert success, "Failed to add agent to team"
                
                logger.info(f"✅ Agent {agent.employee_name} added to team")
            
            # Get team members
            members = self.teams.get_team_members(tenant_id, team.team_id)
            assert len(members) > 0, "Team should have members"
            
            logger.info(f"✅ Team members: {len(members)}")
            
            # Test hierarchy
            if len(agents) >= 2:
                manager = agents[0]
                worker = agents[1]
                
                success = self.hierarchy.set_manager(tenant_id, worker.agent_id, manager.agent_id)
                assert success, "Failed to set manager"
                
                logger.info(f"✅ Manager set: {manager.employee_name} manages {worker.employee_name}")
                
                # Get direct reports
                reports = self.hierarchy.get_direct_reports(tenant_id, manager.agent_id)
                assert len(reports) > 0, "Manager should have reports"
                
                logger.info(f"✅ Direct reports: {len(reports)}")
            
            # Get org chart
            org_chart = self.hierarchy.get_org_chart(tenant_id)
            assert org_chart is not None, "Org chart generation failed"
            assert "top_level" in org_chart, "Org chart missing top_level"
            
            logger.info(f"✅ Org chart generated: {org_chart['total_agents']} agents")
            
            self.test_results.append(("Teams and Hierarchy", True, ""))
            
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
            self.test_results.append(("Teams and Hierarchy", False, str(e)))
            raise
    
    def test_billing_system(self):
        """Test 5: Subscription and Billing"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 5: Subscription and Billing")
        logger.info("=" * 80)
        
        try:
            tenant_id = self.test_tenant.tenant_id
            
            # Create subscription
            subscription = self.billing.create_subscription(
                tenant_id=tenant_id,
                plan_id="professional",
                billing_cycle="monthly"
            )
            
            assert subscription is not None, "Subscription creation failed"
            assert subscription["status"] == "active", "Subscription should be active"
            
            logger.info(f"✅ Subscription created: {subscription['subscription_id']}")
            
            # Generate invoice
            invoice = self.billing.generate_invoice(tenant_id, subscription["subscription_id"])
            
            assert invoice is not None, "Invoice generation failed"
            assert invoice.amount > 0, "Invoice amount should be positive"
            assert invoice.currency == "SAR", "Invoice currency should be SAR"
            
            logger.info(f"✅ Invoice generated: {invoice.invoice_number}, Amount: {invoice.amount} {invoice.currency}")
            
            # Record payment
            payment = self.billing.record_payment(
                invoice.invoice_id,
                invoice.amount,
                "stripe",
                "ch_test123"
            )
            
            assert payment is not None, "Payment recording failed"
            assert payment["status"] == "completed", "Payment should be completed"
            
            logger.info(f"✅ Payment recorded: {payment['payment_id']}")
            
            # Get invoices
            invoices = self.billing.get_tenant_invoices(tenant_id)
            assert len(invoices) > 0, "Should have invoices"
            
            logger.info(f"✅ Invoices retrieved: {len(invoices)}")
            
            self.test_results.append(("Subscription and Billing", True, ""))
            
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
            self.test_results.append(("Subscription and Billing", False, str(e)))
            raise
    
    def test_module_marketplace(self):
        """Test 6: Module Marketplace"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 6: Module Marketplace")
        logger.info("=" * 80)
        
        try:
            tenant_id = self.test_tenant.tenant_id
            
            # List modules
            modules = self.marketplace.list_modules()
            assert len(modules) > 0, "Should have modules in marketplace"
            
            logger.info(f"✅ Modules in marketplace: {len(modules)}")
            for module in modules[:3]:
                logger.info(f"   - {module.display_name}: ${module.price_monthly}/month")
            
            # Purchase module
            module = modules[0]
            result = self.marketplace.purchase_module(tenant_id, module.module_id)
            
            assert result["success"], f"Module purchase failed: {result.get('error', 'Unknown error')}"
            
            logger.info(f"✅ Module purchased: {module.display_name}")
            
            # Verify tenant has module
            has_module = self.marketplace.tenant_has_module(tenant_id, module.module_id)
            assert has_module, "Tenant should have purchased module"
            
            logger.info(f"✅ Module ownership verified")
            
            # Get tenant modules
            tenant_modules = self.marketplace.get_tenant_modules(tenant_id)
            assert len(tenant_modules) > 0, "Tenant should have modules"
            assert any(m["module_name"] == module.module_id for m in tenant_modules), "Purchased module not in list"
            
            logger.info(f"✅ Tenant modules: {len(tenant_modules)}")
            
            # Install module
            install_result = self.module_manager.install_module(
                tenant_id,
                module.module_id,
                {"auto_quotation": True}
            )
            
            assert install_result["success"], f"Module installation failed: {install_result.get('error', 'Unknown error')}"
            
            logger.info(f"✅ Module installed: {module.display_name}")
            
            self.test_results.append(("Module Marketplace", True, ""))
            
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
            self.test_results.append(("Module Marketplace", False, str(e)))
            raise
    
    def test_ksa_localization(self):
        """Test 7: KSA Localization"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 7: KSA Localization")
        logger.info("=" * 80)
        
        try:
            tenant_id = self.test_tenant.tenant_id
            
            # Get localization
            loc = self.ksa_local.get_localization(tenant_id)
            
            assert loc.locale == "ar_SA", f"Expected ar_SA locale, got {loc.locale}"
            assert loc.timezone == "Asia/Riyadh", f"Expected Asia/Riyadh timezone, got {loc.timezone}"
            assert loc.currency == "SAR", f"Expected SAR currency, got {loc.currency}"
            assert loc.work_week_start == "Saturday", "Expected Saturday as work week start"
            assert loc.enable_hijri_calendar == True, "Hijri calendar should be enabled"
            
            logger.info(f"✅ Localization verified:")
            logger.info(f"   - Locale: {loc.locale}")
            logger.info(f"   - Timezone: {loc.timezone}")
            logger.info(f"   - Currency: {loc.currency}")
            logger.info(f"   - Work week: {loc.work_week_start} to {loc.work_week_end}")
            
            # Test currency formatting
            formatted = self.ksa_local.format_currency(tenant_id, 1234.56)
            assert "ر.س" in formatted or "SAR" in formatted, "Currency formatting failed"
            
            logger.info(f"✅ Currency formatting: {formatted}")
            
            # Test business day
            from datetime import datetime
            now = datetime.now()
            is_business = self.ksa_local.is_business_day(tenant_id, now)
            
            logger.info(f"✅ Business day check: {is_business} for {now.strftime('%A')}")
            
            # Test time conversion
            utc_time = datetime.now()
            local_time = self.ksa_local.to_local_time(tenant_id, utc_time)
            
            logger.info(f"✅ Time conversion: UTC {utc_time} -> Local {local_time}")
            
            self.test_results.append(("KSA Localization", True, ""))
            
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
            self.test_results.append(("KSA Localization", False, str(e)))
            raise
    
    def test_usage_tracking(self):
        """Test 8: Usage Tracking"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 8: Usage Tracking")
        logger.info("=" * 80)
        
        try:
            tenant_id = self.test_tenant.tenant_id
            
            # Record usage
            self.usage_tracker.increment_api_call(tenant_id, 100)
            self.usage_tracker.increment_email_usage(tenant_id, 5)
            self.usage_tracker.set_storage_usage(tenant_id, 15.5)
            
            logger.info(f"✅ Usage recorded")
            
            # Get usage
            usage = self.usage_tracker.get_current_month_usage(tenant_id)
            
            assert "api_calls" in usage, "API calls usage missing"
            assert usage["api_calls"] >= 100, "API calls usage incorrect"
            assert "emails" in usage, "Email usage missing"
            assert usage["emails"] >= 5, "Email usage incorrect"
            assert "storage_gb" in usage, "Storage usage missing"
            
            logger.info(f"✅ Usage retrieved: {usage}")
            
            # Check quota
            quota_check = self.usage_tracker.check_quota_exceeded(tenant_id)
            
            logger.info(f"✅ Quota check: Exceeded={quota_check['exceeded']}, Violations={len(quota_check['violations'])}")
            
            self.test_results.append(("Usage Tracking", True, ""))
            
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
            self.test_results.append(("Usage Tracking", False, str(e)))
            raise
    
    def test_security(self):
        """Test 9: Security"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 9: Security")
        logger.info("=" * 80)
        
        try:
            tenant_id = self.test_tenant.tenant_id
            
            # Generate API key
            keys = self.security.generate_api_key(tenant_id, "test_key")
            
            assert "api_key" in keys, "API key generation failed"
            assert "api_secret" in keys, "API secret generation failed"
            
            logger.info(f"✅ API key generated: {keys['key_id']}")
            
            # Verify API key
            verified_tenant = self.security.verify_api_key(keys["api_key"])
            assert verified_tenant == tenant_id, "API key verification failed"
            
            logger.info(f"✅ API key verified")
            
            # Check compliance
            compliance = self.security.check_ksa_compliance(tenant_id)
            
            assert compliance["compliant"] is not None, "Compliance check failed"
            
            logger.info(f"✅ KSA Compliance check: {compliance['compliant']}")
            logger.info(f"   Checks: {compliance['checks']}")
            
            self.test_results.append(("Security", True, ""))
            
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
            self.test_results.append(("Security", False, str(e)))
            raise
    
    def test_erpnext_integration(self):
        """Test 10: ERPNext Integration"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 10: ERPNext Integration")
        logger.info("=" * 80)
        
        try:
            tenant_id = self.test_tenant.tenant_id
            
            # Configure ERPNext (mock)
            success = self.erpnext_integration.configure_erpnext(
                tenant_id=tenant_id,
                base_url="http://localhost:8000",
                api_key="test_key",
                api_secret="test_secret",
                site_name="test_site"
            )
            
            assert success, "ERPNext configuration failed"
            
            logger.info(f"✅ ERPNext configured")
            
            # Get config
            config = self.erpnext_integration.get_erpnext_config(tenant_id)
            
            assert config is not None, "ERPNext config retrieval failed"
            assert config["configured"] == True, "ERPNext should be configured"
            
            logger.info(f"✅ ERPNext config retrieved: {config['base_url']}")
            
            self.test_results.append(("ERPNext Integration", True, ""))
            
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
            self.test_results.append(("ERPNext Integration", False, str(e)))
            # Don't raise - ERPNext might not be available in test environment
    
    def print_summary(self):
        """Print test summary"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST SUMMARY")
        logger.info("=" * 80)
        
        total = len(self.test_results)
        passed = sum(1 for _, success, _ in self.test_results if success)
        failed = total - passed
        
        for test_name, success, error in self.test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            logger.info(f"{status}: {test_name}")
            if error:
                logger.info(f"   Error: {error}")
        
        logger.info("=" * 80)
        logger.info(f"Total: {total} | Passed: {passed} | Failed: {failed}")
        logger.info("=" * 80)
        
        if failed == 0:
            logger.info("🎉 ALL TESTS PASSED!")
        else:
            logger.warning(f"⚠️  {failed} test(s) failed")


if __name__ == "__main__":
    import shutil
    
    # Clean up test databases
    test_db = Path("test_platform.db")
    test_dir = Path("test_tenant_databases")
    
    if test_db.exists():
        test_db.unlink()
    
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    test_dir.mkdir(exist_ok=True)
    
    # Run tests
    suite = TestSuite()
    suite.run_all_tests()
