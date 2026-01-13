namespace DoganSystem.Application.Configuration
{
    /// <summary>
    /// Configuration options for Microsoft Copilot Studio integration
    /// </summary>
    public class MicrosoftCopilotStudioOptions
    {
        /// <summary>
        /// Application (Client) ID from Azure AD app registration
        /// </summary>
        public string ApplicationId { get; set; } = string.Empty;

        /// <summary>
        /// Object ID from Azure AD app registration
        /// </summary>
        public string ObjectId { get; set; } = string.Empty;

        /// <summary>
        /// Directory (Tenant) ID from Azure AD app registration
        /// </summary>
        public string TenantId { get; set; } = string.Empty;

        /// <summary>
        /// Application ID URI (e.g., api://{client-id})
        /// </summary>
        public string ApplicationIdUri { get; set; } = string.Empty;

        /// <summary>
        /// Supported account types (e.g., "My organization only")
        /// </summary>
        public string SupportedAccountTypes { get; set; } = string.Empty;

        /// <summary>
        /// List of redirect URIs configured in Azure AD
        /// </summary>
        public List<string> RedirectUris { get; set; } = new();

        /// <summary>
        /// Client secrets (stored securely, not in configuration)
        /// </summary>
        public List<string> ClientSecrets { get; set; } = new();
    }
}
