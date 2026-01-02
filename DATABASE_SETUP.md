# Database Setup and Migration Guide

## Quick Start

### Option 1: Using PowerShell Scripts (Recommended)

1. **Create Migration**:
   ```powershell
   .\create-migration.ps1
   ```

2. **Apply Migration**:
   ```powershell
   .\apply-migration.ps1
   ```

### Option 2: Manual Commands

1. **Install EF Core Tools** (if not already installed):
   ```bash
   dotnet tool install --global dotnet-ef
   ```

2. **Create Migration**:
   ```bash
   cd src/DoganSystem.EntityFrameworkCore
   dotnet ef migrations add Initial --startup-project ../DoganSystem.Web.Mvc --context DoganSystemDbContext
   ```

3. **Apply Migration**:
   ```bash
   dotnet ef database update --startup-project ../DoganSystem.Web.Mvc --context DoganSystemDbContext
   ```

## Prerequisites

### 1. SQL Server
- **LocalDB** (for development): Usually pre-installed with Visual Studio
- **Full SQL Server** (for production): SQL Server 2019+ or SQL Server Express

### 2. Connection String

Default connection string in `appsettings.json`:
```json
{
  "ConnectionStrings": {
    "Default": "Server=(localdb)\\mssqllocaldb;Database=DoganSystemDb;Trusted_Connection=True;TrustServerCertificate=True"
  }
}
```

**For Production**, update `appsettings.Production.json`:
```json
{
  "ConnectionStrings": {
    "Default": "Server=YOUR_SERVER;Database=DoganSystemDb;User Id=YOUR_USER;Password=YOUR_PASSWORD;TrustServerCertificate=True"
  }
}
```

## Database Schema

The migration creates the following tables:

### ABP Framework Core Tables
- `AbpUsers` - User accounts
- `AbpRoles` - Roles
- `AbpUserRoles` - User-Role mappings
- `AbpRoleClaims` - Role claims
- `AbpUserClaims` - User claims
- `AbpUserLogins` - External login providers
- `AbpUserTokens` - User tokens
- `AbpPermissionGrants` - Permission grants (for GRC permissions)
- `AbpSettings` - Application settings
- `AbpAuditLogs` - Audit logs
- `AbpFeatureValues` - Feature flags

### Business Module Tables
- `Tenants` - Multi-tenant tenant records
  - Indexes: Subdomain (unique), Domain, Status
- `ErpNextInstances` - ERPNext integration instances
  - Indexes: TenantId
- `EmployeeAgents` - Employee agent records
  - Indexes: TenantId, TeamId, ManagerId
- `Subscriptions` - Subscription management
  - Indexes: TenantId, Status

## Verification

### 1. Check Migration Files

After creating migration, verify:
- `src/DoganSystem.EntityFrameworkCore/Migrations/YYYYMMDDHHMMSS_Initial.cs` exists
- Migration includes all entities
- Migration includes Identity tables

### 2. Verify Database

After applying migration, check database:

```sql
USE DoganSystemDb;
GO

-- List all tables
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
GO

-- Check Identity tables
SELECT COUNT(*) as UserCount FROM AbpUsers;
SELECT COUNT(*) as RoleCount FROM AbpRoles;
GO

-- Check business tables
SELECT COUNT(*) as TenantCount FROM Tenants;
SELECT COUNT(*) as AgentCount FROM EmployeeAgents;
GO
```

### 3. Test Application

1. **Run Application**:
   ```bash
   cd src/DoganSystem.Web.Mvc
   dotnet run
   ```

2. **Check Logs** for:
   - Role seeding confirmation (GrcRoleDataSeedContributor)
   - Database connection success
   - No migration errors

3. **Verify Roles Created**:
   - SuperAdmin
   - TenantAdmin
   - ComplianceManager
   - RiskManager
   - Auditor
   - EvidenceOfficer
   - VendorManager
   - Viewer

## Troubleshooting

### Issue: "dotnet-ef command not found"

**Solution**:
```bash
dotnet tool install --global dotnet-ef
# Restart terminal/PowerShell
```

### Issue: "Cannot connect to database"

**Solutions**:
1. **Check SQL Server is running**:
   ```powershell
   Get-Service -Name "*SQL*" | Where-Object {$_.Status -eq "Running"}
   ```

2. **For LocalDB**, start it:
   ```bash
   sqllocaldb start mssqllocaldb
   ```

3. **Verify connection string** in `appsettings.json`

4. **Test connection**:
   ```bash
   sqlcmd -S "(localdb)\mssqllocaldb" -Q "SELECT @@VERSION"
   ```

### Issue: "Migration already exists"

**Solutions**:
- **If you need to recreate**: Delete migration files and recreate
- **If you need to update**: Create new migration with different name:
  ```bash
  dotnet ef migrations add AddNewFeature --startup-project ../DoganSystem.Web.Mvc
  ```

### Issue: "Build failed"

**Solution**: Fix build errors first:
```bash
dotnet build
```

### Issue: "No DbContext was found"

**Solution**: Ensure you specify the context:
```bash
--context DoganSystemDbContext
```

## Post-Migration Steps

### 1. Verify Role Seeding

On first application startup, `GrcRoleDataSeedContributor` automatically:
- Creates 8 default roles
- Grants permissions to each role
- Logs the seeding process

Check application logs for:
```
Created role: SuperAdmin
Granted X permissions to role: SuperAdmin
...
```

### 2. Create Initial Admin User

You can create an admin user via:
- ABP's built-in user management (if UI is available)
- Direct SQL (for initial setup)
- Application service (programmatically)

### 3. Test Permissions

1. Create test users
2. Assign roles
3. Verify menu items show/hide based on permissions
4. Test API endpoints with different roles

## Additional Migrations

When you modify entities:

```bash
dotnet ef migrations add MigrationName --startup-project ../DoganSystem.Web.Mvc --context DoganSystemDbContext
```

**Always review** the generated migration before applying!

## Rollback

### Rollback Last Migration
```bash
dotnet ef database update PreviousMigrationName --startup-project ../DoganSystem.Web.Mvc
```

### Remove Last Migration (without applying)
```bash
dotnet ef migrations remove --startup-project ../DoganSystem.Web.Mvc
```

## Production Deployment

### Before Production:

1. **Backup Database**:
   ```sql
   BACKUP DATABASE DoganSystemDb TO DISK = 'C:\Backups\DoganSystemDb.bak'
   ```

2. **Test Migration on Staging** first

3. **Review Migration Script** carefully

4. **Apply During Maintenance Window**

5. **Verify After Migration**:
   - Check all tables exist
   - Verify data integrity
   - Test critical functionality

### Production Connection String

Use secure connection string with:
- Encrypted credentials
- Connection pooling
- Timeout settings
- Retry logic

Example:
```json
{
  "ConnectionStrings": {
    "Default": "Server=PROD_SERVER;Database=DoganSystemDb;User Id=app_user;Password=***;TrustServerCertificate=True;Connection Timeout=30;Pooling=true;Max Pool Size=100;"
  }
}
```

---

**Status**: ✅ Ready for migration creation and database setup

**Next**: Run `.\create-migration.ps1` to create the initial migration
