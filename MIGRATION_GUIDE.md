# Database Migration Guide

## Prerequisites

1. **SQL Server** (LocalDB or full instance)
   - Connection string configured in `appsettings.json`
   - Default: `(localdb)\mssqllocaldb`

2. **EF Core Tools** installed:
   ```bash
   dotnet tool install --global dotnet-ef
   ```

## Creating Migrations

### Step 1: Create Initial Migration

From the solution root:
```bash
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add Initial --startup-project ../DoganSystem.Web.Mvc --context DoganSystemDbContext
```

Or using the full path:
```bash
dotnet ef migrations add Initial `
  --project src/DoganSystem.EntityFrameworkCore `
  --startup-project src/DoganSystem.Web.Mvc `
  --context DoganSystemDbContext
```

### Step 2: Review Migration

The migration will be created in:
```
src/DoganSystem.EntityFrameworkCore/Migrations/YYYYMMDDHHMMSS_Initial.cs
```

Review the migration file to ensure:
- All entities are included (Tenants, ErpNextInstances, EmployeeAgents, Subscriptions)
- Identity tables are included (Users, Roles, etc.)
- Indexes are created correctly
- Foreign keys are set up properly

### Step 3: Apply Migration to Database

```bash
dotnet ef database update --startup-project ../DoganSystem.Web.Mvc --context DoganSystemDbContext
```

Or:
```bash
dotnet ef database update `
  --project src/DoganSystem.EntityFrameworkCore `
  --startup-project src/DoganSystem.Web.Mvc `
  --context DoganSystemDbContext
```

## Database Schema

The migration will create the following tables:

### Core Tables (ABP Identity)
- `AbpUsers` - User accounts
- `AbpRoles` - Roles
- `AbpUserRoles` - User-Role mappings
- `AbpRoleClaims` - Role claims
- `AbpUserClaims` - User claims
- `AbpUserLogins` - External login providers
- `AbpUserTokens` - User tokens
- `AbpPermissionGrants` - Permission grants

### Business Module Tables
- `Tenants` - Multi-tenant tenant records
- `ErpNextInstances` - ERPNext integration instances
- `EmployeeAgents` - Employee agent records
- `Subscriptions` - Subscription management

### ABP Framework Tables
- `AbpAuditLogs` - Audit logs
- `AbpSettings` - Application settings
- `AbpFeatureValues` - Feature flags
- `AbpTenants` - ABP tenant management (if using ABP multi-tenancy)

## Connection String

Default connection string in `appsettings.json`:
```json
{
  "ConnectionStrings": {
    "Default": "Server=(localdb)\\mssqllocaldb;Database=DoganSystemDb;Trusted_Connection=True;TrustServerCertificate=True"
  }
}
```

### For Production

Update `appsettings.Production.json`:
```json
{
  "ConnectionStrings": {
    "Default": "Server=YOUR_SERVER;Database=DoganSystemDb;User Id=YOUR_USER;Password=YOUR_PASSWORD;TrustServerCertificate=True"
  }
}
```

## Troubleshooting

### Issue: "dotnet-ef command not found"
**Solution**: Install EF Core tools:
```bash
dotnet tool install --global dotnet-ef
```
Then restart your terminal/PowerShell.

### Issue: "No DbContext was found"
**Solution**: Ensure you specify the context:
```bash
--context DoganSystemDbContext
```

### Issue: "Cannot connect to database"
**Solution**: 
1. Verify SQL Server is running
2. Check connection string in `appsettings.json`
3. Ensure database server allows connections
4. For LocalDB, ensure it's installed and running

### Issue: "Migration already exists"
**Solution**: 
- If you need to recreate: Delete the migration folder and recreate
- If you need to update: Create a new migration with a different name

## Verifying Migration

After applying the migration:

1. **Check Database**:
   ```sql
   USE DoganSystemDb;
   SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
   WHERE TABLE_TYPE = 'BASE TABLE'
   ORDER BY TABLE_NAME;
   ```

2. **Verify Tables**:
   - Should see all tables listed above
   - Check indexes are created
   - Verify foreign key constraints

3. **Test Application**:
   - Run the application
   - Check that role seeding works (GrcRoleDataSeedContributor)
   - Verify you can create tenants, agents, etc.

## Next Steps After Migration

1. **Seed Initial Data**:
   - Roles and permissions are automatically seeded on first startup
   - Check logs for seed confirmation

2. **Create Test Data**:
   - Create a test tenant
   - Create test users
   - Assign roles to users

3. **Verify Permissions**:
   - Test that permissions are correctly assigned
   - Verify menu items show/hide based on permissions

## Creating Additional Migrations

When you modify entities:

```bash
dotnet ef migrations add MigrationName --startup-project ../DoganSystem.Web.Mvc --context DoganSystemDbContext
```

Always review the generated migration before applying!

## Rollback Migration

To rollback the last migration:
```bash
dotnet ef database update PreviousMigrationName --startup-project ../DoganSystem.Web.Mvc --context DoganSystemDbContext
```

To remove the last migration (without applying):
```bash
dotnet ef migrations remove --startup-project ../DoganSystem.Web.Mvc --context DoganSystemDbContext
```

---

**Note**: Always backup your database before applying migrations in production!
