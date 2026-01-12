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
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Home",
                "الصفحة الرئيسية",
                "/",
                icon: "fas fa-home"
            ).RequirePermissions(GrcPermissions.Home.Default)
        );

        // لوحة التحكم
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Dashboard",
                "لوحة التحكم",
                "/dashboard",
                icon: "fas fa-chart-line"
            ).RequirePermissions(GrcPermissions.Dashboard.Default)
        );

        // الاشتراكات
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Subscriptions",
                "الاشتراكات",
                "/subscriptions",
                icon: "fas fa-id-card"
            ).RequirePermissions(GrcPermissions.Subscriptions.View)
        );

        // الإدارة (with submenu)
        var adminMenuItem = new ApplicationMenuItem(
            "Grc.Admin",
            "الإدارة",
            "/admin",
            icon: "fas fa-cog"
        ).RequirePermissions(GrcPermissions.Admin.Access);

        adminMenuItem.AddItem(
            new ApplicationMenuItem(
                "Grc.Admin.Users",
                "المستخدمون",
                "/admin/users",
                icon: "fas fa-users"
            ).RequirePermissions(GrcPermissions.Admin.Users)
        );

        adminMenuItem.AddItem(
            new ApplicationMenuItem(
                "Grc.Admin.Roles",
                "الأدوار",
                "/admin/roles",
                icon: "fas fa-user-shield"
            ).RequirePermissions(GrcPermissions.Admin.Roles)
        );

        adminMenuItem.AddItem(
            new ApplicationMenuItem(
                "Grc.Admin.Tenants",
                "العملاء",
                "/admin/tenants",
                icon: "fas fa-building"
            ).RequirePermissions(GrcPermissions.Admin.Tenants)
        );

        menu.AddItem(adminMenuItem);

        // مكتبة الأطر التنظيمية
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Frameworks",
                "مكتبة الأطر التنظيمية",
                "/frameworks",
                icon: "fas fa-layer-group"
            ).RequirePermissions(GrcPermissions.Frameworks.View)
        );

        // الجهات التنظيمية
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Regulators",
                "الجهات التنظيمية",
                "/regulators",
                icon: "fas fa-landmark"
            ).RequirePermissions(GrcPermissions.Regulators.View)
        );

        // التقييمات
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Assessments",
                "التقييمات",
                "/assessments",
                icon: "fas fa-clipboard-check"
            ).RequirePermissions(GrcPermissions.Assessments.View)
        );

        // تقييمات الضوابط
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.ControlAssessments",
                "تقييمات الضوابط",
                "/control-assessments",
                icon: "fas fa-tasks"
            ).RequirePermissions(GrcPermissions.ControlAssessments.View)
        );

        // الأدلة
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Evidence",
                "الأدلة",
                "/evidence",
                icon: "fas fa-file-alt"
            ).RequirePermissions(GrcPermissions.Evidence.View)
        );

        // إدارة المخاطر
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Risks",
                "إدارة المخاطر",
                "/risks",
                icon: "fas fa-exclamation-triangle"
            ).RequirePermissions(GrcPermissions.Risks.View)
        );

        // إدارة المراجعة
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Audits",
                "إدارة المراجعة",
                "/audits",
                icon: "fas fa-search"
            ).RequirePermissions(GrcPermissions.Audits.View)
        );

        // خطط العمل
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.ActionPlans",
                "خطط العمل",
                "/action-plans",
                icon: "fas fa-project-diagram"
            ).RequirePermissions(GrcPermissions.ActionPlans.View)
        );

        // إدارة السياسات
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Policies",
                "إدارة السياسات",
                "/policies",
                icon: "fas fa-gavel"
            ).RequirePermissions(GrcPermissions.Policies.View)
        );

        // تقويم الامتثال
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.ComplianceCalendar",
                "تقويم الامتثال",
                "/compliance-calendar",
                icon: "fas fa-calendar-alt"
            ).RequirePermissions(GrcPermissions.ComplianceCalendar.View)
        );

        // محرك سير العمل
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Workflow",
                "محرك سير العمل",
                "/workflow",
                icon: "fas fa-sitemap"
            ).RequirePermissions(GrcPermissions.Workflow.View)
        );

        // الإشعارات
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Notifications",
                "الإشعارات",
                "/notifications",
                icon: "fas fa-bell"
            ).RequirePermissions(GrcPermissions.Notifications.View)
        );

        // إدارة الموردين
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Vendors",
                "إدارة الموردين",
                "/vendors",
                icon: "fas fa-handshake"
            ).RequirePermissions(GrcPermissions.Vendors.View)
        );

        // التقارير والتحليلات
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Reports",
                "التقارير والتحليلات",
                "/reports",
                icon: "fas fa-chart-pie"
            ).RequirePermissions(GrcPermissions.Reports.View)
        );

        // مركز التكامل
        menu.AddItem(
            new ApplicationMenuItem(
                "Grc.Integrations",
                "مركز التكامل",
                "/integrations",
                icon: "fas fa-plug"
            ).RequirePermissions(GrcPermissions.Integrations.View)
        );

        return Task.CompletedTask;
    }
}
