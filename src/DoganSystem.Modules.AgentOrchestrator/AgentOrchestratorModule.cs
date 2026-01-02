using Volo.Abp.Modularity;
using Volo.Abp.EntityFrameworkCore;
using DoganSystem.Core;
using DoganSystem.Modules.TenantManagement;
using Microsoft.Extensions.DependencyInjection;

namespace DoganSystem.Modules.AgentOrchestrator
{
    [DependsOn(
        typeof(AbpEntityFrameworkCoreModule),
        typeof(DoganSystemCoreModule),
        typeof(TenantManagementModule)
    )]
    public class AgentOrchestratorModule : AbpModule
    {
        public override void ConfigureServices(ServiceConfigurationContext context)
        {
            context.Services.AddTransient<Application.AgentOrchestratorService>();
        }
    }
}
