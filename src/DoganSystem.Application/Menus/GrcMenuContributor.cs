using Volo.Abp.UI.Navigation;
using DoganSystem.Permissions;

namespace DoganSystem.Application.Menus;

    public class GrcMenuContributor : IMenuContributor
    {
        public Task ConfigureMenuAsync(MenuConfigurationContext context)
        {
            // #region agent log
            try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "G", location = "GrcMenuContributor.cs:8", message = "ConfigureMenuAsync called", data = new { menuName = context.Menu.Name }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
            // #endregion
            if (context.Menu.Name != StandardMenus.Main)
            {
                // #region agent log
                try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "G", location = "GrcMenuContributor.cs:11", message = "Menu name mismatch, skipping", data = new { menuName = context.Menu.Name, expected = StandardMenus.Main }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
                // #endregion
                return Task.CompletedTask;
            }
            // #region agent log
            try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "G", location = "GrcMenuContributor.cs:15", message = "Configuring main menu", data = new { menuItemCount = context.Menu.Items.Count }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
            // #endregion

        var menu = context.Menu;

        // الصفحة الرئيسية
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Home",
            "الصفحة الرئيسية",
            "/",
            icon: "fas fa-home"
        )
        {
            RequiredPermissionName = GrcPermissions.Home.Default
        });

        // لوحة التحكم
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Dashboard",
            "لوحة التحكم",
            "/dashboard",
            icon: "fas fa-chart-line"
        )
        {
            RequiredPermissionName = GrcPermissions.Dashboard.Default
        });

        // الاشتراكات
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Subscriptions",
            "الاشتراكات",
            "/subscriptions",
            icon: "fas fa-id-card"
        )
        {
            RequiredPermissionName = GrcPermissions.Subscriptions.View
        });

        // الإدارة (with submenu)
        var adminMenuItem = new ApplicationMenuItem(
            "Grc.Admin",
            "الإدارة",
            "/admin",
            icon: "fas fa-cog"
        )
        {
            RequiredPermissionName = GrcPermissions.Admin.Access
        };

        adminMenuItem.AddItem(new ApplicationMenuItem(
            "Grc.Admin.Users",
            "المستخدمون",
            "/admin/users",
            icon: "fas fa-users"
        )
        {
            RequiredPermissionName = GrcPermissions.Admin.Users
        });

        adminMenuItem.AddItem(new ApplicationMenuItem(
            "Grc.Admin.Roles",
            "الأدوار",
            "/admin/roles",
            icon: "fas fa-user-shield"
        )
        {
            RequiredPermissionName = GrcPermissions.Admin.Roles
        });

        adminMenuItem.AddItem(new ApplicationMenuItem(
            "Grc.Admin.Tenants",
            "العملاء",
            "/admin/tenants",
            icon: "fas fa-building"
        )
        {
            RequiredPermissionName = GrcPermissions.Admin.Tenants
        });

        menu.AddItem(adminMenuItem);

        // مكتبة الأطر التنظيمية
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Frameworks",
            "مكتبة الأطر التنظيمية",
            "/frameworks",
            icon: "fas fa-layer-group"
        )
        {
            RequiredPermissionName = GrcPermissions.Frameworks.View
        });

        // الجهات التنظيمية
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Regulators",
            "الجهات التنظيمية",
            "/regulators",
            icon: "fas fa-landmark"
        )
        {
            RequiredPermissionName = GrcPermissions.Regulators.View
        });

        // التقييمات
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Assessments",
            "التقييمات",
            "/assessments",
            icon: "fas fa-clipboard-check"
        )
        {
            RequiredPermissionName = GrcPermissions.Assessments.View
        });

        // تقييمات الضوابط
        menu.AddItem(new ApplicationMenuItem(
            "Grc.ControlAssessments",
            "تقييمات الضوابط",
            "/control-assessments",
            icon: "fas fa-tasks"
        )
        {
            RequiredPermissionName = GrcPermissions.ControlAssessments.View
        });

        // الأدلة
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Evidence",
            "الأدلة",
            "/evidence",
            icon: "fas fa-file-alt"
        )
        {
            RequiredPermissionName = GrcPermissions.Evidence.View
        });

        // إدارة المخاطر
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Risks",
            "إدارة المخاطر",
            "/risks",
            icon: "fas fa-exclamation-triangle"
        )
        {
            RequiredPermissionName = GrcPermissions.Risks.View
        });

        // إدارة المراجعة
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Audits",
            "إدارة المراجعة",
            "/audits",
            icon: "fas fa-search"
        )
        {
            RequiredPermissionName = GrcPermissions.Audits.View
        });

        // خطط العمل
        menu.AddItem(new ApplicationMenuItem(
            "Grc.ActionPlans",
            "خطط العمل",
            "/action-plans",
            icon: "fas fa-project-diagram"
        )
        {
            RequiredPermissionName = GrcPermissions.ActionPlans.View
        });

        // إدارة السياسات
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Policies",
            "إدارة السياسات",
            "/policies",
            icon: "fas fa-gavel"
        )
        {
            RequiredPermissionName = GrcPermissions.Policies.View
        });

        // تقويم الامتثال
        menu.AddItem(new ApplicationMenuItem(
            "Grc.ComplianceCalendar",
            "تقويم الامتثال",
            "/compliance-calendar",
            icon: "fas fa-calendar-alt"
        )
        {
            RequiredPermissionName = GrcPermissions.ComplianceCalendar.View
        });

        // محرك سير العمل
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Workflow",
            "محرك سير العمل",
            "/workflow",
            icon: "fas fa-sitemap"
        )
        {
            RequiredPermissionName = GrcPermissions.Workflow.View
        });

        // الإشعارات
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Notifications",
            "الإشعارات",
            "/notifications",
            icon: "fas fa-bell"
        )
        {
            RequiredPermissionName = GrcPermissions.Notifications.View
        });

        // إدارة الموردين
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Vendors",
            "إدارة الموردين",
            "/vendors",
            icon: "fas fa-handshake"
        )
        {
            RequiredPermissionName = GrcPermissions.Vendors.View
        });

        // التقارير والتحليلات
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Reports",
            "التقارير والتحليلات",
            "/reports",
            icon: "fas fa-chart-pie"
        )
        {
            RequiredPermissionName = GrcPermissions.Reports.View
        });

        // مركز التكامل
        menu.AddItem(new ApplicationMenuItem(
            "Grc.Integrations",
            "مركز التكامل",
            "/integrations",
            icon: "fas fa-plug"
        )
        {
            RequiredPermissionName = GrcPermissions.Integrations.View
        });

        // #region agent log
        try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "G", location = "GrcMenuContributor.cs:258", message = "Menu configuration complete", data = new { totalItems = menu.Items.Count }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
        // #endregion

        return Task.CompletedTask;
    }
}
