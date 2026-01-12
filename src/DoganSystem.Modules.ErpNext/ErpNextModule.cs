using Microsoft.Extensions.DependencyInjection;
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
            // Register HttpClient for ERPNext API calls using .NET built-in IHttpClientFactory
            context.Services.AddHttpClient("ErpNext", client =>
            {
                client.Timeout = System.TimeSpan.FromSeconds(30);
                client.DefaultRequestHeaders.Add("Accept", "application/json");
            });
        }
    }
}
