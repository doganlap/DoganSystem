# Email Server Credentials Setup

## ✅ Credentials Configured

The following credentials have been configured for the Email Server (Shahin-ai Server):

### User Secrets (Development)
- **User Email**: `info@doganconsult.com`
- **Client Secret**: Configured in User Secrets (not stored in source control)

### Configuration Details
- **Application ID**: `4e2575c6-e269-48eb-b055-ad730a2150a7`
- **Tenant ID**: `c8847e8a-33a0-4b6c-8e01-2e0e6b4aaef5`
- **User Email**: `info@doganconsult.com` (configured in appsettings.json)

## Security Notes

⚠️ **Important Security Information:**

1. **Client Secret**: Stored in User Secrets (local development only)
   - Location: `%APPDATA%\Microsoft\UserSecrets\<user-secrets-id>\secrets.json` (Windows)
   - Never commit this file to source control

2. **Production Setup**: For production, use:
   - Azure Key Vault
   - Environment variables
   - Secure configuration management

3. **Email Password**: The email password (`AhmEma$123456`) is **NOT** stored in the system
   - Microsoft Graph API uses OAuth 2.0 Client Credentials flow
   - No password authentication is required
   - The Client Secret is used instead

## Verification

To verify the credentials are set correctly:

```powershell
# Check User Secrets
cd src/DoganSystem.Web.Mvc
dotnet user-secrets list
```

You should see:
- `EmailServer:AzureAd:ClientSecret`
- `EmailServer:UserEmail`

## Next Steps

1. **Grant API Permissions** in Azure Portal:
   - Go to Azure Portal → App registrations → **Shahin-ai Server**
   - Navigate to **API permissions**
   - Add and grant consent for:
     - `Mail.Send` (Application)
     - `Mail.Read` (Application)
     - `Mail.ReadWrite` (Application)

2. **Test the Integration**:
   ```csharp
   var emailService = serviceProvider.GetRequiredService<IMicrosoftGraphEmailService>();
   var isValid = await emailService.ValidateConnectionAsync();
   ```

3. **Send Test Email**:
   ```csharp
   await emailService.SendEmailAsync(
       to: "test@example.com",
       subject: "Test Email",
       body: "This is a test email from DoganSystem"
   );
   ```

## Troubleshooting

### "Invalid client secret"
- Verify the client secret in User Secrets matches Azure Portal
- Check if the secret has expired (secrets expire after a set period)

### "Insufficient privileges"
- Ensure API permissions are granted
- Verify admin consent is provided

### "User not found"
- Verify `info@doganconsult.com` exists in Azure AD
- Check if the mailbox is accessible

## Production Deployment

For production, configure credentials using:

### Option 1: Azure Key Vault
```json
{
  "EmailServer": {
    "AzureAd": {
      "ClientSecret": "@Microsoft.KeyVault(SecretUri=https://your-vault.vault.azure.net/secrets/EmailServerClientSecret/)"
    }
  }
}
```

### Option 2: Environment Variables
```bash
export EmailServer__AzureAd__ClientSecret="your-secret"
export EmailServer__UserEmail="info@doganconsult.com"
```

### Option 3: App Service Configuration
- Azure Portal → App Service → Configuration → Application settings
- Add:
  - `EmailServer:AzureAd:ClientSecret`
  - `EmailServer:UserEmail`
