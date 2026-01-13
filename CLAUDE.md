# CLAUDE.md - AI Assistant Guide for DoganSystem

This document provides essential context for AI assistants working on the DoganSystem codebase.

## Project Overview

**DoganSystem** is a multi-tenant SaaS platform for enterprise resource management with AI-powered agent orchestration. It integrates with ERPNext and provides subscription management, tenant isolation, and autonomous workflow capabilities.

### Key Business Features
- Multi-tenant architecture with complete tenant isolation
- AI agent orchestration for automated business workflows
- ERPNext v16.2 integration for ERP functionality
- Subscription and billing management
- Bilingual support (Arabic RTL primary, English)

## Architecture

```
DoganSystem/
├── src/                                    # .NET 8 Backend
│   ├── DoganSystem.Web.Mvc/               # ASP.NET Core MVC entry point (port 5000)
│   ├── DoganSystem.Application/           # Application services, DTOs
│   ├── DoganSystem.Core/                  # Domain entities, permissions
│   ├── DoganSystem.EntityFrameworkCore/   # EF Core DbContext, migrations
│   └── DoganSystem.Modules.*/             # Feature modules:
│       ├── AgentOrchestrator/             # AI agent management
│       ├── ErpNext/                       # ERPNext integration
│       ├── Subscription/                  # Billing & subscriptions
│       └── TenantManagement/              # Multi-tenant support
├── frontend/                               # React 18 + Vite frontend (port 3000 dev, 80 prod)
│   ├── src/
│   │   ├── components/                    # Reusable UI components
│   │   ├── pages/                         # Page components (7 main pages)
│   │   ├── services/api.js                # Axios API client
│   │   ├── hooks/useApi.js                # React Query hooks
│   │   └── i18n.js                        # Internationalization
│   └── Dockerfile                         # Multi-stage Node + Nginx
├── docker-compose.yml                     # Container orchestration
├── Dockerfile                             # Backend container
└── deploy.sh                              # Production deployment script
```

## Technology Stack

### Backend
- **.NET 8** with ASP.NET Core MVC
- **ABP Framework** (v8.3.4) - Application framework with modules
- **Entity Framework Core 8** - ORM with PostgreSQL/SQLite
- **Serilog** - Structured logging
- **Swagger/Swashbuckle** - API documentation

### Frontend
- **React 18** with Vite 5 build tool
- **TanStack React Query** - Server state management
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client
- **react-i18next** - Internationalization
- **Vitest** - Testing framework

### DevOps
- **Docker** - Multi-stage containerization
- **Nginx** - Frontend serving with API proxy
- **GitHub Actions** - CI/CD pipeline

## Development Commands

### Frontend (`/frontend`)
```bash
npm install          # Install dependencies
npm run dev          # Start dev server (localhost:3000, proxies to :8006)
npm run build        # Production build to dist/
npm run lint         # ESLint code analysis
npm run lint:fix     # Auto-fix linting issues
npm run format       # Prettier formatting
npm run test         # Run tests (watch mode)
npm run test:ci      # CI test run (verbose)
npm run coverage     # Generate coverage report
npm run quality      # Full quality check (lint + format + test)
```

### Backend (`/src/DoganSystem.Web.Mvc`)
```bash
dotnet restore       # Restore NuGet packages
dotnet build         # Build solution
dotnet run           # Run dev server (localhost:5000)
dotnet publish -c Release -o ./publish   # Production build
```

### Database Migrations
```bash
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add <MigrationName> --startup-project ../DoganSystem.Web.Mvc
dotnet ef database update --startup-project ../DoganSystem.Web.Mvc
```

### Docker
```bash
docker-compose up -d     # Start all services
docker-compose logs -f   # View logs
docker-compose down      # Stop services
./deploy.sh              # Full production deployment
```

## Code Conventions

### Frontend
- **Components**: PascalCase (e.g., `HomePage.jsx`, `Sidebar.jsx`)
- **Hooks**: camelCase with `use` prefix (e.g., `useApi.js`, `useTenants`)
- **Services**: camelCase (e.g., `api.js`)
- **Path aliases**: `@/`, `@components/`, `@pages/`, `@hooks/`, `@services/`
- **Styling**: Tailwind CSS utility classes
- **State**: React Query for server state, useState for local state

### Backend
- **Naming**: ABP conventions (AppServices, Entities, DTOs)
- **Module structure**: Each feature in `DoganSystem.Modules.{FeatureName}`
- **API routes**: RESTful at `/api/{resource}`
- **Permissions**: Defined in `DoganSystem.Core/Permissions`

### Code Quality
- ESLint with React/JSX-a11y rules
- Prettier with 2-space indent, single quotes, 100 char width
- Pre-commit hooks via Husky for lint-staged

## Key Entry Points

### Backend
| File | Purpose |
|------|---------|
| `src/DoganSystem.Web.Mvc/Program.cs` | Application startup |
| `src/DoganSystem.Web.Mvc/appsettings.json` | Configuration |
| `src/DoganSystem.Web.Mvc/Controllers/` | API controllers |
| `src/DoganSystem.EntityFrameworkCore/DoganSystemDbContext.cs` | Database context |

### Frontend
| File | Purpose |
|------|---------|
| `frontend/src/main.jsx` | React entry point |
| `frontend/src/App.jsx` | Root component with routing |
| `frontend/src/services/api.js` | All API client functions |
| `frontend/src/hooks/useApi.js` | React Query hooks |
| `frontend/vite.config.js` | Build configuration |

## API Endpoints

### Core APIs
- `GET /api/system/status` - Health check
- `GET/POST/PUT/DELETE /api/tenants` - Tenant management
- `GET/POST/PUT/DELETE /api/agents` - Agent management
- `GET/POST/PUT/DELETE /api/erpnext` - ERPNext instances
- `GET/POST /api/subscriptions` - Subscription management

### Testing Endpoints
- `POST /api/erpnext/{instanceId}/test-connection` - Test ERPNext connection

## Testing

### Frontend Testing
- **Framework**: Vitest with React Testing Library
- **Config**: `frontend/vitest.config.js`
- **Coverage**: v8 provider with LCOV output

### Test Files Location
```
frontend/src/
├── components/Layout/
│   ├── Header.test.jsx
│   ├── Sidebar.test.jsx
│   └── Layout.test.jsx
└── test/
    └── setup.js       # Global test setup
```

## Configuration Files

### Critical Configs
| File | Purpose |
|------|---------|
| `src/DoganSystem.Web.Mvc/appsettings.json` | Backend settings (DB, SMTP, ERPNext) |
| `frontend/vite.config.js` | Frontend build config with path aliases |
| `frontend/nginx.conf` | Production Nginx config with API proxy |
| `docker-compose.yml` | Container orchestration |
| `.env.production` | Environment variables template |

### Environment Variables (Required for Production)
```bash
CLAUDE_API_KEY=         # Claude AI API key
ERPNEXT_URL=            # ERPNext server URL
ERPNEXT_API_KEY=        # ERPNext API credentials
SMTP_HOST=              # Email server
DB_CONNECTION_STRING=   # PostgreSQL connection
```

## Common AI Assistant Tasks

### Adding a New Page
1. Create page component in `frontend/src/pages/`
2. Add route in `frontend/src/App.jsx`
3. Add navigation link in `frontend/src/components/Layout/Sidebar.jsx`
4. Add translations in `frontend/src/i18n.js` (both AR and EN)

### Adding a New API Endpoint
1. Create/update controller in `src/DoganSystem.Web.Mvc/Controllers/`
2. Add AppService in appropriate module under `src/DoganSystem.Modules.*/`
3. Add DTOs in the Application layer
4. Update frontend API client in `frontend/src/services/api.js`
5. Add React Query hook in `frontend/src/hooks/useApi.js`

### Adding a New Feature Module
1. Create new project `DoganSystem.Modules.{FeatureName}`
2. Add project reference in `DoganSystem.Web.Mvc.csproj`
3. Register module in `DoganSystemWebMvcModule.cs`
4. Create DbContext extensions if needed

### Running Quality Checks Before PR
```bash
cd frontend && npm run quality   # Lint + format + tests
cd src/DoganSystem.Web.Mvc && dotnet build   # Backend compilation
```

## Localization

The system uses Arabic (ar) as the primary language with English (en) support.

### Adding Translations
- Frontend: Update `frontend/src/i18n.js` with both `ar` and `en` keys
- Backend: Update resources in `src/DoganSystem.Core/Localization/`

### RTL Support
- Arabic layout is RTL (right-to-left)
- Tailwind RTL classes are available
- Language toggle is in the Header component

## Documentation Index

| Document | Purpose |
|----------|---------|
| `BUILD_AND_DEPLOY.md` | Detailed build instructions |
| `QUICK_DEPLOY.md` | Fast Docker deployment |
| `frontend/ARCHITECTURE.md` | Frontend design patterns |
| `frontend/CODE_QUALITY.md` | Code standards |
| `ABP_ARCHITECTURE.md` | Backend framework details |
| `DATABASE_SETUP.md` | Database configuration |

## Git Workflow

- **main**: Production code
- **develop**: Staging/integration
- **claude/**: AI assistant feature branches

### Commit Message Format
Conventional commits style:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation
- `chore:` Maintenance
- `refactor:` Code restructuring

## Troubleshooting

### Common Issues

1. **Frontend proxy not working**
   - Check `vite.config.js` proxy settings
   - Ensure backend is running on port 5000

2. **Database migrations fail**
   - Ensure DbContext is properly configured
   - Run from EntityFrameworkCore directory with startup project flag

3. **Docker build fails**
   - Check .NET SDK version (requires 8.0)
   - Verify Node version (18.x or 20.x)

4. **Tests failing**
   - Run `npm run lint:fix` for auto-fixable issues
   - Check test setup in `frontend/src/test/setup.js`

## Security Notes

- Never commit `.env` files with secrets
- API keys should be in environment variables
- Docker runs as non-root user
- CORS is configured in `appsettings.json`
- Security headers set in `nginx.conf`
