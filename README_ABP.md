# ABP MVC Application - Quick Start

## ✅ What's Built

**ABP MVC Application** with **Entity Framework Core** as the **Imperial App Shell** with 4 business modules:

1. **ERPNext Management** - Manage ERPNext instances
2. **Tenant Management** - Multi-tenant SaaS platform
3. **Multi-Agent Orchestrator** - Employee agent management
4. **Subscription Management** - Billing and subscriptions

## Quick Start

### 1. Prerequisites

- .NET 8.0 SDK
- SQL Server (LocalDB or full instance)
- Visual Studio 2022 or VS Code

### 2. Restore Packages

```bash
dotnet restore
```

### 3. Configure Database

Edit `src/DoganSystem.Web.Mvc/appsettings.json`:

```json
{
  "ConnectionStrings": {
    "Default": "Server=(localdb)\\mssqllocaldb;Database=DoganSystemDb;Trusted_Connection=True;TrustServerCertificate=True"
  }
}
```

### 4. Create Database

```bash
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add Initial --startup-project ../DoganSystem.Web.Mvc
dotnet ef database update --startup-project ../DoganSystem.Web.Mvc
```

### 5. Run Application

```bash
cd src/DoganSystem.Web.Mvc
dotnet run
```

Access: `https://localhost:5001`

## Architecture

```
ABP MVC Shell (Layer 1)
    │
    ├── ERPNext Module
    ├── Tenant Management Module
    ├── Agent Orchestrator Module
    └── Subscription Module
```

## Integration

- **Python Orchestrator**: `http://localhost:8006`
- **ERPNext API**: `http://localhost:8000`
- **Database**: SQL Server

## Documentation

- `ABP_MVC_SETUP.md` - Detailed setup guide
- `ABP_ARCHITECTURE.md` - Architecture details
- `ABP_BUILD_SUMMARY.md` - Build summary
