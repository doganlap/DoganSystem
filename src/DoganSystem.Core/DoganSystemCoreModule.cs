using Volo.Abp.Modularity;
using Volo.Abp.Authorization;

namespace DoganSystem.Core
{
    [DependsOn(typeof(AbpAuthorizationModule))]
    public class DoganSystemCoreModule : AbpModule
    {
        public override void ConfigureServices(ServiceConfigurationContext context)
        {
        }
    }
}
