using Volo.Abp.Modularity;
using DoganSystem.Core;

namespace DoganSystem.Application
{
    [DependsOn(
        typeof(DoganSystemCoreModule)
    )]
    public class DoganSystemApplicationModule : AbpModule
    {
        public override void ConfigureServices(ServiceConfigurationContext context)
        {
        }
    }
}
