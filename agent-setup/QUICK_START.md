# Multi-Tenant SaaS Platform - Quick Start Guide

## Prerequisites

- Python 3.8+
- pip
- SQLite (included with Python)
- (Optional) PostgreSQL for production
- (Optional) Redis for distributed event bus

## Installation

### 1. Install Dependencies

```bash
cd agent-setup
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `env.example` to `.env` and configure:

```bash
cp env.example .env
```

Edit `.env` with your settings:

```env
# Multi-Tenancy
PLATFORM_DB_PATH=platform.db
TENANT_DB_DIR=tenant_databases
TENANT_ISOLATION_MODE=database

# Billing (Optional - for payment processing)
BILLING_PROVIDER=stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
USAGE_TRACKING_ENABLED=true

# SaaS Settings
TRIAL_PERIOD_DAYS=14
DEFAULT_PLAN=starter

# ERPNext (Optional)
ERPNEXT_BASE_URL=http://localhost:8000
ERPNEXT_API_KEY=your_api_key
ERPNEXT_API_SECRET=your_api_secret

# Redis (Optional - for distributed event bus)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 3. Initialize Platform

```bash
python setup_platform.py
```

This will:
- Create necessary directories
- Initialize platform database
- Set up subscription plans
- Initialize module marketplace
- (Optional) Create example tenant

### 4. Run Tests

```bash
python test_tenant_system.py
```

This comprehensive test suite will verify:
- ✅ Tenant creation and provisioning
- ✅ Agent creation and management
- ✅ Agent delegation
- ✅ Teams and hierarchy
- ✅ Billing system
- ✅ Module marketplace
- ✅ KSA localization
- ✅ Usage tracking
- ✅ Security
- ✅ ERPNext integration

## Starting Services

### Tenant Management API

```bash
python tenant-api.py
```

Access at: `http://localhost:8002`

### API Gateway

```bash
python api-gateway.py
```

Access at: `http://localhost:8006`

### Webhook Receiver

```bash
python webhook-receiver.py
```

Access at: `http://localhost:8003`

### Monitoring Dashboard

```bash
python monitoring-dashboard.py
```

Access at: `http://localhost:8005`

## Creating Your First Tenant

### Using Python

```python
from tenant_manager import TenantManager
from tenant_provisioning import TenantProvisioner

# Initialize
manager = TenantManager()
provisioner = TenantProvisioner(manager)

# Create tenant
tenant = manager.create_tenant(
    name="My Company",
    subdomain="mycompany",
    subscription_tier="professional"
)

# Provision tenant (creates database, agents, workflows)
result = provisioner.provision_tenant(tenant)

print(f"Tenant created: {tenant.tenant_id}")
print(f"Access at: http://{tenant.subdomain}.yourdomain.com")
```

### Using API

```bash
curl -X POST http://localhost:8002/api/admin/tenants \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Company",
    "subdomain": "mycompany",
    "subscription_tier": "professional"
  }'
```

## Creating Employee Agents

```python
from employee_agent_system import EmployeeAgentSystem
from tenant_isolation import TenantIsolation
from tenant_manager import TenantManager

manager = TenantManager()
tenant_isolation = TenantIsolation(manager)
agent_system = EmployeeAgentSystem(tenant_isolation)

tenant = manager.get_tenant_by_subdomain("mycompany")

# Create agent
agent = agent_system.create_agent(
    tenant_id=tenant.tenant_id,
    employee_name="أحمد السعود",
    role="Sales Manager",
    department="Sales",
    capabilities=["customer_management", "quotation", "sales_order"]
)

print(f"Agent created: {agent.employee_name} ({agent.agent_id})")
```

## Purchasing Modules

```python
from module_marketplace import ModuleMarketplace
from tenant_manager import TenantManager

manager = TenantManager()
marketplace = ModuleMarketplace(manager)

tenant = manager.get_tenant_by_subdomain("mycompany")

# List available modules
modules = marketplace.list_modules()
for module in modules:
    print(f"{module.display_name}: ${module.price_monthly}/month")

# Purchase module
result = marketplace.purchase_module(
    tenant.tenant_id,
    "sales_agent"
)

print(f"Purchase result: {result}")
```

## API Examples

### Get Tenant Info

```bash
curl http://localhost:8006/api/v1/tenant/info \
  -H "X-Tenant-ID: tenant_xxx"
```

### Get Quota

```bash
curl http://localhost:8006/api/v1/tenant/quota \
  -H "X-Tenant-ID: tenant_xxx"
```

### List Agents

```bash
curl http://localhost:8006/api/v1/tenant_xxx/agents
```

## Tenant Routing

The system supports multiple routing methods:

1. **Subdomain**: `http://mycompany.yourdomain.com`
2. **Path**: `http://yourdomain.com/api/tenant/tenant_xxx/...`
3. **Header**: `X-Tenant-ID: tenant_xxx`
4. **Query**: `?tenant_id=tenant_xxx`

## KSA Localization

All tenants are configured with KSA defaults:
- **Locale**: `ar_SA` (Arabic - Saudi Arabia)
- **Timezone**: `Asia/Riyadh`
- **Currency**: `SAR` (Saudi Riyal)
- **Work Week**: Saturday to Wednesday
- **Hijri Calendar**: Enabled

## Subscription Plans

### Starter Plan - $99/month
- 5 employee agents
- 10 workflows
- 10,000 API calls/month
- 10 GB storage
- 1 ERPNext module

### Professional Plan - $299/month
- 20 employee agents
- 50 workflows
- 100,000 API calls/month
- 50 GB storage
- 5 ERPNext modules

### Enterprise Plan - $999/month
- Unlimited agents
- Unlimited workflows
- Unlimited API calls
- 500 GB storage
- All modules

## Troubleshooting

### Database Issues

If you encounter database errors:
1. Check file permissions
2. Ensure SQLite is available
3. Verify `PLATFORM_DB_PATH` and `TENANT_DB_DIR` are correct

### Import Errors

If you get import errors:
```bash
# Ensure you're in the agent-setup directory
cd agent-setup

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Conflicts

If ports are already in use:
- Change ports in the Python files
- Or stop existing services

## Next Steps

1. **Integration**: Connect to your ERPNext instance
2. **Payment**: Configure Stripe or other payment gateway
3. **Deployment**: Set up Docker/Kubernetes for production
4. **Monitoring**: Configure Prometheus and Grafana
5. **UI**: Build admin dashboard

## Support

For issues or questions:
- Check logs in `logs/` directory
- Review test output: `python test_tenant_system.py`
- Check API documentation: See `API_DOCUMENTATION.md`
