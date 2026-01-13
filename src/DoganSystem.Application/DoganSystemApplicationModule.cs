using Volo.Abp.Modularity;
using Volo.Abp.AutoMapper;
using Volo.Abp.Authorization;
using Volo.Abp.Identity;
using Volo.Abp.TenantManagement;
using Volo.Abp.PermissionManagement;
using Volo.Abp.FeatureManagement;
using Volo.Abp.Emailing;
using DoganSystem.Core;
using DoganSystem.Application.ObjectMapper;
using DoganSystem.Application.Policy;
using DoganSystem.Core.Policy;
using DoganSystem.Application.Permissions;
using Microsoft.Extensions.DependencyInjection;

namespace DoganSystem.Application
{
    [DependsOn(
        typeof(AbpAutoMapperModule),
        typeof(AbpAuthorizationModule),
        typeof(AbpIdentityApplicationModule),
        typeof(AbpIdentityApplicationContractsModule),
        typeof(AbpTenantManagementApplicationModule),
        typeof(AbpTenantManagementApplicationContractsModule),
        typeof(AbpPermissionManagementApplicationModule),
        typeof(AbpPermissionManagementApplicationContractsModule),
        typeof(AbpFeatureManagementApplicationModule),
        typeof(AbpFeatureManagementApplicationContractsModule),
        typeof(AbpEmailingModule),
        typeof(DoganSystemCoreModule)
    )]
    public class DoganSystemApplicationModule : AbpModule
    {
        public override void PreConfigureServices(ServiceConfigurationContext context)
        {
            // Permission definition provider is automatically discovered by ABP
            // No need to manually register - ABP discovers PermissionDefinitionProvider classes automatically
            // They are discovered via dependency injection
        }

        public override void ConfigureServices(ServiceConfigurationContext context)
        {
            context.Services.AddAutoMapperObjectMapper<DoganSystemApplicationModule>();
            Configure<AbpAutoMapperOptions>(options =>
            {
                options.AddMaps<DoganSystemApplicationAutoMapperProfile>();
            });

            // Register Policy services
            context.Services.AddSingleton<PolicyStore>();
            context.Services.AddScoped<Core.Policy.IPolicyEnforcer, PolicyEnforcer>();
            context.Services.AddScoped<PolicyAuditLogger>();
        }
    }
}
