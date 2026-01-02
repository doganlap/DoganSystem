# ABP MVC Application Setup Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│         ABP MVC Application Shell               │
│         (Imperial App Shell)                    │
│  - DoganSystem.Web.Mvc                          │
│  - Main UI & Controllers                        │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼───┐ ┌──────▼───┐ ┌─────▼────┐
│ ERPNext   │ │ Tenant   │ │ Agent    │
│ Module    │ │ Mgmt      │ │ Orchestr │
└───────────┘ └───────────┘ └──────────┘
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────▼────────────┐
        │  Subscription Module     │
        └─────────────────────────┘
```

## Project Structure

```
DoganSystem/
├── src/
│   ├── DoganSystem.Core/              # Core domain entities
│   ├── DoganSystem.Application/       # Application services
│   ├── DoganSystem.EntityFrameworkCore/  # EF Core configuration
│   ├── DoganSystem.Web.Mvc/           # MVC Web Application (Shell)
│   ├── DoganSystem.Modules.ErpNext/   # ERPNext Management Module
│   ├── DoganSystem.Modules.TenantManagement/  # Tenant Management
│   ├── DoganSystem.Modules.AgentOrchestrator/  # Multi-Agent Orchestrator
│   └── DoganSystem.Modules.Subscription/      # Subscription Management
└── test/
```

## Prerequisites

- .NET 8.0 SDK
- Visual Studio 2022 or VS Code
- SQL Server (LocalDB or full instance)
- ABP CLI (optional): `dotnet tool install -g Volo.Abp.Cli`

## Installation Steps

### 1. Install ABP Framework

```bash
# Install ABP CLI
dotnet tool install -g Volo.Abp.Cli

# Or use NuGet packages directly (already in .csproj files)
```

### 2. Configure Database

Edit `appsettings.json` in `DoganSystem.Web.Mvc`:

```json
{
  "ConnectionStrings": {
    "Default": "Server=(localdb)\\mssqllocaldb;Database=DoganSystemDb;Trusted_Connection=True;TrustServerCertificate=True"
  }
}
```

### 3. Run Migrations

```bash
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add Initial
dotnet ef database update
```

### 4. Run Application

```bash
cd src/DoganSystem.Web.Mvc
dotnet run
```

Access: `https://localhost:5001` or `http://localhost:5000`

## Module Integration

### ERPNext Module
- Manages ERPNext instances
- Connects to ERPNext APIs
- Syncs data between systems

### Tenant Management Module
- Multi-tenant support
- Tenant isolation
- Tenant provisioning

### Agent Orchestrator Module
- Manages employee agents
- Integrates with Python orchestrator service
- Agent delegation and teams

### Subscription Module
- Subscription plans
- Billing management
- Payment integration

## Integration with Python Services

The ABP MVC application integrates with existing Python services:

1. **Agent Orchestrator Service** (Python)
   - URL: `http://localhost:8006` (API Gateway)
   - Called via HTTP from Agent Orchestrator module

2. **ERPNext** (Python/Frappe)
   - URL: `http://localhost:8000`
   - Managed via ERPNext module

## Next Steps

1. ✅ Create Entity Framework configurations for each module
2. ✅ Create Application Services
3. ✅ Create Controllers and Views
4. ✅ Integrate with Python services
5. ✅ Add authentication and authorization
6. ✅ Create admin dashboard
