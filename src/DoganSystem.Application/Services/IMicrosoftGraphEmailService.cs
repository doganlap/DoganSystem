namespace DoganSystem.Application.Services
{
    /// <summary>
    /// Service interface for Microsoft Graph API email operations
    /// </summary>
    public interface IMicrosoftGraphEmailService
    {
        /// <summary>
        /// Send an email using Microsoft Graph API
        /// </summary>
        Task<bool> SendEmailAsync(string to, string subject, string body, bool isHtml = false, string? cc = null, string? bcc = null);

        /// <summary>
        /// Read emails from mailbox using Microsoft Graph API
        /// </summary>
        Task<List<EmailMessage>> ReadEmailsAsync(int limit = 10, bool unreadOnly = false);

        /// <summary>
        /// Mark an email as read
        /// </summary>
        Task<bool> MarkAsReadAsync(string messageId);

        /// <summary>
        /// Get email by ID
        /// </summary>
        Task<EmailMessage?> GetEmailAsync(string messageId);

        /// <summary>
        /// Validate connection to Microsoft Graph API
        /// </summary>
        Task<bool> ValidateConnectionAsync();
    }

    /// <summary>
    /// Email message model
    /// </summary>
    public class EmailMessage
    {
        public string Id { get; set; } = string.Empty;
        public string From { get; set; } = string.Empty;
        public string To { get; set; } = string.Empty;
        public string Subject { get; set; } = string.Empty;
        public string Body { get; set; } = string.Empty;
        public bool IsHtml { get; set; }
        public DateTime ReceivedDateTime { get; set; }
        public bool IsRead { get; set; }
        public List<string> Cc { get; set; } = new();
        public List<string> Bcc { get; set; } = new();
    }
}
