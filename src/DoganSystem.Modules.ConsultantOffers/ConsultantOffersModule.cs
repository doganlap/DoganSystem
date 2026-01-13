using Volo.Abp.Modularity;
using Volo.Abp.Application;
using DoganSystem.Core;

namespace DoganSystem.Modules.ConsultantOffers
{
    [DependsOn(
        typeof(AbpDddApplicationModule),
        typeof(DoganSystemCoreModule)
    )]
    public class ConsultantOffersModule : AbpModule
    {
        public override void ConfigureServices(ServiceConfigurationContext context)
        {
            // Module configuration
        }
    }
}
