using DoganSystem.Application.Configuration;

namespace DoganSystem.Application.Services
{
    /// <summary>
    /// Service interface for Microsoft Copilot Studio integration
    /// </summary>
    public interface ICopilotStudioService
    {
        /// <summary>
        /// Gets the application configuration for Copilot Studio
        /// </summary>
        Task<MicrosoftCopilotStudioOptions> GetConfigurationAsync();

        /// <summary>
        /// Validates the Copilot Studio connection
        /// </summary>
        Task<bool> ValidateConnectionAsync();

        /// <summary>
        /// Gets the authentication URL for Copilot Studio
        /// </summary>
        string GetAuthenticationUrl(string redirectUri);
    }
}
