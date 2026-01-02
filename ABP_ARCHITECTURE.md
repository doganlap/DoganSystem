# ABP MVC Architecture - DoganSystem

## Overview

**ABP MVC Application** serves as the **Imperial App Shell** (main application framework) with **Entity Framework Core** for data persistence.

## Architecture Layers

### Layer 1: Application Shell (ABP MVC)
- **DoganSystem.Web.Mvc** - Main MVC application
- **DoganSystem.Core** - Core domain entities
- **DoganSystem.Application** - Application services
- **DoganSystem.EntityFrameworkCore** - EF Core configuration

### Layer 2: Business Modules

#### 1. ERPNext Management Module
- **Purpose**: Manage ERPNext instances and connections
- **Entities**: `ErpNextInstance`
- **Features**:
  - Create/Update/Delete ERPNext instances
  - Manage API keys and connections
  - Sync data with ERPNext

#### 2. Tenant Management Module
- **Purpose**: Multi-tenant SaaS platform management
- **Entities**: `Tenant`
- **Features**:
  - Tenant CRUD operations
  - Tenant provisioning
  - Tenant isolation
  - Subdomain/Domain management

#### 3. Multi-Agent Orchestrator Module
- **Purpose**: Manage employee agents and orchestration
- **Entities**: `EmployeeAgent`
- **Features**:
  - Employee agent management
  - Agent delegation
  - Teams and hierarchy
  - Integration with Python orchestrator service

#### 4. Subscription Management Module
- **Purpose**: Manage subscriptions and billing
- **Entities**: `Subscription`
- **Features**:
  - Subscription plans (Starter, Professional, Enterprise)
  - Billing management
  - Payment integration
  - Usage tracking

## Integration Points

### Python Services Integration

The ABP MVC application integrates with existing Python services:

```
ABP MVC Application
    │
    ├─── Agent Orchestrator Module
    │    └─── HTTP Calls ──► Python Orchestrator Service (port 8006)
    │
    ├─── ERPNext Module
    │    └─── HTTP Calls ──► ERPNext API (port 8000)
    │
    └─── Tenant Management Module
         └─── Database ──► SQL Server (LocalDB/Full)
```

### Data Flow

1. **User Action** → ABP MVC Controller
2. **Controller** → Application Service
3. **Application Service** → 
   - Save to SQL Server (via EF Core)
   - Call Python service (via HTTP)
4. **Python Service** → Process and return
5. **Response** → Return to user

## Database Schema

### Tables

- **ErpNextInstances** - ERPNext instance configurations
- **Tenants** - Tenant information
- **EmployeeAgents** - Employee agent data
- **Subscriptions** - Subscription and billing data

## Module Structure

Each module follows ABP framework conventions:

```
ModuleName/
├── Domain/              # Domain entities
├── Application/         # Application services
├── EntityFrameworkCore/ # EF Core configurations
└── Web/                 # Controllers and Views (if needed)
```

## Next Steps

1. ✅ Create Entity Framework configurations
2. ✅ Create Application Services
3. ⏳ Create Controllers
4. ⏳ Create Views
5. ⏳ Add authentication
6. ⏳ Integrate with Python services
7. ⏳ Create admin dashboard

## Running the Application

```bash
# Restore packages
dotnet restore

# Run migrations
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add Initial
dotnet ef database update

# Run application
cd ../DoganSystem.Web.Mvc
dotnet run
```

Access: `https://localhost:5001`
