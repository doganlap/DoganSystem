# Email Server Azure AD Integration Guide

## Overview

This guide explains how to configure the Email Server (Shahin-ai Server) integration with DoganSystem using Azure AD and Microsoft Graph API for email operations.

## Azure AD App Registration Details

The following Azure AD application has been configured for Email Server:

- **Display Name**: Shahin-ai Server
- **Application (Client) ID**: `4e2575c6-e269-48eb-b055-ad730a2150a7`
- **Object ID**: `263703d6-de9c-494a-a14f-828e72565f2d`
- **Directory (Tenant) ID**: `c8847e8a-33a0-4b6c-8e01-2e0e6b4aaef5`
- **Application ID URI**: `api://4e2575c6-e269-48eb-b055-ad730a2150a7`
- **Supported Account Types**: My organization only
- **Client Credentials**: 5 secrets configured

## Configuration Steps

### 1. Add Client Secret

You need to add a client secret from Azure AD to your configuration:

1. Go to Azure Portal → Azure Active Directory → App registrations
2. Select your app: **Shahin-ai Server**
3. Navigate to **Certificates & secrets**
4. Create a new client secret (or use an existing one)
5. Copy the secret value (you can only see it once)
6. Add it to your `appsettings.json` or `appsettings.Production.json`:

```json
{
  "EmailServer": {
    "AzureAd": {
      "ClientSecret": "your-client-secret-here"
    }
  }
}
```

**Important**: Never commit client secrets to source control. Use:
- User Secrets for development: `dotnet user-secrets set "EmailServer:AzureAd:ClientSecret" "your-secret"`
- Azure Key Vault for production
- Environment variables

### 2. Configure API Permissions

1. Go to Azure Portal → App registrations → **Shahin-ai Server** → API permissions
2. Add the following **Microsoft Graph** permissions:
   - **Mail.Send** (Application permission) - Send emails
   - **Mail.Read** (Application permission) - Read emails
   - **Mail.ReadWrite** (Application permission) - Read and write emails
   - **User.Read.All** (Application permission) - Read user information (if needed)

3. Click **Grant admin consent** for your organization

### 3. Configure User Email

Add the email address of the mailbox to use for sending/receiving emails:

```json
{
  "EmailServer": {
    "UserEmail": "service-account@yourdomain.com"
  }
}
```

This should be:
- A service account mailbox, OR
- A shared mailbox, OR
- A user mailbox with appropriate permissions

### 4. Update appsettings.json

The configuration has been added to `appsettings.json`:

```json
{
  "EmailServer": {
    "AzureAd": {
      "Instance": "https://login.microsoftonline.com/",
      "TenantId": "c8847e8a-33a0-4b6c-8e01-2e0e6b4aaef5",
      "ClientId": "4e2575c6-e269-48eb-b055-ad730a2150a7",
      "ObjectId": "263703d6-de9c-494a-a14f-828e72565f2d",
      "ClientSecret": "",  // Add your secret here
      "ApplicationIdUri": "api://4e2575c6-e269-48eb-b055-ad730a2150a7",
      "Scopes": "https://graph.microsoft.com/.default",
      "GraphApiEndpoint": "https://graph.microsoft.com/v1.0"
    },
    "DisplayName": "Shahin-ai Server",
    "SupportedAccountTypes": "My organization only",
    "UserEmail": "service-account@yourdomain.com"
  }
}
```

## Using User Secrets (Development)

For local development, use .NET User Secrets:

```powershell
dotnet user-secrets init --project src/DoganSystem.Web.Mvc
dotnet user-secrets set "EmailServer:AzureAd:ClientSecret" "your-client-secret-here" --project src/DoganSystem.Web.Mvc
dotnet user-secrets set "EmailServer:UserEmail" "service-account@yourdomain.com" --project src/DoganSystem.Web.Mvc
```

## Authentication Flow

The Email Server uses **Client Credentials Flow** (application-only authentication):

1. Application requests access token using Client ID and Client Secret
2. Azure AD validates credentials and returns access token
3. Application uses token to call Microsoft Graph API
4. Microsoft Graph API validates token and processes request

## Using the Email Service

### In Application Services

```csharp
using DoganSystem.Application.Services;

public class MyEmailService
{
    private readonly IMicrosoftGraphEmailService _emailService;
    
    public MyEmailService(IMicrosoftGraphEmailService emailService)
    {
        _emailService = emailService;
    }
    
    public async Task SendEmailAsync()
    {
        var success = await _emailService.SendEmailAsync(
            to: "customer@example.com",
            subject: "Invoice",
            body: "Your invoice is attached.",
            isHtml: true
        );
    }
    
    public async Task ReadEmailsAsync()
    {
        var emails = await _emailService.ReadEmailsAsync(limit: 10, unreadOnly: true);
        foreach (var email in emails)
        {
            // Process email
        }
    }
}
```

## API Permissions Required

| Permission | Type | Description |
|------------|------|-------------|
| Mail.Send | Application | Send emails on behalf of the application |
| Mail.Read | Application | Read emails from mailboxes |
| Mail.ReadWrite | Application | Read and modify emails |
| User.Read.All | Application | Read user information (optional) |

## Differences from SMTP/IMAP

### Advantages of Microsoft Graph API:
- ✅ **Modern authentication** - Uses OAuth 2.0 instead of passwords
- ✅ **Better security** - No need to store SMTP passwords
- ✅ **Unified API** - Single API for all Microsoft 365 services
- ✅ **Better integration** - Works seamlessly with Azure AD
- ✅ **Advanced features** - Access to calendar, contacts, etc.

### Migration from SMTP/IMAP:
If you're currently using SMTP/IMAP, you can:
1. Keep both implementations (SMTP for legacy, Graph for new)
2. Gradually migrate to Microsoft Graph API
3. Use Graph API for Office 365/Outlook accounts, SMTP for others

## Troubleshooting

### Common Issues

1. **"AADSTS7000215: Invalid client secret"**
   - Solution: Verify the client secret is correct and not expired

2. **"AADSTS700016: Application not found"**
   - Solution: Verify the ClientId and TenantId are correct

3. **"Insufficient privileges to complete the operation"**
   - Solution: Ensure API permissions are granted and admin consent is provided

4. **"User not found"**
   - Solution: Verify the UserEmail is correct and the mailbox exists

5. **"Mailbox not accessible"**
   - Solution: Ensure the service principal has permissions to access the mailbox

## Security Best Practices

1. ✅ Never commit secrets to source control
2. ✅ Use Azure Key Vault for production secrets
3. ✅ Rotate client secrets regularly
4. ✅ Use the least privilege principle for API permissions
5. ✅ Monitor access logs for suspicious activity
6. ✅ Use service accounts instead of user accounts when possible

## Testing the Integration

1. Configure client secret and user email
2. Start the application
3. Call the email service methods
4. Check logs for authentication and API calls
5. Verify emails are sent/received correctly

## Next Steps

- Configure additional API permissions as needed
- Set up monitoring and logging for email operations
- Implement email templates and formatting
- Add support for attachments
- Integrate with existing email workflows
