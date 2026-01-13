# Microsoft Copilot Studio Integration Guide

## Overview

This guide explains how to configure Microsoft Copilot Studio integration with DoganSystem using Azure AD authentication.

## Azure AD App Registration Details

The following Azure AD application has been configured:

- **Display Name**: Agent (Microsoft Copilot Studio)
- **Application (Client) ID**: `1bc8f3e9-f550-40e7-854d-9f60d7788423`
- **Object ID**: `7f9cac51-dacf-4195-a2c0-f209b161014a`
- **Directory (Tenant) ID**: `c8847e8a-33a0-4b6c-8e01-2e0e6b4aaef5`
- **Application ID URI**: `api://1bc8f3e9-f550-40e7-854d-9f60d7788423`
- **Supported Account Types**: My organization only

## Configuration Steps

### 1. Add Client Secret

You need to add a client secret from Azure AD to your configuration:

1. Go to Azure Portal → Azure Active Directory → App registrations
2. Select your app: **Agent (Microsoft Copilot Studio)**
3. Navigate to **Certificates & secrets**
4. Create a new client secret
5. Copy the secret value (you can only see it once)
6. Add it to your `appsettings.json` or `appsettings.Production.json`:

```json
{
  "AzureAd": {
    "ClientSecret": "your-client-secret-here"
  }
}
```

**Important**: Never commit client secrets to source control. Use:
- User Secrets for development: `dotnet user-secrets set "AzureAd:ClientSecret" "your-secret"`
- Azure Key Vault for production
- Environment variables

### 2. Configure Redirect URIs

Add the following redirect URIs in Azure AD:

1. Go to Azure Portal → App registrations → Your app → Authentication
2. Add redirect URIs:
   - `https://your-domain.com/signin-oidc` (Production)
   - `https://localhost:5001/signin-oidc` (Development)
   - `http://localhost:5000/signin-oidc` (Development HTTP)

### 3. Configure API Permissions

1. Go to Azure Portal → App registrations → Your app → API permissions
2. Add required permissions:
   - Microsoft Graph: `User.Read`
   - Microsoft Graph: `openid`
   - Microsoft Graph: `profile`
   - Microsoft Graph: `email`

### 4. Update appsettings.json

The configuration has been added to `appsettings.json`:

```json
{
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "TenantId": "c8847e8a-33a0-4b6c-8e01-2e0e6b4aaef5",
    "ClientId": "1bc8f3e9-f550-40e7-854d-9f60d7788423",
    "CallbackPath": "/signin-oidc",
    "SignedOutCallbackPath": "/signout-callback-oidc",
    "ClientSecret": "",  // Add your secret here
    "Scopes": "openid profile email",
    "ApplicationIdUri": "api://1bc8f3e9-f550-40e7-854d-9f60d7788423"
  },
  "MicrosoftCopilotStudio": {
    "ApplicationId": "1bc8f3e9-f550-40e7-854d-9f60d7788423",
    "ObjectId": "7f9cac51-dacf-4195-a2c0-f209b161014a",
    "TenantId": "c8847e8a-33a0-4b6c-8e01-2e0e6b4aaef5",
    "ApplicationIdUri": "api://1bc8f3e9-f550-40e7-854d-9f60d7788423",
    "SupportedAccountTypes": "My organization only"
  }
}
```

## Using User Secrets (Development)

For local development, use .NET User Secrets:

```powershell
dotnet user-secrets init --project src/DoganSystem.Web.Mvc
dotnet user-secrets set "AzureAd:ClientSecret" "your-client-secret-here" --project src/DoganSystem.Web.Mvc
```

## Authentication Flow

1. User navigates to a protected page
2. Application redirects to Azure AD login
3. User authenticates with Microsoft account
4. Azure AD redirects back with authorization code
5. Application exchanges code for tokens
6. User is authenticated and can access the application

## Accessing Configuration in Code

```csharp
using DoganSystem.Application.Configuration;
using Microsoft.Extensions.Options;

public class MyService
{
    private readonly MicrosoftCopilotStudioOptions _options;
    
    public MyService(IOptions<MicrosoftCopilotStudioOptions> options)
    {
        _options = options.Value;
    }
    
    public void UseConfiguration()
    {
        var appId = _options.ApplicationId;
        var tenantId = _options.TenantId;
        // Use the configuration
    }
}
```

## Testing the Integration

1. Start the application
2. Navigate to any protected page
3. You should be redirected to Microsoft login
4. After successful login, you'll be redirected back to the application

## Troubleshooting

### Common Issues

1. **"AADSTS50011: The reply URL specified in the request does not match"**
   - Solution: Ensure redirect URIs in Azure AD match your application URLs

2. **"AADSTS7000215: Invalid client secret"**
   - Solution: Verify the client secret is correct and not expired

3. **"AADSTS700016: Application not found"**
   - Solution: Verify the ClientId and TenantId are correct

## Security Best Practices

1. ✅ Never commit secrets to source control
2. ✅ Use Azure Key Vault for production secrets
3. ✅ Rotate client secrets regularly
4. ✅ Use HTTPS in production
5. ✅ Implement proper token validation
6. ✅ Use the least privilege principle for API permissions

## Next Steps

- Configure additional API permissions as needed
- Set up token caching for better performance
- Implement role-based access control (RBAC)
- Add logging for authentication events
