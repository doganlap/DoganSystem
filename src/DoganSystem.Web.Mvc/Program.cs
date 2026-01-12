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
        public async static Task<int> Main(string[] args)
        {
            // #region agent log
            try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "A", location = "Program.cs:13", message = "Main entry", data = new { args = args?.Length ?? 0 }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
            // #endregion
            try
            {
                var builder = WebApplication.CreateBuilder(args);
                // #region agent log
                try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "A", location = "Program.cs:18", message = "Builder created", data = new { }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
                // #endregion
                await builder.AddApplicationAsync<DoganSystemWebMvcModule>();
                // #region agent log
                try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "A", location = "Program.cs:20", message = "Application module added", data = new { }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
                // #endregion
                var app = builder.Build();
                // #region agent log
                try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "A", location = "Program.cs:22", message = "App built", data = new { }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
                // #endregion
                
                // Initialize application
                await app.InitializeApplicationAsync();
                Console.WriteLine("Application initialized successfully.");

                // Seed database with initial data using direct EF Core access
                try
                {
                    await DbSeeder.SeedAsync(app.Services);
                }
                catch (Exception seedEx)
                {
                    Console.WriteLine($"Warning: Database seeding had issues: {seedEx.Message}");
                    // Continue anyway - seeding can be retried manually
                }

                await app.RunAsync();
                // #region agent log
                try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "C", location = "Program.cs:54", message = "After app.RunAsync (should not reach here)", data = new { }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
                // #endregion
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
