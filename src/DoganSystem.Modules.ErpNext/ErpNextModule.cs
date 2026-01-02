using Volo.Abp.Modularity;
using Volo.Abp.EntityFrameworkCore;
using DoganSystem.Core;

namespace DoganSystem.Modules.ErpNext
{
    [DependsOn(
        typeof(AbpEntityFrameworkCoreModule),
        typeof(DoganSystemCoreModule)
    )]
    public class ErpNextModule : AbpModule
    {
        public override void ConfigureServices(ServiceConfigurationContext context)
        {
        }
    }
}
