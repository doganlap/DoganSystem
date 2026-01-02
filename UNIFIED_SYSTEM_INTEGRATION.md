# Unified System Integration Guide

## Overview

The DoganSystem has been fully integrated into a **unified orchestrator** that combines:
- ✅ Multi-tenant SaaS platform
- ✅ Autonomous workflows
- ✅ Employee-style agents
- ✅ KSA localization
- ✅ Self-healing system
- ✅ Email processing
- ✅ Monitoring and metrics

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Unified Orchestrator                     │
│  (Multi-Tenant + Autonomous + Agents + KSA)      │
└──────────────┬──────────────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│Tenant │ │Tenant │ │Tenant │
│   1   │ │   2   │ │   N   │
└───┬───┘ └───┬───┘ └───┬───┘
    │          │          │
    └──────────┼──────────┘
               │
    ┌──────────▼──────────┐
    │  Per-Tenant         │
    │  Orchestrator       │
    │  - ERPNext Client   │
    │  - Employee Agents  │
    │  - Workflows        │
    │  - KSA Localization│
    │  - Self-Healing     │
    └─────────────────────┘
```

## Quick Start

### 1. Configure Environment

Edit `agent-setup/.env`:

```env
# ERPNext Configuration
ERPNEXT_BASE_URL=http://localhost:8000
ERPNEXT_API_KEY=your_api_key_here
ERPNEXT_API_SECRET=your_api_secret_here

# Claude API
CLAUDE_API_KEY=your_claude_api_key_here

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Multi-Tenancy
PLATFORM_DB_PATH=platform.db
TENANT_DB_DIR=tenant_databases

# Unified Orchestrator Features
ENABLE_MULTI_TENANT=true
ENABLE_AUTONOMOUS_WORKFLOWS=true
ENABLE_SELF_HEALING=true
ENABLE_EMAIL_PROCESSING=true
ENABLE_EMPLOYEE_AGENTS=true
ENABLE_KSA_LOCALIZATION=true
ENABLE_MONITORING=true
```

### 2. Start Unified System

**Windows:**
```powershell
cd agent-setup
.\start-unified.ps1
```

**Linux/Mac:**
```bash
cd agent-setup
chmod +x start-unified.sh
./start-unified.sh
```

**Or directly:**
```bash
cd agent-setup
python unified-orchestrator.py
```

### 3. Start API Gateway (Optional)

The API gateway integrates with the unified orchestrator:

```bash
cd agent-setup
python api-gateway.py
```

Or with uvicorn:
```bash
uvicorn api-gateway:app --host 0.0.0.0 --port 8006
```

## System Components

### 1. Unified Orchestrator (`unified-orchestrator.py`)

**Main entry point** that coordinates all systems:

- **Multi-tenant management**: Creates and manages tenant orchestrators
- **Per-tenant isolation**: Each tenant has its own orchestrator
- **Employee agents**: Uses employee-style agents per tenant
- **KSA localization**: Applies KSA settings (timezone, currency, calendar)
- **Autonomous workflows**: Runs workflows per tenant
- **Self-healing**: Monitors and fixes issues per tenant

**Key Classes:**
- `UnifiedOrchestrator`: Main orchestrator
- `TenantOrchestrator`: Per-tenant orchestrator

### 2. Tenant Orchestrator

Each tenant has its own orchestrator that manages:
- ERPNext client connection
- Employee agents
- Autonomous workflows
- Email processing
- Self-healing
- KSA localization

### 3. API Gateway (`api-gateway.py`)

REST API that:
- Routes requests to tenants
- Integrates with unified orchestrator
- Provides system status endpoints
- Tracks usage and metrics

## Integration Points

### Employee Agents Integration

Employee agents are automatically created per tenant with:
- Employee-style names (e.g., "Ahmed Al-Saud - Sales Manager")
- Roles and departments
- Teams and hierarchy
- KSA localization applied

**Example:**
```python
from unified_orchestrator import UnifiedOrchestrator, UnifiedSystemConfig
from employee_agent_system import EmployeeAgentSystem

# Get tenant orchestrator
orchestrator = unified_orchestrator.get_or_create_tenant_orchestrator(tenant_id)

# Create employee agent
agent = unified_orchestrator.employee_agent_system.create_agent(
    tenant_id=tenant_id,
    employee_name="Ahmed Al-Saud",
    role="Sales Manager",
    department="Sales"
)
```

### KSA Localization Integration

KSA localization is automatically applied to:
- Workflow schedules (KSA timezone)
- Currency formatting (SAR)
- Calendar (Hijri support)
- Business week (Saturday-Wednesday)

**Example:**
```python
# Localization is automatically loaded per tenant
localization = unified_orchestrator.ksa_localization.get_localization(tenant_id)
# Returns: KSALocalization with locale="ar_SA", timezone="Asia/Riyadh", currency="SAR"
```

### Autonomous Workflows Integration

Workflows are automatically initialized per tenant with:
- KSA-aware schedules
- Tenant-specific ERPNext connections
- Employee agent integration

**Workflows included:**
- Auto-process emails (every 15 minutes)
- Auto-send quotations (on quotation_created event)
- Auto-send invoices (on invoice_created event)
- Auto-follow-up (daily at 9:00 AM KSA time)

### Multi-Tenant Integration

Each tenant has:
- Separate database
- Isolated data
- Independent ERPNext connection
- Own employee agents
- Own workflows

## API Endpoints

### System Status

```bash
# Get unified system status
GET /api/v1/system/status

# Get tenant orchestrator status
GET /api/v1/{tenant_id}/orchestrator/status
```

### Tenant Management

```bash
# Create tenant
POST /api/admin/tenants

# List tenants
GET /api/admin/tenants

# Get tenant info
GET /api/v1/tenant/info

# Get tenant quota
GET /api/v1/tenant/quota
```

## Usage Examples

### Create Tenant and Start Orchestrator

```python
from unified_orchestrator import UnifiedOrchestrator, UnifiedSystemConfig
from tenant_manager import TenantManager

# Initialize
config = UnifiedSystemConfig(
    platform_db_path="platform.db",
    tenant_db_dir="tenant_databases",
    default_erpnext_url="http://localhost:8000",
    default_erpnext_api_key="your_key",
    default_erpnext_api_secret="your_secret",
    claude_api_key="your_claude_key"
)

orchestrator = UnifiedOrchestrator(config)

# Create tenant
tenant = orchestrator.tenant_manager.create_tenant(
    name="Acme Corp",
    subdomain="acme",
    subscription_tier="professional"
)

# Provision tenant (creates database, agents, workflows)
orchestrator.tenant_provisioner.provision_tenant(tenant)

# Start unified system (starts all tenant orchestrators)
orchestrator.start()

# Get tenant orchestrator
tenant_orch = orchestrator.get_or_create_tenant_orchestrator(tenant.tenant_id)
```

### Create Employee Agent

```python
# Create employee agent for tenant
agent = orchestrator.employee_agent_system.create_agent(
    tenant_id=tenant.tenant_id,
    employee_name="Ahmed Al-Saud",
    role="Sales Manager",
    department="Sales",
    capabilities=["customer_management", "quotation"]
)
```

### Trigger Workflow

```python
# Get tenant orchestrator
tenant_orch = orchestrator.get_or_create_tenant_orchestrator(tenant_id)

# Trigger workflow
tenant_orch.workflow_engine.trigger_workflow(
    workflow_id=f"auto_send_quotation_{tenant_id}",
    trigger_data={"quotation_name": "QTN-001"}
)
```

## Configuration

### Unified System Config

```python
@dataclass
class UnifiedSystemConfig:
    platform_db_path: str = "platform.db"
    tenant_db_dir: str = "tenant_databases"
    default_erpnext_url: Optional[str] = None
    default_erpnext_api_key: Optional[str] = None
    default_erpnext_api_secret: Optional[str] = None
    default_email_smtp_server: Optional[str] = None
    default_email_smtp_port: int = 587
    default_email_username: Optional[str] = None
    default_email_password: Optional[str] = None
    claude_api_key: Optional[str] = None
    enable_multi_tenant: bool = True
    enable_autonomous_workflows: bool = True
    enable_self_healing: bool = True
    enable_email_processing: bool = True
    enable_employee_agents: bool = True
    enable_ksa_localization: bool = True
    enable_monitoring: bool = True
    auto_provision_new_tenants: bool = True
    default_subscription_tier: str = "starter"
```

## Monitoring

### System Status

```python
status = orchestrator.get_system_status()
# Returns:
# {
#   "status": "running",
#   "uptime_seconds": 3600,
#   "tenants": {
#     "total": 3,
#     "statuses": {...}
#   },
#   "features": {...}
# }
```

### Tenant Status

```python
tenant_status = tenant_orch.get_status()
# Returns:
# {
#   "tenant_id": "...",
#   "tenant_name": "...",
#   "status": "running",
#   "localization": {
#     "locale": "ar_SA",
#     "timezone": "Asia/Riyadh",
#     "currency": "SAR"
#   },
#   "workflows": {...},
#   "agents": {...}
# }
```

## Troubleshooting

### Issue: Tenant orchestrator not starting

**Solution:**
1. Check ERPNext configuration for tenant
2. Verify tenant database exists
3. Check logs for errors

### Issue: Employee agents not working

**Solution:**
1. Verify `enable_employee_agents=True` in config
2. Check tenant isolation is working
3. Verify employee agent system is initialized

### Issue: KSA localization not applied

**Solution:**
1. Verify `enable_ksa_localization=True` in config
2. Check KSA localization is loaded for tenant
3. Verify timezone settings

## Next Steps

1. **Deploy to Production**: Use Docker Compose or Kubernetes
2. **Add More Tenants**: Create additional tenants via API
3. **Customize Workflows**: Add tenant-specific workflows
4. **Monitor System**: Use metrics collector and monitoring dashboard
5. **Scale Horizontally**: Use distributed system components

## Files Created

- `unified-orchestrator.py`: Main unified orchestrator
- `start-unified.ps1`: Windows startup script
- `start-unified.sh`: Linux/Mac startup script
- `api-gateway.py`: Updated with unified orchestrator integration
- `UNIFIED_SYSTEM_INTEGRATION.md`: This guide

## Summary

✅ **All components integrated**
✅ **Multi-tenant support**
✅ **Employee agents with KSA context**
✅ **Autonomous workflows per tenant**
✅ **Unified startup and management**
✅ **API gateway integration**

The system is now fully integrated and ready for production use!
