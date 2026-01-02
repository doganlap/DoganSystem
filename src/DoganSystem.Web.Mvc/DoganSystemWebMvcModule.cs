using DoganSystem.EntityFrameworkCore;
using DoganSystem.Application;
using DoganSystem.Modules.TenantManagement;
using DoganSystem.Modules.ErpNext;
using DoganSystem.Modules.AgentOrchestrator;
using DoganSystem.Modules.Subscription;
using DoganSystem.Application.Seed;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Volo.Abp;
using Volo.Abp.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc.UI.Theme.Basic;
using Volo.Abp.Autofac;
using Volo.Abp.Modularity;
using Volo.Abp.EntityFrameworkCore;
using Volo.Abp.EntityFrameworkCore.SqlServer;
using Volo.Abp.Identity;
using Volo.Abp.Data;

namespace DoganSystem.Web
{
    [DependsOn(
        typeof(AbpAspNetCoreMvcModule),
        typeof(AbpAspNetCoreMvcUiBasicThemeModule),
        typeof(AbpAutofacModule),
        typeof(AbpEntityFrameworkCoreSqlServerModule),
        typeof(AbpIdentityDomainModule),
        typeof(DoganSystemEntityFrameworkCoreModule),
        typeof(DoganSystemApplicationModule),
        typeof(TenantManagementModule),
        typeof(ErpNextModule),
        typeof(AgentOrchestratorModule),
        typeof(SubscriptionModule)
    )]
    public class DoganSystemWebMvcModule : AbpModule
    {
        public override void ConfigureServices(ServiceConfigurationContext context)
        {
            var hostingEnvironment = context.Services.GetHostingEnvironment();
            var configuration = context.Services.GetConfiguration();

            Configure<AbpDbContextOptions>(options =>
            {
                options.UseSqlServer();
            });

            context.Services.AddAbpDbContext<DoganSystemDbContext>(options =>
            {
                options.AddDefaultRepositories(includeAllEntities: true);
            });

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

        public override async Task OnApplicationInitializationAsync(ApplicationInitializationContext context)
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

            app.UseHttpsRedirection();
            app.UseAbpRequestLocalization();
            app.UseStaticFiles();
            app.UseRouting();
            
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
            
            app.UseConfiguredEndpoints();

            // Seed GRC roles and permissions
            await SeedGrcDataAsync(context);
        }

        private async Task SeedGrcDataAsync(ApplicationInitializationContext context)
        {
            using var scope = context.ServiceProvider.CreateScope();
            var dataSeeder = scope.ServiceProvider.GetRequiredService<GrcRoleDataSeedContributor>();
            await dataSeeder.SeedAsync(new DataSeedContext());
        }
    }
}
