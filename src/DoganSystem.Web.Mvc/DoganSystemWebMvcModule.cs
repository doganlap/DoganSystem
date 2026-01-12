using DoganSystem.EntityFrameworkCore;
using DoganSystem.Application;
using DoganSystem.Modules.TenantManagement;
using DoganSystem.Modules.ErpNext;
using DoganSystem.Modules.AgentOrchestrator;
using DoganSystem.Modules.Subscription;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Localization;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System.Globalization;
using Volo.Abp;
using Volo.Abp.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc.UI.Theme.Basic;
using Volo.Abp.Autofac;
using Volo.Abp.Modularity;
using Volo.Abp.EntityFrameworkCore;
using Volo.Abp.EntityFrameworkCore.PostgreSql;
using Volo.Abp.Identity;
using Volo.Abp.TenantManagement;
using Volo.Abp.PermissionManagement;
using Volo.Abp.FeatureManagement;
using Volo.Abp.MultiTenancy;
// Account modules temporarily disabled
// using Volo.Abp.Account;
// using Volo.Abp.Account.Web;
using Volo.Abp.Identity.AspNetCore;
// OpenIddict temporarily disabled
// using OpenIddict.Validation.AspNetCore;
// using OpenIddict.Server;
using Microsoft.AspNetCore.Identity;

namespace DoganSystem.Web
{
    [DependsOn(
        typeof(AbpAspNetCoreMvcModule),
        typeof(AbpAspNetCoreMvcUiBasicThemeModule),
        typeof(AbpAutofacModule),
        typeof(AbpEntityFrameworkCorePostgreSqlModule),
        typeof(AbpIdentityDomainModule),
        typeof(AbpIdentityApplicationModule),
        typeof(AbpIdentityApplicationContractsModule),
        typeof(AbpTenantManagementDomainModule),
        typeof(AbpTenantManagementApplicationModule),
        typeof(AbpTenantManagementApplicationContractsModule),
        typeof(AbpPermissionManagementDomainModule),
        typeof(AbpPermissionManagementApplicationModule),
        typeof(AbpPermissionManagementApplicationContractsModule),
        typeof(AbpFeatureManagementDomainModule),
        typeof(AbpFeatureManagementApplicationModule),
        typeof(AbpFeatureManagementApplicationContractsModule),
        // Account and OpenIddict modules temporarily disabled - will configure later
        // typeof(AbpAccountApplicationModule),
        typeof(AbpIdentityAspNetCoreModule),
        // typeof(AbpAccountWebOpenIddictModule),
        typeof(DoganSystemEntityFrameworkCoreModule),
        typeof(DoganSystemApplicationModule),
        typeof(TenantManagementModule),
        typeof(ErpNextModule),
        typeof(AgentOrchestratorModule),
        typeof(SubscriptionModule)
    )]
    public class DoganSystemWebMvcModule : AbpModule
    {
        public override void PreConfigureServices(ServiceConfigurationContext context)
        {
            // Configure multi-tenancy to allow host-level operations
            Configure<Volo.Abp.MultiTenancy.AbpMultiTenancyOptions>(options =>
            {
                options.IsEnabled = true;
            });

            // OpenIddict configuration temporarily disabled
            // Will be re-enabled after proper setup
        }

        public override void ConfigureServices(ServiceConfigurationContext context)
        {
            var hostingEnvironment = context.Services.GetHostingEnvironment();
            var configuration = context.Services.GetConfiguration();

            Configure<AbpDbContextOptions>(options =>
            {
                options.UseNpgsql();
            });

            context.Services.AddAbpDbContext<DoganSystemDbContext>(options =>
            {
                options.AddDefaultRepositories(includeAllEntities: true);
            });

            // All entities use the unified DoganSystemDbContext
            // Module-specific DbContexts have been removed as they were unused

            // Configure multi-tenancy to allow host-level operations during initialization
            Configure<Volo.Abp.MultiTenancy.AbpMultiTenancyOptions>(options =>
            {
                options.IsEnabled = true;
            });

            // Configure PermissionManagement to save definitions asynchronously (avoid startup null reference)
            Configure<Volo.Abp.PermissionManagement.PermissionManagementOptions>(options =>
            {
                options.SaveStaticPermissionsToDatabase = false; // Disable for now, will be enabled after first request
            });

            // Configure FeatureManagement to save definitions asynchronously
            Configure<Volo.Abp.FeatureManagement.FeatureManagementOptions>(options =>
            {
                options.SaveStaticFeaturesToDatabase = false; // Disable for now
            });

            // Configure ForwardedHeaders for reverse proxy (Nginx)
            context.Services.Configure<Microsoft.AspNetCore.Builder.ForwardedHeadersOptions>(options =>
            {
                options.ForwardedHeaders = Microsoft.AspNetCore.HttpOverrides.ForwardedHeaders.XForwardedFor |
                                          Microsoft.AspNetCore.HttpOverrides.ForwardedHeaders.XForwardedProto;
                options.KnownNetworks.Clear();
                options.KnownProxies.Clear();
            });

            // Configure Identity options for admin user seeding
            Configure<IdentityOptions>(options =>
            {
                options.Password.RequireDigit = true;
                options.Password.RequireLowercase = true;
                options.Password.RequireUppercase = true;
                options.Password.RequireNonAlphanumeric = false;
                options.Password.RequiredLength = 6;
            });

            // Note: Identity is already configured by AbpIdentityAspNetCoreModule
            // Do not call AddIdentity again as it causes duplicate scheme registration

            // Add MVC with views support
            context.Services.AddControllersWithViews();
            context.Services.AddRazorPages();

            // Add Swagger
            context.Services.AddSwaggerGen(options =>
            {
                options.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo
                {
                    Title = "DoganSystem API",
                    Version = "v1",
                    Description = "Multi-Tenant SaaS Platform API"
                });
            });
        }

        public override Task OnApplicationInitializationAsync(ApplicationInitializationContext context)
        {
            var app = context.GetApplicationBuilder();
            var env = context.GetEnvironment();

            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseExceptionHandler("/Error");
                app.UseHsts();
            }

            // Use forwarded headers from reverse proxy (Nginx handles HTTPS)
            app.UseForwardedHeaders();

            // Use configuration-based request localization
            var configuration = context.ServiceProvider.GetRequiredService<Microsoft.Extensions.Configuration.IConfiguration>();
            var defaultLanguage = configuration["Abp:Localization:DefaultLanguage"] ?? "ar";
            var supportedLanguages = configuration.GetSection("Abp:Localization:SupportedLanguages").Get<string[]>()
                ?? new[] { "ar", "en" };

            var supportedCultures = supportedLanguages.Select(lang => new CultureInfo(lang)).ToArray();
            var localizationOptions = new RequestLocalizationOptions
            {
                DefaultRequestCulture = new RequestCulture(defaultLanguage),
                SupportedCultures = supportedCultures,
                SupportedUICultures = supportedCultures,
                RequestCultureProviders = new List<IRequestCultureProvider>
                {
                    new QueryStringRequestCultureProvider(),
                    new CookieRequestCultureProvider(),
                    new AcceptLanguageHeaderRequestCultureProvider()
                }
            };
            app.UseRequestLocalization(localizationOptions);
            app.UseStaticFiles();
            app.UseRouting();
            app.UseAuthentication();
            app.UseAuthorization();
            app.UseMultiTenancy();

            // Swagger (only in development)
            if (env.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI(options =>
                {
                    options.SwaggerEndpoint("/swagger/v1/swagger.json", "DoganSystem API");
                    options.RoutePrefix = "swagger";
                });
            }

            app.UseConfiguredEndpoints(endpoints =>
            {
                endpoints.MapControllerRoute(
                    name: "default",
                    pattern: "{controller=Home}/{action=Index}/{id?}");
                endpoints.MapRazorPages();
            });

            return Task.CompletedTask;
        }
    }
}
