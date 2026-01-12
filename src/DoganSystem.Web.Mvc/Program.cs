using DoganSystem.Web;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Volo.Abp;
using Volo.Abp.AspNetCore.Mvc;
using Volo.Abp.Modularity;
using Volo.Abp.Data;
using DoganSystem.Web.Mvc;

namespace DoganSystem.Web.Mvc
{
    public class Program
    {
        public static async Task<int> Main(string[] args)
        {
            try
            {
                var builder = WebApplication.CreateBuilder(args);
                await builder.AddApplicationAsync<DoganSystemWebMvcModule>();
                var app = builder.Build();

                // Initialize application
                await app.InitializeApplicationAsync();
                Console.WriteLine("Application initialized successfully.");

                // Seed database with initial data using direct EF Core access
                try
                {
                    await DbSeeder.SeedAsync(app.Services, builder.Configuration);
                }
                catch (Exception seedEx)
                {
                    Console.WriteLine($"Warning: Database seeding had issues: {seedEx.Message}");
                    // Continue anyway - seeding can be retried manually
                }

                await app.RunAsync();
                return 0;
            }
            catch (Exception ex)
            {
                if (ex is HostAbortedException)
                {
                    throw;
                }

                Console.WriteLine($"Application startup failed: {ex.Message}");
                Console.WriteLine($"Stack trace: {ex.StackTrace}");
                if (ex.InnerException != null)
                {
                    Console.WriteLine($"Inner exception: {ex.InnerException.Message}");
                }
                return 1;
            }
        }
    }
}
