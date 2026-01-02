# DoganSystem - Multi-Tenant SaaS Platform

## 🚀 Quick Start

**Ready to build and deploy!** See:
- **`QUICK_START.md`** - Get running in 5 minutes
- **`BUILD_AND_DEPLOY.md`** - Complete deployment guide
- **`BUILD_READY.md`** - Current build status

## 📋 Build Status

✅ **Code Complete** - All features implemented
⚠️ **Build Pending** - Requires NuGet package restore (needs internet access)

## 🏗️ Quick Build

```powershell
# Windows
.\build.ps1

# Or manually
dotnet restore
dotnet build DoganSystem.sln --configuration Release
```

## 📚 Documentation

- `QUICK_START.md` - Fastest way to get running
- `BUILD_AND_DEPLOY.md` - Full deployment instructions
- `BUILD_TROUBLESHOOTING.md` - Fix common issues
- `APP_COMPLETION_SUMMARY.md` - What's been implemented
- `BUILD_READY.md` - Current status and next steps

---

# DoganSystem - Multi-Tenant SaaS Platform

Complete multi-tenant SaaS platform with ERPNext integration, multi-agent AI orchestration, and subscription management.

## 🚀 Features

- **Multi-Tenant Architecture** - Complete tenant isolation and management
- **ERPNext Integration** - Manage multiple ERPNext instances
- **Multi-Agent AI System** - Employee-style agents with Claude AI
- **Subscription Management** - Billing and subscription lifecycle
- **KSA Localization** - Arabic language, timezone, currency support
- **Autonomous Workflows** - Self-healing and automated processes
- **ABP MVC Framework** - Modern .NET application shell

## 📋 Prerequisites

- .NET 8.0 SDK
- SQL Server (LocalDB or full instance)
- Python 3.10+ (for agent orchestrator)
- Node.js 18+ (for ERPNext)
- ERPNext v16 (optional, can be installed separately)

## 🏗️ Architecture

```
ABP MVC Application Shell (Layer 1)
├── ERPNext Management Module
├── Tenant Management Module
├── Multi-Agent Orchestrator Module
└── Subscription Management Module

Python Services (Layer 2)
├── Unified Orchestrator
├── Employee Agent System
├── Autonomous Workflows
└── KSA Localization
```

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/doganlap/DoganSystem.git
cd DoganSystem
```

### 2. Setup ABP MVC Application

```bash
# Restore packages
dotnet restore

# Create database migration
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add Initial --startup-project ../DoganSystem.Web.Mvc

# Update database
dotnet ef database update --startup-project ../DoganSystem.Web.Mvc
```

### 3. Configure Application

Edit `src/DoganSystem.Web.Mvc/appsettings.json`:

```json
{
  "ConnectionStrings": {
    "Default": "Server=(localdb)\\mssqllocaldb;Database=DoganSystemDb;Trusted_Connection=True;TrustServerCertificate=True"
  },
  "PythonServices": {
    "OrchestratorUrl": "http://localhost:8006"
  }
}
```

### 4. Run ABP MVC Application

```bash
cd src/DoganSystem.Web.Mvc
dotnet run
```

Access: `https://localhost:5001`

### 5. Setup Python Services (Optional)

```bash
cd agent-setup

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your API keys

# Start unified orchestrator
python unified-orchestrator.py
```

## 📚 Documentation

- [ABP MVC Setup Guide](ABP_MVC_SETUP.md)
- [Complete Implementation Guide](COMPLETE_IMPLEMENTATION.md)
- [Unified System Integration](UNIFIED_SYSTEM_INTEGRATION.md)
- [ERPNext Setup Guide](README.md#erpnext-setup)

## 🏛️ Project Structure

```
DoganSystem/
├── src/                          # ABP MVC Application
│   ├── DoganSystem.Core/
│   ├── DoganSystem.Application/
│   ├── DoganSystem.EntityFrameworkCore/
│   ├── DoganSystem.Web.Mvc/
│   └── DoganSystem.Modules.*/
├── agent-setup/                  # Python Services
│   ├── unified-orchestrator.py
│   ├── employee-agent-system.py
│   └── ...
├── frontend/                     # React Frontend (optional)
└── Documentation/
```

## 🔌 API Endpoints

### Tenants
- `GET /api/tenants` - List tenants
- `POST /api/tenants` - Create tenant
- `GET /api/tenants/{id}` - Get tenant
- `PUT /api/tenants/{id}` - Update tenant
- `DELETE /api/tenants/{id}` - Delete tenant

### ERPNext Instances
- `GET /api/erpnext` - List instances
- `POST /api/erpnext` - Create instance
- `POST /api/erpnext/{id}/test-connection` - Test connection

### Employee Agents
- `GET /api/agents` - List agents
- `POST /api/agents` - Create agent
- `PUT /api/agents/{id}` - Update agent

### Subscriptions
- `GET /api/subscriptions` - List subscriptions
- `POST /api/subscriptions` - Create subscription
- `POST /api/subscriptions/{id}/cancel` - Cancel subscription

## 🧪 Testing

```bash
# Run ABP application tests (when available)
dotnet test

# Test Python services
cd agent-setup
python test_tenant_system.py
```

## 📦 Technologies

- **Backend**: ABP Framework 8.0, .NET 8.0, Entity Framework Core
- **Python Services**: FastAPI, Python 3.10+
- **Database**: SQL Server / SQLite
- **Frontend**: React + Vite (optional)
- **AI**: Anthropic Claude API

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Dogan System Team**

## 🙏 Acknowledgments

- ABP Framework
- ERPNext Community
- Anthropic Claude

## 📞 Support

For support, email support@dogansystem.com or open an issue in the repository.

---

**Built with ❤️ for Multi-Tenant SaaS Platforms**
