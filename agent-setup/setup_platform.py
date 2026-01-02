"""
Platform Setup Script
Initializes the multi-tenant SaaS platform
"""

import os
import sys
from pathlib import Path
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def setup_platform():
    """Setup the multi-tenant platform"""
    logger.info("=" * 80)
    logger.info("MULTI-TENANT SAAS PLATFORM SETUP")
    logger.info("=" * 80)
    
    # 1. Create directories
    logger.info("\n1. Creating directories...")
    directories = [
        "tenant_databases",
        "logs",
        "backups"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"   ✅ {directory}/")
    
    # 2. Initialize platform database
    logger.info("\n2. Initializing platform database...")
    from tenant_manager import TenantManager
    
    platform_db_path = os.getenv("PLATFORM_DB_PATH", "platform.db")
    tenant_manager = TenantManager(platform_db_path=platform_db_path)
    
    logger.info(f"   ✅ Platform database initialized: {platform_db_path}")
    
    # 3. Verify subscription plans
    logger.info("\n3. Verifying subscription plans...")
    from subscription_plans import SubscriptionPlanManager
    
    plan_manager = SubscriptionPlanManager()
    plans = plan_manager.list_plans()
    
    for plan in plans:
        logger.info(f"   ✅ {plan.name}: ${plan.price_monthly}/month")
    
    # 4. Initialize module marketplace
    logger.info("\n4. Initializing module marketplace...")
    from module_marketplace import ModuleMarketplace
    
    marketplace = ModuleMarketplace(tenant_manager, platform_db_path=platform_db_path)
    modules = marketplace.list_modules()
    
    logger.info(f"   ✅ {len(modules)} modules available in marketplace")
    
    # 5. Check environment variables
    logger.info("\n5. Checking environment variables...")
    required_vars = [
        "PLATFORM_DB_PATH",
        "TENANT_DB_DIR"
    ]
    
    optional_vars = [
        "STRIPE_SECRET_KEY",
        "STRIPE_WEBHOOK_SECRET",
        "REDIS_HOST",
        "REDIS_PORT"
    ]
    
    missing_required = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_required.append(var)
        else:
            logger.info(f"   ✅ {var}={value}")
    
    if missing_required:
        logger.warning(f"   ⚠️  Missing required variables: {', '.join(missing_required)}")
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"   ✅ {var} is set")
        else:
            logger.info(f"   ⚠️  {var} not set (optional)")
    
    # 6. Test database connections
    logger.info("\n6. Testing database connections...")
    try:
        import sqlite3
        conn = sqlite3.connect(platform_db_path)
        conn.close()
        logger.info(f"   ✅ Platform database connection successful")
    except Exception as e:
        logger.error(f"   ❌ Platform database connection failed: {str(e)}")
        return False
    
    # 7. Create example tenant (optional)
    create_example = os.getenv("CREATE_EXAMPLE_TENANT", "false").lower() == "true"
    if create_example:
        logger.info("\n7. Creating example tenant...")
        from tenant_provisioning import TenantProvisioner
        
        provisioner = TenantProvisioner(tenant_manager)
        example_tenant = tenant_manager.create_tenant(
            name="Example Company",
            subdomain="example",
            subscription_tier="starter"
        )
        
        result = provisioner.provision_tenant(example_tenant)
        
        if result.get("database_created"):
            logger.info(f"   ✅ Example tenant created: {example_tenant.tenant_id}")
            logger.info(f"      Subdomain: {example_tenant.subdomain}")
            logger.info(f"      Access at: http://{example_tenant.subdomain}.yourdomain.com")
        else:
            logger.warning(f"   ⚠️  Example tenant creation had issues: {result.get('errors', [])}")
    else:
        logger.info("\n7. Skipping example tenant creation (set CREATE_EXAMPLE_TENANT=true to enable)")
    
    logger.info("\n" + "=" * 80)
    logger.info("SETUP COMPLETE")
    logger.info("=" * 80)
    logger.info("\nNext steps:")
    logger.info("1. Review environment variables in .env file")
    logger.info("2. Configure payment gateway (Stripe, etc.)")
    logger.info("3. Start API servers:")
    logger.info("   - Tenant API: python tenant-api.py")
    logger.info("   - API Gateway: python api-gateway.py")
    logger.info("   - Webhook Receiver: python webhook-receiver.py")
    logger.info("4. Run tests: python test_tenant_system.py")
    logger.info("=" * 80)
    
    return True


if __name__ == "__main__":
    success = setup_platform()
    sys.exit(0 if success else 1)
