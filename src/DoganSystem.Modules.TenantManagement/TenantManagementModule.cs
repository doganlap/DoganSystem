using Volo.Abp.Modularity;
using Volo.Abp.EntityFrameworkCore;
using DoganSystem.Core;

namespace DoganSystem.Modules.TenantManagement
{
    [DependsOn(
        typeof(AbpEntityFrameworkCoreModule),
        typeof(DoganSystemCoreModule)
    )]
    public class TenantManagementModule : AbpModule
    {
        public override void ConfigureServices(ServiceConfigurationContext context)
        {
        }
    }
}
