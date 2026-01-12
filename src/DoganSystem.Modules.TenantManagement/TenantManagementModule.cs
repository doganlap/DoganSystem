using Volo.Abp.Modularity;
using Volo.Abp.EntityFrameworkCore;
using Volo.Abp.TenantManagement;
using DoganSystem.Core;

namespace DoganSystem.Modules.TenantManagement
{
    [DependsOn(
        typeof(AbpEntityFrameworkCoreModule),
        typeof(AbpTenantManagementDomainModule),
        typeof(AbpTenantManagementApplicationModule),
        typeof(AbpTenantManagementApplicationContractsModule),
        typeof(DoganSystemCoreModule)
    )]
    public class TenantManagementModule : AbpModule
    {
        public override void ConfigureServices(ServiceConfigurationContext context)
        {
        }
    }
}
