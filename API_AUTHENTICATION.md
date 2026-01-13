# API Authentication Documentation - DoganSystem

Complete guide for authenticating with the DoganSystem API.

## Table of Contents

1. [Overview](#overview)
2. [Authentication Methods](#authentication-methods)
3. [API Key Management](#api-key-management)
4. [Request Examples](#request-examples)
5. [Rate Limiting](#rate-limiting)
6. [Error Responses](#error-responses)
7. [Security Best Practices](#security-best-practices)

---

## Overview

DoganSystem uses multiple authentication methods depending on the type of access:

- **API Keys** - For programmatic access from external applications
- **JWT Tokens** - For web application sessions
- **OAuth 2.0** - For third-party integrations (optional)

### Base URLs

```
Production:    https://api.doganconsult.com
Development:   http://localhost:8006
```

---

## Authentication Methods

### Method 1: API Key Authentication

**Best For:** Server-to-server communication, CLI tools, automated scripts

#### How It Works

1. Generate API key and secret from the dashboard
2. Include API key in the `X-API-Key` header
3. Sign requests with API secret (optional but recommended for production)

#### Headers Required

```http
X-API-Key: ak_1234567890abcdef
X-Tenant-ID: tenant_abc123xyz
Content-Type: application/json
```

#### Example Request

```bash
curl -X GET https://api.doganconsult.com/api/v1/tenant/info \
  -H "X-API-Key: ak_1234567890abcdef" \
  -H "X-Tenant-ID: tenant_abc123xyz"
```

---

### Method 2: JWT Token Authentication

**Best For:** Web applications, mobile apps, single-page applications

#### Obtaining a Token

```bash
POST /api/auth/token
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your-password"
}
```

#### Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "def50200..."
}
```

#### Using the Token

```bash
curl -X GET https://api.doganconsult.com/api/v1/agents \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Refreshing Tokens

```bash
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "def50200..."
}
```

---

### Method 3: Tenant Subdomain Authentication

**Best For:** Multi-tenant web access

Access your tenant via subdomain:

```
https://yourcompany.doganconsult.com
```

The tenant is automatically identified by the subdomain. Users log in with their credentials, and sessions are managed via cookies.

---

## API Key Management

### Generating API Keys

#### Via Web Dashboard

1. Log in to [https://doganconsult.com](https://doganconsult.com)
2. Navigate to **Settings** → **API Access**
3. Click **Generate New API Key**
4. Provide a descriptive name (e.g., "Production Server", "CI/CD Pipeline")
5. Copy the API key and secret immediately (secret is only shown once)

#### Via API (Requires Admin Access)

```bash
POST /api/v1/tenant/api-keys
Authorization: Bearer {admin-token}
Content-Type: application/json

{
  "name": "Production Server",
  "expires_at": null  // null = never expires, or ISO 8601 date
}
```

#### Response

```json
{
  "key_id": "key_abc123",
  "api_key": "ak_1234567890abcdef",
  "api_secret": "as_0987654321fedcba",
  "name": "Production Server",
  "created_at": "2026-01-13T10:30:00Z",
  "expires_at": null
}
```

**⚠️ IMPORTANT:** Store the `api_secret` securely. It will not be shown again.

---

### Listing API Keys

```bash
GET /api/v1/tenant/api-keys
Authorization: Bearer {token}
```

#### Response

```json
{
  "keys": [
    {
      "key_id": "key_abc123",
      "name": "Production Server",
      "api_key": "ak_1234567890abcdef",
      "created_at": "2026-01-13T10:30:00Z",
      "last_used": "2026-01-13T15:45:00Z",
      "expires_at": null,
      "status": "active"
    }
  ]
}
```

**Note:** `api_secret` is never returned in list responses for security.

---

### Revoking API Keys

```bash
DELETE /api/v1/tenant/api-keys/{key_id}
Authorization: Bearer {token}
```

#### Response

```json
{
  "success": true,
  "message": "API key revoked successfully",
  "key_id": "key_abc123"
}
```

---

## Request Examples

### Python Example

```python
import requests

API_BASE = "https://api.doganconsult.com"
API_KEY = "ak_1234567890abcdef"
TENANT_ID = "tenant_abc123xyz"

headers = {
    "X-API-Key": API_KEY,
    "X-Tenant-ID": TENANT_ID,
    "Content-Type": "application/json"
}

# Get tenant information
response = requests.get(
    f"{API_BASE}/api/v1/tenant/info",
    headers=headers
)

print(response.json())
```

---

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

const API_BASE = 'https://api.doganconsult.com';
const API_KEY = 'ak_1234567890abcdef';
const TENANT_ID = 'tenant_abc123xyz';

const headers = {
  'X-API-Key': API_KEY,
  'X-Tenant-ID': TENANT_ID,
  'Content-Type': 'application/json'
};

// Get tenant information
axios.get(`${API_BASE}/api/v1/tenant/info`, { headers })
  .then(response => console.log(response.data))
  .catch(error => console.error('Error:', error.response.data));
```

---

### cURL Example with JWT

```bash
# 1. Get access token
TOKEN=$(curl -X POST https://api.doganconsult.com/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"your-password"}' \
  | jq -r '.access_token')

# 2. Make authenticated request
curl -X GET https://api.doganconsult.com/api/v1/agents \
  -H "Authorization: Bearer $TOKEN"
```

---

## Rate Limiting

### Default Limits

- **API Key**: 100 requests per minute per tenant
- **JWT Token**: 60 requests per minute per user
- **Public Endpoints**: 10 requests per minute per IP

### Rate Limit Headers

Every API response includes rate limit information:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642097400
```

### Rate Limit Exceeded Response

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Please try again in 30 seconds.",
  "retry_after": 30,
  "limit": 100,
  "reset_at": "2026-01-13T10:35:00Z"
}
```

### Increasing Rate Limits

Contact support@doganconsult.com or upgrade your subscription plan for higher limits.

---

## Error Responses

### Error Response Format

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {
    "field": "email",
    "reason": "Invalid format"
  },
  "request_id": "req_abc123"
}
```

### Common Error Codes

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 400 | `invalid_request` | Malformed request or missing required parameters |
| 401 | `unauthorized` | Missing or invalid authentication credentials |
| 403 | `forbidden` | Valid credentials but insufficient permissions |
| 404 | `not_found` | Requested resource does not exist |
| 409 | `conflict` | Request conflicts with current state (e.g., duplicate email) |
| 422 | `validation_error` | Request validation failed |
| 429 | `rate_limit_exceeded` | Too many requests |
| 500 | `internal_error` | Server error (contact support if persists) |
| 503 | `service_unavailable` | Service temporarily unavailable (maintenance or overload) |

### Authentication Error Examples

#### Invalid API Key

```http
HTTP/1.1 401 Unauthorized

{
  "error": "invalid_api_key",
  "message": "The provided API key is invalid or has been revoked",
  "request_id": "req_abc123"
}
```

#### Missing Tenant ID

```http
HTTP/1.1 400 Bad Request

{
  "error": "missing_tenant_id",
  "message": "X-Tenant-ID header is required for this endpoint",
  "request_id": "req_abc123"
}
```

#### Expired Token

```http
HTTP/1.1 401 Unauthorized

{
  "error": "token_expired",
  "message": "JWT token has expired. Please obtain a new token or use your refresh token.",
  "expired_at": "2026-01-13T10:00:00Z",
  "request_id": "req_abc123"
}
```

---

## Security Best Practices

### 1. Protect Your Secrets

```bash
# ✅ DO: Store in environment variables
export DOGANSYSTEM_API_KEY="ak_1234567890abcdef"
export DOGANSYSTEM_API_SECRET="as_0987654321fedcba"

# ❌ DON'T: Hardcode in source code
api_key = "ak_1234567890abcdef"  # NEVER do this!
```

### 2. Use HTTPS Only

Always use `https://` URLs in production:

```python
# ✅ DO
API_BASE = "https://api.doganconsult.com"

# ❌ DON'T
API_BASE = "http://api.doganconsult.com"  # Insecure!
```

### 3. Rotate API Keys Regularly

```bash
# Rotate keys every 90 days
1. Generate new API key
2. Update applications to use new key
3. Test applications
4. Revoke old API key
```

### 4. Use Separate Keys for Different Environments

```bash
PRODUCTION_API_KEY=ak_prod_...
STAGING_API_KEY=ak_staging_...
DEVELOPMENT_API_KEY=ak_dev_...
```

### 5. Implement Retry Logic with Exponential Backoff

```python
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(
    total=3,
    backoff_factor=1,  # 1s, 2s, 4s
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

response = session.get(url, headers=headers)
```

### 6. Validate SSL Certificates

```python
# ✅ DO: Verify SSL certificates
response = requests.get(url, headers=headers, verify=True)

# ❌ DON'T: Disable SSL verification
response = requests.get(url, headers=headers, verify=False)  # NEVER do this!
```

### 7. Monitor API Key Usage

- Regularly check `last_used` timestamp for unexpected activity
- Set up alerts for unusual usage patterns
- Review audit logs monthly

### 8. Use Request Signing (Advanced)

For sensitive operations, sign requests with your API secret:

```python
import hmac
import hashlib
import time

def sign_request(api_secret, method, path, body=""):
    timestamp = str(int(time.time()))
    message = f"{method}:{path}:{timestamp}:{body}"
    signature = hmac.new(
        api_secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature, timestamp

# Usage
signature, timestamp = sign_request(API_SECRET, "POST", "/api/v1/data", json.dumps(data))
headers = {
    "X-API-Key": API_KEY,
    "X-Signature": signature,
    "X-Timestamp": timestamp
}
```

---

## API Endpoints Reference

### Authentication Endpoints

```
POST   /api/auth/token          # Obtain JWT token
POST   /api/auth/refresh        # Refresh JWT token
POST   /api/auth/logout         # Invalidate token
```

### Tenant Management

```
GET    /api/v1/tenant/info      # Get tenant information
PUT    /api/v1/tenant/settings  # Update tenant settings
GET    /api/v1/tenant/usage     # Get usage statistics
```

### API Key Management

```
GET    /api/v1/tenant/api-keys          # List API keys
POST   /api/v1/tenant/api-keys          # Generate new API key
DELETE /api/v1/tenant/api-keys/{key_id} # Revoke API key
```

### Agent Management

```
GET    /api/v1/agents           # List agents
POST   /api/v1/agents           # Create agent
GET    /api/v1/agents/{id}      # Get agent details
PUT    /api/v1/agents/{id}      # Update agent
DELETE /api/v1/agents/{id}      # Delete agent
```

### ERPNext Integration

```
GET    /api/v1/erpnext/customers        # List customers
POST   /api/v1/erpnext/sales-orders     # Create sales order
GET    /api/v1/erpnext/invoices         # List invoices
```

### Health & Status

```
GET    /health                  # Comprehensive health check
GET    /                        # API status
```

---

## Testing Your Integration

### Health Check

```bash
curl -X GET https://api.doganconsult.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "api-gateway",
  "version": "2.0.0",
  "timestamp": "2026-01-13T10:30:00Z"
}
```

### Authenticated Request Test

```bash
curl -X GET https://api.doganconsult.com/api/v1/tenant/info \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "X-Tenant-ID: YOUR_TENANT_ID"
```

---

## Support & Resources

- **Documentation:** [https://doganconsult.com/docs](https://doganconsult.com/docs)
- **API Status:** [https://status.doganconsult.com](https://status.doganconsult.com)
- **Support Email:** support@doganconsult.com
- **Security Issues:** security@doganconsult.com
- **GitHub:** [https://github.com/doganlap/DoganSystem](https://github.com/doganlap/DoganSystem)

---

**Last Updated:** 2026-01-13
**API Version:** 2.0.0
