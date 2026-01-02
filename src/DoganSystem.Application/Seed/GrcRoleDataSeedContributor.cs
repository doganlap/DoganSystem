using Microsoft.Extensions.Logging;
using Volo.Abp.Data;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Identity;
using Volo.Abp.PermissionManagement;
using DoganSystem.Permissions;

namespace DoganSystem.Application.Seed;

public class GrcRoleDataSeedContributor : IDataSeedContributor, ITransientDependency
{
    private readonly IdentityRoleManager _roleManager;
    private readonly IPermissionManager _permissionManager;
    private readonly ILogger<GrcRoleDataSeedContributor> _logger;

    public GrcRoleDataSeedContributor(
        IdentityRoleManager roleManager,
        IPermissionManager permissionManager,
        ILogger<GrcRoleDataSeedContributor> logger)
    {
        _roleManager = roleManager;
        _permissionManager = permissionManager;
        _logger = logger;
    }

    public async Task SeedAsync(DataSeedContext context)
    {
        _logger.LogInformation("Seeding GRC roles and permissions...");

        // SuperAdmin - All permissions
        await CreateRoleWithPermissions("SuperAdmin", new[]
        {
            GrcPermissions.Home.Default,
            GrcPermissions.Dashboard.Default,
            GrcPermissions.Subscriptions.View,
            GrcPermissions.Subscriptions.Manage,
            GrcPermissions.Admin.Access,
            GrcPermissions.Admin.Users,
            GrcPermissions.Admin.Roles,
            GrcPermissions.Admin.Tenants,
            GrcPermissions.Frameworks.View,
            GrcPermissions.Frameworks.Create,
            GrcPermissions.Frameworks.Update,
            GrcPermissions.Frameworks.Delete,
            GrcPermissions.Frameworks.Import,
            GrcPermissions.Regulators.View,
            GrcPermissions.Regulators.Manage,
            GrcPermissions.Assessments.View,
            GrcPermissions.Assessments.Create,
            GrcPermissions.Assessments.Update,
            GrcPermissions.Assessments.Submit,
            GrcPermissions.Assessments.Approve,
            GrcPermissions.ControlAssessments.View,
            GrcPermissions.ControlAssessments.Manage,
            GrcPermissions.Evidence.View,
            GrcPermissions.Evidence.Upload,
            GrcPermissions.Evidence.Update,
            GrcPermissions.Evidence.Delete,
            GrcPermissions.Evidence.Approve,
            GrcPermissions.Risks.View,
            GrcPermissions.Risks.Manage,
            GrcPermissions.Risks.Accept,
            GrcPermissions.Audits.View,
            GrcPermissions.Audits.Manage,
            GrcPermissions.Audits.Close,
            GrcPermissions.ActionPlans.View,
            GrcPermissions.ActionPlans.Manage,
            GrcPermissions.ActionPlans.Assign,
            GrcPermissions.ActionPlans.Close,
            GrcPermissions.Policies.View,
            GrcPermissions.Policies.Manage,
            GrcPermissions.Policies.Approve,
            GrcPermissions.Policies.Publish,
            GrcPermissions.ComplianceCalendar.View,
            GrcPermissions.ComplianceCalendar.Manage,
            GrcPermissions.Workflow.View,
            GrcPermissions.Workflow.Manage,
            GrcPermissions.Notifications.View,
            GrcPermissions.Notifications.Manage,
            GrcPermissions.Vendors.View,
            GrcPermissions.Vendors.Manage,
            GrcPermissions.Vendors.Assess,
            GrcPermissions.Reports.View,
            GrcPermissions.Reports.Export,
            GrcPermissions.Integrations.View,
            GrcPermissions.Integrations.Manage
        });

        // TenantAdmin
        await CreateRoleWithPermissions("TenantAdmin", new[]
        {
            GrcPermissions.Home.Default,
            GrcPermissions.Dashboard.Default,
            GrcPermissions.Subscriptions.View,
            GrcPermissions.Subscriptions.Manage,
            GrcPermissions.Admin.Access,
            GrcPermissions.Admin.Users,
            GrcPermissions.Admin.Roles,
            GrcPermissions.Integrations.View,
            GrcPermissions.Integrations.Manage
        });

        // ComplianceManager
        await CreateRoleWithPermissions("ComplianceManager", new[]
        {
            GrcPermissions.Home.Default,
            GrcPermissions.Dashboard.Default,
            GrcPermissions.Frameworks.View,
            GrcPermissions.Frameworks.Create,
            GrcPermissions.Frameworks.Update,
            GrcPermissions.Frameworks.Delete,
            GrcPermissions.Frameworks.Import,
            GrcPermissions.Regulators.View,
            GrcPermissions.Regulators.Manage,
            GrcPermissions.Assessments.View,
            GrcPermissions.Assessments.Create,
            GrcPermissions.Assessments.Update,
            GrcPermissions.Assessments.Submit,
            GrcPermissions.Assessments.Approve,
            GrcPermissions.ControlAssessments.View,
            GrcPermissions.ControlAssessments.Manage,
            GrcPermissions.Evidence.View,
            GrcPermissions.Evidence.Upload,
            GrcPermissions.Evidence.Update,
            GrcPermissions.Evidence.Delete,
            GrcPermissions.Evidence.Approve,
            GrcPermissions.Policies.View,
            GrcPermissions.Policies.Manage,
            GrcPermissions.Policies.Approve,
            GrcPermissions.Policies.Publish,
            GrcPermissions.ComplianceCalendar.View,
            GrcPermissions.ComplianceCalendar.Manage,
            GrcPermissions.Workflow.View,
            GrcPermissions.Workflow.Manage,
            GrcPermissions.Reports.View,
            GrcPermissions.Reports.Export
        });

        // RiskManager
        await CreateRoleWithPermissions("RiskManager", new[]
        {
            GrcPermissions.Home.Default,
            GrcPermissions.Dashboard.Default,
            GrcPermissions.Risks.View,
            GrcPermissions.Risks.Manage,
            GrcPermissions.Risks.Accept,
            GrcPermissions.ActionPlans.View,
            GrcPermissions.ActionPlans.Manage,
            GrcPermissions.ActionPlans.Assign,
            GrcPermissions.ActionPlans.Close,
            GrcPermissions.Reports.View,
            GrcPermissions.Reports.Export
        });

        // Auditor
        await CreateRoleWithPermissions("Auditor", new[]
        {
            GrcPermissions.Home.Default,
            GrcPermissions.Dashboard.Default,
            GrcPermissions.Audits.View,
            GrcPermissions.Audits.Manage,
            GrcPermissions.Audits.Close,
            GrcPermissions.Evidence.View,
            GrcPermissions.Assessments.View,
            GrcPermissions.Reports.View
        });

        // EvidenceOfficer
        await CreateRoleWithPermissions("EvidenceOfficer", new[]
        {
            GrcPermissions.Home.Default,
            GrcPermissions.Dashboard.Default,
            GrcPermissions.Evidence.View,
            GrcPermissions.Evidence.Upload,
            GrcPermissions.Evidence.Update,
            GrcPermissions.Assessments.View,
            GrcPermissions.Assessments.Create,
            GrcPermissions.Assessments.Update,
            GrcPermissions.Assessments.Submit
        });

        // VendorManager
        await CreateRoleWithPermissions("VendorManager", new[]
        {
            GrcPermissions.Home.Default,
            GrcPermissions.Dashboard.Default,
            GrcPermissions.Vendors.View,
            GrcPermissions.Vendors.Manage,
            GrcPermissions.Vendors.Assess
        });

        // Viewer
        await CreateRoleWithPermissions("Viewer", new[]
        {
            GrcPermissions.Home.Default,
            GrcPermissions.Dashboard.Default,
            GrcPermissions.Frameworks.View,
            GrcPermissions.Regulators.View,
            GrcPermissions.Assessments.View,
            GrcPermissions.ControlAssessments.View,
            GrcPermissions.Evidence.View,
            GrcPermissions.Risks.View,
            GrcPermissions.Audits.View,
            GrcPermissions.ActionPlans.View,
            GrcPermissions.Policies.View,
            GrcPermissions.ComplianceCalendar.View,
            GrcPermissions.Workflow.View,
            GrcPermissions.Notifications.View,
            GrcPermissions.Vendors.View,
            GrcPermissions.Reports.View,
            GrcPermissions.Integrations.View
        });

        _logger.LogInformation("GRC roles and permissions seeded successfully.");
    }

    private async Task CreateRoleWithPermissions(string roleName, string[] permissions)
    {
        var role = await _roleManager.FindByNameAsync(roleName);
        if (role == null)
        {
            role = new IdentityRole(Guid.NewGuid(), roleName, null);
            await _roleManager.CreateAsync(role);
            _logger.LogInformation("Created role: {RoleName}", roleName);
        }

        foreach (var permission in permissions)
        {
            // Set permission for role - provider name "R" = Role, provider key = roleName
            // SetAsync signature: (permissionName, providerName, providerKey, isGranted)
            await _permissionManager.SetAsync(permission, "R", roleName, true);
        }

        _logger.LogInformation("Granted {Count} permissions to role: {RoleName}", permissions.Length, roleName);
    }
}
