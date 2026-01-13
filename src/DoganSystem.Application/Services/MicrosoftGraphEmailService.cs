using DoganSystem.Application.Configuration;
using Microsoft.Extensions.Options;
using Microsoft.Extensions.Logging;
using System.Text;
using System.Text.Json;

namespace DoganSystem.Application.Services
{
    /// <summary>
    /// Service implementation for Microsoft Graph API email operations
    /// </summary>
    public class MicrosoftGraphEmailService : IMicrosoftGraphEmailService
    {
        private readonly EmailServerOptions _options;
        private readonly ILogger<MicrosoftGraphEmailService> _logger;
        private readonly HttpClient _httpClient;
        private string? _accessToken;

        public MicrosoftGraphEmailService(
            IOptions<EmailServerOptions> options,
            ILogger<MicrosoftGraphEmailService> logger,
            IHttpClientFactory httpClientFactory)
        {
            _options = options.Value;
            _logger = logger;
            _httpClient = httpClientFactory.CreateClient();
            _httpClient.BaseAddress = new Uri(_options.AzureAd.GraphApiEndpoint);
        }

        /// <summary>
        /// Get access token using client credentials flow
        /// </summary>
        private async Task<string?> GetAccessTokenAsync()
        {
            if (!string.IsNullOrEmpty(_accessToken))
            {
                return _accessToken;
            }

            try
            {
                var tokenEndpoint = $"{_options.AzureAd.Instance}{_options.AzureAd.TenantId}/oauth2/v2.0/token";
                
                var requestBody = new Dictionary<string, string>
                {
                    { "client_id", _options.AzureAd.ClientId },
                    { "client_secret", _options.AzureAd.ClientSecret },
                    { "scope", _options.AzureAd.Scopes },
                    { "grant_type", "client_credentials" }
                };

                var request = new HttpRequestMessage(HttpMethod.Post, tokenEndpoint)
                {
                    Content = new FormUrlEncodedContent(requestBody)
                };

                var response = await _httpClient.SendAsync(request);
                response.EnsureSuccessStatusCode();

                var responseContent = await response.Content.ReadAsStringAsync();
                var tokenResponse = JsonSerializer.Deserialize<JsonElement>(responseContent);

                if (tokenResponse.TryGetProperty("access_token", out var token))
                {
                    _accessToken = token.GetString();
                    return _accessToken;
                }

                _logger.LogError("Failed to get access token: No access_token in response");
                return null;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting access token");
                return null;
            }
        }

        /// <summary>
        /// Set authorization header with access token
        /// </summary>
        private async Task<bool> SetAuthorizationHeaderAsync()
        {
            var token = await GetAccessTokenAsync();
            if (string.IsNullOrEmpty(token))
            {
                return false;
            }

            _httpClient.DefaultRequestHeaders.Authorization = 
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);
            
            return true;
        }

        public async Task<bool> SendEmailAsync(string to, string subject, string body, bool isHtml = false, string? cc = null, string? bcc = null)
        {
            try
            {
                if (!await SetAuthorizationHeaderAsync())
                {
                    _logger.LogError("Failed to set authorization header");
                    return false;
                }

                // Get user's email address (you may need to configure this)
                var userEmail = await GetUserEmailAsync();
                if (string.IsNullOrEmpty(userEmail))
                {
                    _logger.LogError("User email not configured");
                    return false;
                }

                var message = new
                {
                    message = new
                    {
                        subject = subject,
                        body = new
                        {
                            contentType = isHtml ? "html" : "text",
                            content = body
                        },
                        toRecipients = new[]
                        {
                            new { emailAddress = new { address = to } }
                        },
                        ccRecipients = !string.IsNullOrEmpty(cc) ? new[]
                        {
                            new { emailAddress = new { address = cc } }
                        } : null,
                        bccRecipients = !string.IsNullOrEmpty(bcc) ? new[]
                        {
                            new { emailAddress = new { address = bcc } }
                        } : null
                    }
                };

                var json = JsonSerializer.Serialize(message);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync($"/users/{userEmail}/sendMail", content);
                response.EnsureSuccessStatusCode();

                _logger.LogInformation($"Email sent successfully to {to}");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error sending email to {to}");
                return false;
            }
        }

        public async Task<List<EmailMessage>> ReadEmailsAsync(int limit = 10, bool unreadOnly = false)
        {
            var emails = new List<EmailMessage>();

            try
            {
                if (!await SetAuthorizationHeaderAsync())
                {
                    _logger.LogError("Failed to set authorization header");
                    return emails;
                }

                var userEmail = await GetUserEmailAsync();
                if (string.IsNullOrEmpty(userEmail))
                {
                    _logger.LogError("User email not configured");
                    return emails;
                }

                var filter = unreadOnly ? "?$filter=isRead eq false" : "";
                var top = $"{filter}{(string.IsNullOrEmpty(filter) ? "?" : "&")}$top={limit}&$orderby=receivedDateTime desc";

                var response = await _httpClient.GetAsync($"/users/{userEmail}/messages{top}");
                response.EnsureSuccessStatusCode();

                var responseContent = await response.Content.ReadAsStringAsync();
                var jsonDoc = JsonDocument.Parse(responseContent);

                if (jsonDoc.RootElement.TryGetProperty("value", out var messages))
                {
                    foreach (var message in messages.EnumerateArray())
                    {
                        var email = new EmailMessage
                        {
                            Id = message.TryGetProperty("id", out var id) ? id.GetString() ?? "" : "",
                            Subject = message.TryGetProperty("subject", out var subject) ? subject.GetString() ?? "" : "",
                            Body = message.TryGetProperty("body", out var body) && body.TryGetProperty("content", out var content) 
                                ? content.GetString() ?? "" : "",
                            IsHtml = message.TryGetProperty("body", out var bodyProp) && bodyProp.TryGetProperty("contentType", out var contentType) 
                                && contentType.GetString() == "html",
                            IsRead = message.TryGetProperty("isRead", out var isRead) && isRead.GetBoolean(),
                            ReceivedDateTime = message.TryGetProperty("receivedDateTime", out var received) 
                                && DateTime.TryParse(received.GetString(), out var date) ? date : DateTime.MinValue
                        };

                        if (message.TryGetProperty("from", out var from) && from.TryGetProperty("emailAddress", out var fromEmail))
                        {
                            email.From = fromEmail.TryGetProperty("address", out var address) ? address.GetString() ?? "" : "";
                        }

                        if (message.TryGetProperty("toRecipients", out var toRecipients))
                        {
                            foreach (var recipient in toRecipients.EnumerateArray())
                            {
                                if (recipient.TryGetProperty("emailAddress", out var emailAddr) 
                                    && emailAddr.TryGetProperty("address", out var addr))
                                {
                                    email.To = addr.GetString() ?? "";
                                    break;
                                }
                            }
                        }

                        emails.Add(email);
                    }
                }

                _logger.LogInformation($"Read {emails.Count} emails");
                return emails;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error reading emails");
                return emails;
            }
        }

        public async Task<bool> MarkAsReadAsync(string messageId)
        {
            try
            {
                if (!await SetAuthorizationHeaderAsync())
                {
                    return false;
                }

                var userEmail = await GetUserEmailAsync();
                if (string.IsNullOrEmpty(userEmail))
                {
                    return false;
                }

                var patch = new { isRead = true };
                var json = JsonSerializer.Serialize(patch);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PatchAsync($"/users/{userEmail}/messages/{messageId}", content);
                response.EnsureSuccessStatusCode();

                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error marking email {messageId} as read");
                return false;
            }
        }

        public async Task<EmailMessage?> GetEmailAsync(string messageId)
        {
            try
            {
                if (!await SetAuthorizationHeaderAsync())
                {
                    return null;
                }

                var userEmail = await GetUserEmailAsync();
                if (string.IsNullOrEmpty(userEmail))
                {
                    return null;
                }

                var response = await _httpClient.GetAsync($"/users/{userEmail}/messages/{messageId}");
                response.EnsureSuccessStatusCode();

                var responseContent = await response.Content.ReadAsStringAsync();
                var message = JsonDocument.Parse(responseContent).RootElement;

                var email = new EmailMessage
                {
                    Id = message.TryGetProperty("id", out var id) ? id.GetString() ?? "" : "",
                    Subject = message.TryGetProperty("subject", out var subject) ? subject.GetString() ?? "" : "",
                    Body = message.TryGetProperty("body", out var body) && body.TryGetProperty("content", out var content) 
                        ? content.GetString() ?? "" : "",
                    IsHtml = message.TryGetProperty("body", out var bodyProp) && bodyProp.TryGetProperty("contentType", out var contentType) 
                        && contentType.GetString() == "html",
                    IsRead = message.TryGetProperty("isRead", out var isRead) && isRead.GetBoolean(),
                    ReceivedDateTime = message.TryGetProperty("receivedDateTime", out var received) 
                        && DateTime.TryParse(received.GetString(), out var date) ? date : DateTime.MinValue
                };

                if (message.TryGetProperty("from", out var from) && from.TryGetProperty("emailAddress", out var fromEmail))
                {
                    email.From = fromEmail.TryGetProperty("address", out var address) ? address.GetString() ?? "" : "";
                }

                if (message.TryGetProperty("toRecipients", out var toRecipients))
                {
                    foreach (var recipient in toRecipients.EnumerateArray())
                    {
                        if (recipient.TryGetProperty("emailAddress", out var emailAddr) 
                            && emailAddr.TryGetProperty("address", out var addr))
                        {
                            email.To = addr.GetString() ?? "";
                            break;
                        }
                    }
                }

                if (message.TryGetProperty("ccRecipients", out var ccRecipients))
                {
                    foreach (var recipient in ccRecipients.EnumerateArray())
                    {
                        if (recipient.TryGetProperty("emailAddress", out var emailAddr) 
                            && emailAddr.TryGetProperty("address", out var addr))
                        {
                            email.Cc.Add(addr.GetString() ?? "");
                        }
                    }
                }

                return email;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error getting email {messageId}");
                return null;
            }
        }

        public async Task<bool> ValidateConnectionAsync()
        {
            try
            {
                var token = await GetAccessTokenAsync();
                return !string.IsNullOrEmpty(token);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error validating connection");
                return false;
            }
        }

        /// <summary>
        /// Get user email address (configure this based on your setup)
        /// This should be configured in appsettings.json or retrieved from current user context
        /// </summary>
        private Task<string?> GetUserEmailAsync()
        {
            // Get from configuration (for service account)
            return Task.FromResult(_options.UserEmail);
        }
    }
}
