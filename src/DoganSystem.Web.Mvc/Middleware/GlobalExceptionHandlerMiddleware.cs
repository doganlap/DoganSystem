using System.Net;
using System.Text.Json;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Volo.Abp;

namespace DoganSystem.Web.Mvc.Middleware
{
    /// <summary>
    /// Global exception handling middleware following ABP and ASP.NET best practices
    /// </summary>
    public class GlobalExceptionHandlerMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<GlobalExceptionHandlerMiddleware> _logger;

        public GlobalExceptionHandlerMiddleware(
            RequestDelegate next,
            ILogger<GlobalExceptionHandlerMiddleware> logger)
        {
            _next = next;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            try
            {
                await _next(context);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "An unhandled exception occurred. Request Path: {Path}", context.Request.Path);
                await HandleExceptionAsync(context, ex);
            }
        }

        private static Task HandleExceptionAsync(HttpContext context, Exception exception)
        {
            var code = HttpStatusCode.InternalServerError;
            var result = string.Empty;

            switch (exception)
            {
                case BusinessException businessException:
                    code = HttpStatusCode.BadRequest;
                    result = JsonSerializer.Serialize(new
                    {
                        error = new
                        {
                            code = businessException.Code ?? "BUSINESS_ERROR",
                            message = businessException.Message,
                            details = businessException.Details
                        }
                    });
                    break;

                case UnauthorizedAccessException:
                    code = HttpStatusCode.Unauthorized;
                    result = JsonSerializer.Serialize(new
                    {
                        error = new
                        {
                            code = "UNAUTHORIZED",
                            message = "You are not authorized to perform this action."
                        }
                    });
                    break;

                case ArgumentException argumentException:
                    code = HttpStatusCode.BadRequest;
                    result = JsonSerializer.Serialize(new
                    {
                        error = new
                        {
                            code = "INVALID_ARGUMENT",
                            message = argumentException.Message
                        }
                    });
                    break;

                default:
                    // Don't expose internal errors in production
                    var isDevelopment = context.RequestServices
                        .GetService<IWebHostEnvironment>()?.IsDevelopment() ?? false;

                    result = JsonSerializer.Serialize(new
                    {
                        error = new
                        {
                            code = "INTERNAL_SERVER_ERROR",
                            message = isDevelopment ? exception.Message : "An error occurred while processing your request.",
                            details = isDevelopment ? exception.StackTrace : null
                        }
                    });
                    break;
            }

            context.Response.ContentType = "application/json";
            context.Response.StatusCode = (int)code;
            return context.Response.WriteAsync(result);
        }
    }
}
