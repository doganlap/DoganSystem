using Volo.Abp.UI.Navigation;
using DoganSystem.Permissions;

namespace DoganSystem.Application.Menus;

public class GrcMenuContributor : IMenuContributor
{
    public Task ConfigureMenuAsync(MenuConfigurationContext context)
    {
        if (context.Menu.Name != StandardMenus.Main)
        {
            return Task.CompletedTask;
        }

        var menu = context.Menu;

        // الصفحة الرئيسية
        var homeItem = new ApplicationMenuItem(
            "Grc.Home",
            "الصفحة الرئيسية",
            "/",
            icon: "fas fa-home"
        );
        homeItem.RequiredPermissionName = GrcPermissions.Home.Default;
        menu.AddItem(homeItem);

        // لوحة التحكم
        var dashboardItem = new ApplicationMenuItem(
            "Grc.Dashboard",
            "لوحة التحكم",
            "/dashboard",
            icon: "fas fa-chart-line"
        );
        dashboardItem.RequiredPermissionName = GrcPermissions.Dashboard.Default;
        menu.AddItem(dashboardItem);

        // الاشتراكات
        var subscriptionsItem = new ApplicationMenuItem(
            "Grc.Subscriptions",
            "الاشتراكات",
            "/subscriptions",
            icon: "fas fa-id-card"
        );
        subscriptionsItem.RequiredPermissionName = GrcPermissions.Subscriptions.View;
        menu.AddItem(subscriptionsItem);

        // الإدارة (with submenu)
        var adminMenuItem = new ApplicationMenuItem(
            "Grc.Admin",
            "الإدارة",
            "/admin",
            icon: "fas fa-cog"
        );

        var usersItem = new ApplicationMenuItem(
            "Grc.Admin.Users",
            "المستخدمون",
            "/admin/users",
            icon: "fas fa-users"
        );
        usersItem.RequiredPermissionName = GrcPermissions.Admin.Users;
        adminMenuItem.AddItem(usersItem);

        var rolesItem = new ApplicationMenuItem(
            "Grc.Admin.Roles",
            "الأدوار",
            "/admin/roles",
            icon: "fas fa-user-shield"
        );
        rolesItem.RequiredPermissionName = GrcPermissions.Admin.Roles;
        adminMenuItem.AddItem(rolesItem);

        var tenantsItem = new ApplicationMenuItem(
            "Grc.Admin.Tenants",
            "العملاء",
            "/admin/tenants",
            icon: "fas fa-building"
        );
        tenantsItem.RequiredPermissionName = GrcPermissions.Admin.Tenants;
        adminMenuItem.AddItem(tenantsItem);

        menu.AddItem(adminMenuItem);

        // مكتبة الأطر التنظيمية
        var frameworksItem = new ApplicationMenuItem(
            "Grc.Frameworks",
            "مكتبة الأطر التنظيمية",
            "/frameworks",
            icon: "fas fa-layer-group"
        );
        frameworksItem.RequiredPermissionName = GrcPermissions.Frameworks.View;
        menu.AddItem(frameworksItem);

        // الجهات التنظيمية
        var regulatorsItem = new ApplicationMenuItem(
            "Grc.Regulators",
            "الجهات التنظيمية",
            "/regulators",
            icon: "fas fa-landmark"
        );
        regulatorsItem.RequiredPermissionName = GrcPermissions.Regulators.View;
        menu.AddItem(regulatorsItem);

        // التقييمات
        var assessmentsItem = new ApplicationMenuItem(
            "Grc.Assessments",
            "التقييمات",
            "/assessments",
            icon: "fas fa-clipboard-check"
        );
        assessmentsItem.RequiredPermissionName = GrcPermissions.Assessments.View;
        menu.AddItem(assessmentsItem);

        // تقييمات الضوابط
        var controlAssessmentsItem = new ApplicationMenuItem(
            "Grc.ControlAssessments",
            "تقييمات الضوابط",
            "/control-assessments",
            icon: "fas fa-tasks"
        );
        controlAssessmentsItem.RequiredPermissionName = GrcPermissions.ControlAssessments.View;
        menu.AddItem(controlAssessmentsItem);

        // الأدلة
        var evidenceItem = new ApplicationMenuItem(
            "Grc.Evidence",
            "الأدلة",
            "/evidence",
            icon: "fas fa-file-alt"
        );
        evidenceItem.RequiredPermissionName = GrcPermissions.Evidence.View;
        menu.AddItem(evidenceItem);

        // إدارة المخاطر
        var risksItem = new ApplicationMenuItem(
            "Grc.Risks",
            "إدارة المخاطر",
            "/risks",
            icon: "fas fa-exclamation-triangle"
        );
        risksItem.RequiredPermissionName = GrcPermissions.Risks.View;
        menu.AddItem(risksItem);

        // إدارة المراجعة
        var auditsItem = new ApplicationMenuItem(
            "Grc.Audits",
            "إدارة المراجعة",
            "/audits",
            icon: "fas fa-search"
        );
        auditsItem.RequiredPermissionName = GrcPermissions.Audits.View;
        menu.AddItem(auditsItem);

        // خطط العمل
        var actionPlansItem = new ApplicationMenuItem(
            "Grc.ActionPlans",
            "خطط العمل",
            "/action-plans",
            icon: "fas fa-project-diagram"
        );
        actionPlansItem.RequiredPermissionName = GrcPermissions.ActionPlans.View;
        menu.AddItem(actionPlansItem);

        // إدارة السياسات
        var policiesItem = new ApplicationMenuItem(
            "Grc.Policies",
            "إدارة السياسات",
            "/policies",
            icon: "fas fa-gavel"
        );
        policiesItem.RequiredPermissionName = GrcPermissions.Policies.View;
        menu.AddItem(policiesItem);

        // تقويم الامتثال
        var complianceCalendarItem = new ApplicationMenuItem(
            "Grc.ComplianceCalendar",
            "تقويم الامتثال",
            "/compliance-calendar",
            icon: "fas fa-calendar-alt"
        );
        complianceCalendarItem.RequiredPermissionName = GrcPermissions.ComplianceCalendar.View;
        menu.AddItem(complianceCalendarItem);

        // محرك سير العمل
        var workflowItem = new ApplicationMenuItem(
            "Grc.Workflow",
            "محرك سير العمل",
            "/workflow",
            icon: "fas fa-sitemap"
        );
        workflowItem.RequiredPermissionName = GrcPermissions.Workflow.View;
        menu.AddItem(workflowItem);

        // الإشعارات
        var notificationsItem = new ApplicationMenuItem(
            "Grc.Notifications",
            "الإشعارات",
            "/notifications",
            icon: "fas fa-bell"
        );
        notificationsItem.RequiredPermissionName = GrcPermissions.Notifications.View;
        menu.AddItem(notificationsItem);

        // إدارة الموردين
        var vendorsItem = new ApplicationMenuItem(
            "Grc.Vendors",
            "إدارة الموردين",
            "/vendors",
            icon: "fas fa-handshake"
        );
        vendorsItem.RequiredPermissionName = GrcPermissions.Vendors.View;
        menu.AddItem(vendorsItem);

        // التقارير والتحليلات
        var reportsItem = new ApplicationMenuItem(
            "Grc.Reports",
            "التقارير والتحليلات",
            "/reports",
            icon: "fas fa-chart-pie"
        );
        reportsItem.RequiredPermissionName = GrcPermissions.Reports.View;
        menu.AddItem(reportsItem);

        // مركز التكامل
        var integrationsItem = new ApplicationMenuItem(
            "Grc.Integrations",
            "مركز التكامل",
            "/integrations",
            icon: "fas fa-plug"
        );
        integrationsItem.RequiredPermissionName = GrcPermissions.Integrations.View;
        menu.AddItem(integrationsItem);

        return Task.CompletedTask;
    }
}
