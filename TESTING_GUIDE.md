# Testing Guide - DoganSystem

## Overview

This guide covers testing the complete DoganSystem implementation including:
- GRC Permissions System
- Policy Enforcement Engine
- Database Migrations
- API Endpoints
- Role-Based Access Control

## Pre-Testing Checklist

- [x] ✅ Build successful (0 errors)
- [ ] ⏳ Database migration created and applied
- [ ] ⏳ Application runs without errors
- [ ] ⏳ Roles and permissions seeded
- [ ] ⏳ Test users created

## 1. Database Setup

### Step 1: Create Migration
```powershell
.\create-migration.ps1
```

Or manually:
```bash
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add Initial --startup-project ../DoganSystem.Web.Mvc --context DoganSystemDbContext
```

### Step 2: Apply Migration
```powershell
.\apply-migration.ps1
```

Or manually:
```bash
dotnet ef database update --startup-project ../DoganSystem.Web.Mvc --context DoganSystemDbContext
```

### Step 3: Verify Database
```sql
USE DoganSystemDb;
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME;
```

Should see:
- AbpUsers, AbpRoles, AbpPermissionGrants
- Tenants, ErpNextInstances, EmployeeAgents, Subscriptions

## 2. Application Startup Testing

### Run Application
```bash
cd src/DoganSystem.Web.Mvc
dotnet run
```

### Verify Startup
1. **Check Logs** for:
   - ✅ "Created role: SuperAdmin"
   - ✅ "Granted X permissions to role: SuperAdmin"
   - ✅ Similar messages for all 8 roles
   - ✅ No errors

2. **Access Application**:
   - Open browser: `https://localhost:5001` or `http://localhost:5000`
   - Should see home page

3. **Check Swagger** (Development only):
   - `https://localhost:5001/swagger`
   - Should see all API endpoints

## 3. GRC Permissions Testing

### Test 1: Verify Roles Created

**SQL Query**:
```sql
SELECT Name, Id FROM AbpRoles ORDER BY Name;
```

**Expected**: 8 roles
- SuperAdmin
- TenantAdmin
- ComplianceManager
- RiskManager
- Auditor
- EvidenceOfficer
- VendorManager
- Viewer

### Test 2: Verify Permissions Granted

**SQL Query**:
```sql
SELECT 
    r.Name as RoleName,
    COUNT(pg.Name) as PermissionCount
FROM AbpRoles r
LEFT JOIN AbpPermissionGrants pg ON pg.ProviderName = 'R' AND pg.ProviderKey = r.Name
GROUP BY r.Name
ORDER BY r.Name;
```

**Expected**: Each role should have multiple permissions granted

### Test 3: Permission Structure

**Verify Permission Hierarchy**:
- Grc.Home
- Grc.Dashboard
- Grc.Subscriptions.View, Grc.Subscriptions.Manage
- Grc.Admin.Access, Grc.Admin.Users, Grc.Admin.Roles, Grc.Admin.Tenants
- Grc.Frameworks.View, Grc.Frameworks.Create, etc.
- ... (all 19 menu items)

## 4. Policy Enforcement Testing

### Test 1: Policy Engine Initialization

**Check Logs** on application startup:
- PolicyStore should load `etc/policies/grc-baseline.yml`
- No policy loading errors

### Test 2: Policy Rules

**Test Data Classification Requirement**:
```csharp
// This should fail if dataClassification is missing
var evidence = new Evidence { /* missing dataClassification */ };
await _policyEnforcer.EnforceAsync(new PolicyContext {
    Action = "create",
    ResourceType = "Evidence",
    Resource = evidence,
    Environment = "prod"
});
// Should throw PolicyViolationException
```

### Test 3: Policy Mutations

**Test Owner Normalization**:
```csharp
var resource = new Evidence { Owner = "unknown" };
// After policy enforcement, Owner should be null
```

## 5. API Endpoint Testing

### Test 1: Tenant Management API

**Create Tenant**:
```bash
POST /api/tenants
Content-Type: application/json

{
  "name": "Test Company",
  "subdomain": "testco",
  "subscriptionTier": "Professional",
  "trialDays": 30
}
```

**Expected**: 201 Created with tenant data

**List Tenants**:
```bash
GET /api/tenants?SkipCount=0&MaxResultCount=10
```

**Expected**: 200 OK with tenant list

### Test 2: Agent Management API

**Create Agent**:
```bash
POST /api/agents
Content-Type: application/json

{
  "tenantId": "GUID",
  "employeeName": "John Doe",
  "role": "Sales Manager",
  "department": "Sales"
}
```

**Expected**: 201 Created

### Test 3: ERPNext API

**Test Connection**:
```bash
POST /api/erpnext/{id}/test-connection
```

**Expected**: 200 OK with connection status

### Test 4: Subscription API

**Create Subscription**:
```bash
POST /api/subscriptions
Content-Type: application/json

{
  "tenantId": "GUID",
  "planType": "Professional",
  "startDate": "2025-01-01T00:00:00Z"
}
```

**Expected**: 201 Created with calculated monthly price

## 6. Authorization Testing

### Test 1: Permission-Based Access

**Test with Different Roles**:

1. **Create Test Users**:
   - User1: SuperAdmin role
   - User2: Viewer role
   - User3: EvidenceOfficer role

2. **Test API Access**:
   ```bash
   # As Viewer (should fail)
   POST /api/tenants
   # Expected: 403 Forbidden
   
   # As SuperAdmin (should succeed)
   POST /api/tenants
   # Expected: 201 Created
   ```

### Test 2: Menu Visibility

**Test Menu Items**:
- Viewer should see all menu items (view-only)
- EvidenceOfficer should see Evidence menu
- ComplianceManager should see Frameworks, Regulators, etc.
- SuperAdmin should see everything including Admin menu

## 7. Integration Testing

### Test 1: ERPNext Integration

**Prerequisites**:
- ERPNext instance running (or mock)
- API key configured

**Test**:
```bash
POST /api/erpnext
{
  "name": "Test Instance",
  "baseUrl": "http://localhost:8000",
  "apiKey": "test-key",
  "apiSecret": "test-secret"
}

# Then test connection
POST /api/erpnext/{id}/test-connection
```

### Test 2: Python Service Integration

**Prerequisites**:
- Python orchestrator service running on port 8006

**Test**:
- Create an EmployeeAgent
- Verify sync to Python service (check logs)

## 8. Policy Enforcement Integration

### Test 1: Evidence Creation with Policy

**Test Valid Evidence**:
```csharp
var evidence = new Evidence {
    DataClassification = "internal",
    Owner = "compliance-team",
    // ... other required fields
};
// Should succeed
```

**Test Invalid Evidence** (missing classification):
```csharp
var evidence = new Evidence {
    Owner = "compliance-team",
    // Missing DataClassification
};
// Should throw PolicyViolationException with remediation hint
```

**Test Restricted in Prod**:
```csharp
var evidence = new Evidence {
    DataClassification = "restricted",
    ApprovedForProd = false,
    // In prod environment
};
// Should throw PolicyViolationException
```

## 9. Performance Testing

### Test 1: Policy Evaluation Performance

- Measure time for policy evaluation
- Should be < 100ms per evaluation
- Test with 1000 concurrent requests

### Test 2: Database Performance

- Test tenant listing with 1000+ tenants
- Test agent listing with pagination
- Verify indexes are used (check query plans)

## 10. Security Testing

### Test 1: SQL Injection

**Test**:
```bash
GET /api/tenants?Filter='; DROP TABLE Tenants;--
```

**Expected**: Should be sanitized, no SQL execution

### Test 2: Authorization Bypass

**Test**: Try to access admin endpoints without admin role
**Expected**: 403 Forbidden

### Test 3: Cross-Tenant Data Access

**Test**: User from Tenant A trying to access Tenant B data
**Expected**: Should be filtered by TenantId

## 11. Error Handling Testing

### Test 1: Invalid Input

**Test**:
```bash
POST /api/tenants
{
  "name": "",  // Empty name
  "subdomain": "invalid-subdomain-with-very-long-name-that-exceeds-max-length"
}
```

**Expected**: 400 Bad Request with validation errors

### Test 2: Not Found

**Test**:
```bash
GET /api/tenants/00000000-0000-0000-0000-000000000000
```

**Expected**: 404 Not Found

### Test 3: Policy Violation

**Test**: Create resource violating policy
**Expected**: BusinessException with code "Grc:PolicyViolation" and remediation hint

## 12. Localization Testing

### Test 1: Arabic Menu

- Verify all menu items display in Arabic
- Check menu icons
- Verify menu routing

### Test 2: Permission Names

- Check permission display names (if UI available)
- Should support localization

## Test Results Template

```
## Test Results - [Date]

### Database Migration
- [ ] Migration created successfully
- [ ] Migration applied successfully
- [ ] All tables created
- [ ] Indexes created correctly

### Application Startup
- [ ] Application starts without errors
- [ ] Roles seeded successfully
- [ ] Permissions granted correctly

### API Endpoints
- [ ] Tenant API works
- [ ] Agent API works
- [ ] ERPNext API works
- [ ] Subscription API works

### Authorization
- [ ] Permission-based access works
- [ ] Role-based menu visibility works
- [ ] API authorization works

### Policy Enforcement
- [ ] Policy engine loads correctly
- [ ] Policy rules evaluate correctly
- [ ] Policy violations throw correct exceptions
- [ ] Policy mutations apply correctly

### Integration
- [ ] ERPNext integration works
- [ ] Python service integration works

### Performance
- [ ] Policy evaluation < 100ms
- [ ] API response times acceptable
- [ ] Database queries optimized

### Security
- [ ] SQL injection prevented
- [ ] Authorization enforced
- [ ] Cross-tenant isolation works

## Issues Found
1. [Issue description]
2. [Issue description]

## Next Steps
- [ ] Fix identified issues
- [ ] Re-run failed tests
- [ ] Performance optimization
- [ ] Additional test cases
```

---

## Quick Test Commands

```bash
# Build
dotnet build

# Run application
cd src/DoganSystem.Web.Mvc
dotnet run

# Test API (using curl or Postman)
curl -X GET https://localhost:5001/api/tenants

# Check database
sqlcmd -S "(localdb)\mssqllocaldb" -d DoganSystemDb -Q "SELECT COUNT(*) FROM AbpRoles"
```

---

**Status**: ✅ Ready for comprehensive testing

**Next**: Run database migration, then proceed with testing checklist
