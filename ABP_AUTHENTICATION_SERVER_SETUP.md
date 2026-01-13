# ABP Authentication Server Setup Guide

## Overview

This guide explains how the ABP OpenIddict authentication server has been configured for DoganSystem.

## What Has Been Configured

### 1. OpenIddict Integration ✅

**Packages Added:**
- `Volo.Abp.Account.Web.OpenIddict` (v8.3.4)
- `Volo.Abp.Account.Application` (v8.3.4)
- `Volo.Abp.Account.HttpApi` (v8.3.4)
- `Volo.Abp.OpenIddict.EntityFrameworkCore` (v8.3.4)

### 2. Database Configuration ✅

**File:** `src/DoganSystem.EntityFrameworkCore/DoganSystemDbContext.cs`

- OpenIddict entities configured in DbContext
- `builder.ConfigureOpenIddict()` added

### 3. Module Dependencies ✅

**File:** `src/DoganSystem.Web.Mvc/DoganSystemWebMvcModule.cs`

- `AbpAccountWebOpenIddictModule` added
- `AbpAccountApplicationModule` added
- `AbpAccountHttpApiModule` added
- OpenIddict options pre-configured

### 4. Application Configuration ✅

**File:** `src/DoganSystem.Web.Mvc/appsettings.json`

OpenIddict applications configured:
- **DoganSystem_Web** - Web application client
- **DoganSystem_App** - Mobile/desktop application client

### 5. Seed Data ✅

**File:** `src/DoganSystem.Application/Seed/OpenIddictDataSeedContributor.cs`

- Automatically seeds OpenIddict applications
- Automatically seeds OpenIddict scopes
- Runs on application startup

---

## Authentication Endpoints

Once the application is running, the following endpoints are available:

### Authorization Endpoint
```
GET /connect/authorize
```

### Token Endpoint
```
POST /connect/token
```

### UserInfo Endpoint
```
GET /connect/userinfo
```

### Logout Endpoint
```
GET /connect/logout
```

### Discovery Document
```
GET /.well-known/openid-configuration
```

---

## Supported Grant Types

### 1. Authorization Code Flow
- **Use Case:** Web applications
- **Client:** DoganSystem_Web
- **Redirect URIs:** Configured in appsettings.json

### 2. Password Grant (Resource Owner Password Credentials)
- **Use Case:** Trusted applications
- **Client:** DoganSystem_App
- **Note:** Use with caution, only for trusted clients

### 3. Client Credentials
- **Use Case:** Service-to-service authentication
- **Client:** DoganSystem_App

### 4. Refresh Token
- **Use Case:** Token renewal
- **Supported by:** All clients

---

## Configuration

### appsettings.json

```json
{
  "OpenIddict": {
    "Applications": {
      "DoganSystem_Web": {
        "ClientId": "DoganSystem_Web",
        "RootUrl": "https://localhost:5001",
        "ClientSecret": "",
        "Scopes": ["openid", "profile", "email", "role", "phone", "address"],
        "GrantTypes": ["authorization_code", "password", "client_credentials", "implicit", "refresh_token"],
        "RedirectUris": [
          "https://localhost:5001/signin-oidc",
          "https://localhost:5001/swagger/oauth2-redirect.html"
        ],
        "PostLogoutRedirectUris": [
          "https://localhost:5001/signout-callback-oidc"
        ]
      }
    },
    "Resources": {
      "DoganSystem": {
        "DisplayName": "DoganSystem API",
        "Scopes": ["openid", "profile", "email", "role", "phone", "address"]
      }
    }
  }
}
```

---

## Getting an Access Token

### Using Authorization Code Flow

1. **Redirect to authorization endpoint:**
```
GET /connect/authorize?
  client_id=DoganSystem_Web&
  redirect_uri=https://localhost:5001/signin-oidc&
  response_type=code&
  scope=openid profile email&
  state=xyz
```

2. **User authenticates and authorizes**

3. **Exchange code for token:**
```
POST /connect/token
Content-Type: application/x-www-form-urlencoded

client_id=DoganSystem_Web&
client_secret=YOUR_SECRET&
code=AUTHORIZATION_CODE&
redirect_uri=https://localhost:5001/signin-oidc&
grant_type=authorization_code
```

### Using Password Grant (for trusted apps)

```
POST /connect/token
Content-Type: application/x-www-form-urlencoded

client_id=DoganSystem_App&
client_secret=YOUR_SECRET&
username=USERNAME&
password=PASSWORD&
grant_type=password&
scope=openid profile email
```

### Using Client Credentials (for services)

```
POST /connect/token
Content-Type: application/x-www-form-urlencoded

client_id=DoganSystem_App&
client_secret=YOUR_SECRET&
grant_type=client_credentials&
scope=openid
```

---

## Using the Access Token

Once you have an access token, include it in API requests:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Example:
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     https://localhost:5001/api/tenants
```

---

## Swagger Integration

Swagger UI is configured to support OAuth2 authentication:

1. Navigate to `/swagger`
2. Click "Authorize" button
3. Use client credentials:
   - **Client ID:** DoganSystem_Web
   - **Client Secret:** (if configured)
4. Authorize and use the API

---

## Security Best Practices

### 1. Client Secrets
- **Development:** Can be empty for public clients
- **Production:** Always use strong, randomly generated secrets
- **Storage:** Use Azure Key Vault or environment variables

### 2. Redirect URIs
- **Development:** `https://localhost:5001/*`
- **Production:** Use your actual domain
- **Never:** Use wildcards in production

### 3. Grant Types
- **Web Apps:** Use `authorization_code` only
- **Mobile Apps:** Use `authorization_code` with PKCE
- **Services:** Use `client_credentials`
- **Avoid:** `password` grant in production (use only for trusted apps)

### 4. Scopes
- **Principle:** Request only necessary scopes
- **Default:** `openid profile email`
- **Custom:** Add custom scopes as needed

---

## Database Migrations

After adding OpenIddict, you need to create a migration:

```bash
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add AddOpenIddict
dotnet ef database update
```

---

## Testing the Authentication Server

### 1. Check Discovery Document
```bash
curl https://localhost:5001/.well-known/openid-configuration
```

### 2. Test Token Endpoint
```bash
curl -X POST https://localhost:5001/connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=DoganSystem_App&grant_type=client_credentials&scope=openid"
```

### 3. Test Protected Endpoint
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://localhost:5001/api/tenants
```

---

## Troubleshooting

### Issue: "Invalid client"
**Solution:** Check that the client ID exists in the database and matches appsettings.json

### Issue: "Invalid redirect_uri"
**Solution:** Ensure the redirect URI in the request matches one configured in appsettings.json

### Issue: "Invalid grant_type"
**Solution:** Verify the grant type is enabled for the client in appsettings.json

### Issue: "Invalid scope"
**Solution:** Check that the requested scopes are configured in the resource definition

---

## Next Steps

1. **Run Database Migration**
   ```bash
   dotnet ef migrations add AddOpenIddict
   dotnet ef database update
   ```

2. **Configure Production Settings**
   - Update `appsettings.Production.json` with production URLs
   - Set strong client secrets
   - Configure proper redirect URIs

3. **Test Authentication Flow**
   - Test authorization code flow
   - Test token refresh
   - Test API access with tokens

4. **Add Custom Scopes** (if needed)
   - Define custom scopes in appsettings.json
   - Update seed data contributor

---

## References

- [ABP OpenIddict Documentation](https://docs.abp.io/en/abp/latest/Modules/OpenIddict)
- [OpenIddict Documentation](https://documentation.openiddict.com/)
- [OAuth 2.0 Specification](https://oauth.net/2/)

---

**Status:** ✅ **CONFIGURED AND READY**

The ABP authentication server is fully configured. Run database migrations and start testing the authentication flows.
