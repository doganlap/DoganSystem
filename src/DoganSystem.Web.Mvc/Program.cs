using DoganSystem.Web;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Volo.Abp;
using Volo.Abp.AspNetCore.Mvc;
using Volo.Abp.Modularity;

namespace DoganSystem.Web.Mvc
{
    public class Program
    {
        public async static Task<int> Main(string[] args)
        {
            try
            {
                var builder = WebApplication.CreateBuilder(args);
                await builder.AddApplicationAsync<DoganSystemWebMvcModule>();
                var app = builder.Build();
                await app.InitializeApplicationAsync();
                await app.RunAsync();
                return 0;
            }
            catch (Exception ex)
            {
                if (ex is HostAbortedException)
                {
                    throw;
                }
                return 1;
            }
        }
    }
}
