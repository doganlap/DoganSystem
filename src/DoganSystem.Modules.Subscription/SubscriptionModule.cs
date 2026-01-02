using Volo.Abp.Modularity;
using Volo.Abp.EntityFrameworkCore;
using DoganSystem.Core;
using DoganSystem.Modules.TenantManagement;

namespace DoganSystem.Modules.Subscription
{
    [DependsOn(
        typeof(AbpEntityFrameworkCoreModule),
        typeof(DoganSystemCoreModule),
        typeof(TenantManagementModule)
    )]
    public class SubscriptionModule : AbpModule
    {
        public override void ConfigureServices(ServiceConfigurationContext context)
        {
        }
    }
}
