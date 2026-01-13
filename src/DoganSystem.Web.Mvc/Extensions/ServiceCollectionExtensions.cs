using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Microsoft.OpenApi.Models;
using System.Text.Json;
using DoganSystem.Web.Mvc.Middleware;
using HealthChecks.UI.Client;

namespace DoganSystem.Web.Mvc.Extensions
{
    /// <summary>
    /// Extension methods for service collection configuration
    /// Following ASP.NET and ABP best practices
    /// </summary>
    public static class ServiceCollectionExtensions
    {
        /// <summary>
        /// Add health checks for database, external services, etc.
        /// </summary>
        public static IServiceCollection AddCustomHealthChecks(this IServiceCollection services, IConfiguration configuration)
        {
            var healthChecks = services.AddHealthChecks();

            // Database health check
            var connectionString = configuration.GetConnectionString("Default");
            if (!string.IsNullOrEmpty(connectionString))
            {
                healthChecks.AddSqlServer(
                    connectionString,
                    name: "database",
                    failureStatus: HealthStatus.Unhealthy,
                    tags: new[] { "db", "sql", "sqlserver" });
            }

            // Python Services health check (simplified)
            var pythonServicesUrl = configuration["PythonServices:OrchestratorUrl"];
            if (!string.IsNullOrEmpty(pythonServicesUrl))
            {
                healthChecks.AddCheck("python-services", () => HealthCheckResult.Healthy("Python Services configured"), tags: new[] { "external", "python" });
            }

            // ERPNext health check (simplified)
            var erpNextUrl = configuration["ErpNext:DefaultUrl"];
            if (!string.IsNullOrEmpty(erpNextUrl))
            {
                healthChecks.AddCheck("erpnext", () => HealthCheckResult.Healthy("ERPNext configured"), tags: new[] { "external", "erpnext" });
            }

            return services;
        }

        /// <summary>
        /// Configure CORS following best practices
        /// </summary>
        public static IServiceCollection AddCustomCors(this IServiceCollection services, IConfiguration configuration)
        {
            var allowedOrigins = configuration.GetSection("Cors:AllowedOrigins").Get<string[]>() 
                ?? new[] { "http://localhost:3000", "http://localhost:5000" };

            services.AddCors(options =>
            {
                options.AddDefaultPolicy(builder =>
                {
                    builder
                        .WithOrigins(allowedOrigins)
                        .AllowAnyMethod()
                        .AllowAnyHeader()
                        .AllowCredentials()
                        .SetPreflightMaxAge(TimeSpan.FromMinutes(10));
                });

                // Production policy
                options.AddPolicy("Production", builder =>
                {
                    var productionOrigins = configuration.GetSection("Cors:ProductionOrigins").Get<string[]>() 
                        ?? Array.Empty<string>();

                    builder
                        .WithOrigins(productionOrigins)
                        .AllowAnyMethod()
                        .AllowAnyHeader()
                        .AllowCredentials()
                        .SetPreflightMaxAge(TimeSpan.FromMinutes(10));
                });
            });

            return services;
        }

        /// <summary>
        /// Configure Swagger with security and best practices
        /// </summary>
        public static IServiceCollection AddCustomSwagger(this IServiceCollection services, IConfiguration configuration)
        {
            services.AddSwaggerGen(options =>
            {
                options.SwaggerDoc("v1", new OpenApiInfo
                {
                    Title = "DoganSystem API",
                    Version = "v1",
                    Description = "Multi-Tenant SaaS Platform API",
                    Contact = new OpenApiContact
                    {
                        Name = "Dogan Consult",
                        Email = "info@doganconsult.com"
                    },
                    License = new OpenApiLicense
                    {
                        Name = "Proprietary",
                        Url = new Uri("https://doganconsult.com")
                    }
                });

                // Add security definition for Bearer token
                options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
                {
                    Description = "JWT Authorization header using the Bearer scheme. Enter 'Bearer' [space] and then your token.",
                    Name = "Authorization",
                    In = ParameterLocation.Header,
                    Type = SecuritySchemeType.ApiKey,
                    Scheme = "Bearer"
                });

                options.AddSecurityRequirement(new OpenApiSecurityRequirement
                {
                    {
                        new OpenApiSecurityScheme
                        {
                            Reference = new OpenApiReference
                            {
                                Type = ReferenceType.SecurityScheme,
                                Id = "Bearer"
                            }
                        },
                        Array.Empty<string>()
                    }
                });

                // Include XML comments if available
                var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
                var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
                if (File.Exists(xmlPath))
                {
                    options.IncludeXmlComments(xmlPath);
                }
            });

            return services;
        }

        /// <summary>
        /// Configure rate limiting
        /// Note: Rate limiting is built into .NET 8, but API may vary
        /// </summary>
        public static IServiceCollection AddCustomRateLimiting(this IServiceCollection services)
        {
            // Rate limiting configuration - can be enabled later when needed
            // services.AddRateLimiter(options => { ... });
            return services;
        }
    }
}
