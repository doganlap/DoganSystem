namespace DoganSystem.Application.Configuration
{
    /// <summary>
    /// Azure AD configuration options for Email Server (Shahin-ai Server)
    /// </summary>
    public class EmailServerAzureAdOptions
    {
        /// <summary>
        /// Azure AD instance URL
        /// </summary>
        public string Instance { get; set; } = "https://login.microsoftonline.com/";

        /// <summary>
        /// Directory (Tenant) ID from Azure AD app registration
        /// </summary>
        public string TenantId { get; set; } = string.Empty;

        /// <summary>
        /// Application (Client) ID from Azure AD app registration
        /// </summary>
        public string ClientId { get; set; } = string.Empty;

        /// <summary>
        /// Object ID from Azure AD app registration
        /// </summary>
        public string ObjectId { get; set; } = string.Empty;

        /// <summary>
        /// Client secret (stored securely, not in configuration)
        /// </summary>
        public string ClientSecret { get; set; } = string.Empty;

        /// <summary>
        /// Application ID URI (e.g., api://{client-id})
        /// </summary>
        public string ApplicationIdUri { get; set; } = string.Empty;

        /// <summary>
        /// Microsoft Graph API scopes
        /// </summary>
        public string Scopes { get; set; } = "https://graph.microsoft.com/.default";

        /// <summary>
        /// Microsoft Graph API endpoint
        /// </summary>
        public string GraphApiEndpoint { get; set; } = "https://graph.microsoft.com/v1.0";
    }

    /// <summary>
    /// Email Server configuration options
    /// </summary>
    public class EmailServerOptions
    {
        /// <summary>
        /// Azure AD configuration for Email Server
        /// </summary>
        public EmailServerAzureAdOptions AzureAd { get; set; } = new();

        /// <summary>
        /// Display name of the email server application
        /// </summary>
        public string DisplayName { get; set; } = string.Empty;

        /// <summary>
        /// Supported account types
        /// </summary>
        public string SupportedAccountTypes { get; set; } = string.Empty;

        /// <summary>
        /// User email address to use for sending/receiving emails via Microsoft Graph API
        /// This should be the email of the service account or user mailbox
        /// </summary>
        public string? UserEmail { get; set; }
    }
}
