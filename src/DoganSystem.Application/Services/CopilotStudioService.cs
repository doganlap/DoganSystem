using DoganSystem.Application.Configuration;
using Microsoft.Extensions.Options;
using Microsoft.Extensions.Logging;

namespace DoganSystem.Application.Services
{
    /// <summary>
    /// Service implementation for Microsoft Copilot Studio integration
    /// </summary>
    public class CopilotStudioService : ICopilotStudioService
    {
        private readonly MicrosoftCopilotStudioOptions _options;
        private readonly ILogger<CopilotStudioService> _logger;

        public CopilotStudioService(
            IOptions<MicrosoftCopilotStudioOptions> options,
            ILogger<CopilotStudioService> logger)
        {
            _options = options.Value;
            _logger = logger;
        }

        public Task<MicrosoftCopilotStudioOptions> GetConfigurationAsync()
        {
            return Task.FromResult(_options);
        }

        public Task<bool> ValidateConnectionAsync()
        {
            // Basic validation - check if required configuration is present
            var isValid = !string.IsNullOrEmpty(_options.ApplicationId) &&
                         !string.IsNullOrEmpty(_options.TenantId) &&
                         !string.IsNullOrEmpty(_options.ApplicationIdUri);

            if (!isValid)
            {
                _logger.LogWarning("Copilot Studio configuration is incomplete. Required: ApplicationId, TenantId, ApplicationIdUri");
            }

            return Task.FromResult(isValid);
        }

        public string GetAuthenticationUrl(string redirectUri)
        {
            var tenantId = _options.TenantId;
            var clientId = _options.ApplicationId;
            var scope = "openid profile email";
            
            return $"https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/authorize?" +
                   $"client_id={clientId}&" +
                   $"response_type=code&" +
                   $"redirect_uri={Uri.EscapeDataString(redirectUri)}&" +
                   $"response_mode=query&" +
                   $"scope={Uri.EscapeDataString(scope)}";
        }
    }
}
