# Multi-Tenant SaaS Platform - API Documentation

## Base URLs

- **Tenant Management API**: `http://localhost:8002`
- **API Gateway**: `http://localhost:8006`
- **Webhook Receiver**: `http://localhost:8003`
- **Monitoring Dashboard**: `http://localhost:8005`
- **Tenant Admin API**: `http://localhost:8007`

## Authentication

### API Key Authentication

Include API key in header:
```
X-API-Key: ak_xxxxxxxxxxxx
```

### Tenant Identification

Tenant can be identified via:
1. **Subdomain**: `http://tenant1.yourdomain.com`
2. **Path**: `/api/tenant/{tenant_id}/...`
3. **Header**: `X-Tenant-ID: tenant_xxx`
4. **Query**: `?tenant_id=tenant_xxx`

## Admin Endpoints

### Create Tenant

```http
POST /api/admin/tenants
Content-Type: application/json

{
  "name": "Acme Corporation",
  "subdomain": "acme",
  "domain": "acme.com",
  "subscription_tier": "professional",
  "trial_days": 14
}
```

**Response:**
```json
{
  "success": true,
  "tenant": {
    "tenant_id": "tenant_abc123",
    "name": "Acme Corporation",
    "subdomain": "acme",
    "status": "trial",
    "subscription_tier": "professional"
  },
  "provisioning": {
    "database_created": true,
    "schema_initialized": true,
    "default_agents_created": true
  }
}
```

### List Tenants

```http
GET /api/admin/tenants?status=active&limit=100&offset=0
```

**Response:**
```json
[
  {
    "tenant_id": "tenant_abc123",
    "name": "Acme Corporation",
    "subdomain": "acme",
    "status": "active",
    "subscription_tier": "professional"
  }
]
```

### Get Tenant

```http
GET /api/admin/tenants/{tenant_id}
```

### Update Tenant

```http
PUT /api/admin/tenants/{tenant_id}
Content-Type: application/json

{
  "name": "Updated Name",
  "status": "active",
  "subscription_tier": "enterprise"
}
```

### Suspend Tenant

```http
POST /api/admin/tenants/{tenant_id}/suspend
```

### Activate Tenant

```http
POST /api/admin/tenants/{tenant_id}/activate
```

### Delete Tenant

```http
DELETE /api/admin/tenants/{tenant_id}
```

## Tenant-Scoped Endpoints

### Get Tenant Info

```http
GET /api/v1/tenant/info
X-Tenant-ID: tenant_xxx
```

**Response:**
```json
{
  "tenant_id": "tenant_xxx",
  "name": "Acme Corporation",
  "subdomain": "acme",
  "status": "active",
  "subscription_tier": "professional"
}
```

### Get Quota

```http
GET /api/v1/tenant/quota
X-Tenant-ID: tenant_xxx
```

**Response:**
```json
{
  "tenant_id": "tenant_xxx",
  "quota": {
    "max_agents": 20,
    "max_workflows": 50,
    "max_api_calls": 100000,
    "max_storage_gb": 50
  },
  "usage": {
    "agents": 5,
    "workflows": 10,
    "api_calls": 5000,
    "storage_gb": 2.5
  }
}
```

## Agent Management

### List Agents

```http
GET /api/v1/{tenant_id}/agents?department=Sales&status=available
```

**Response:**
```json
[
  {
    "agent_id": "agent_xxx",
    "employee_name": "أحمد السعود",
    "role": "Sales Manager",
    "department": "Sales",
    "status": "available",
    "capabilities": ["customer_management", "quotation"]
  }
]
```

### Create Agent

```http
POST /api/v1/{tenant_id}/agents
Content-Type: application/json

{
  "employee_name": "أحمد السعود",
  "role": "Sales Manager",
  "department": "Sales",
  "capabilities": ["customer_management", "quotation"]
}
```

### Update Agent

```http
PUT /api/v1/{tenant_id}/agents/{agent_id}
Content-Type: application/json

{
  "status": "busy",
  "role": "Senior Sales Manager"
}
```

### Delete Agent

```http
DELETE /api/v1/{tenant_id}/agents/{agent_id}
```

## Module Marketplace

### List Modules

```http
GET /api/v1/{tenant_id}/modules
```

**Response:**
```json
{
  "tenant_id": "tenant_xxx",
  "modules": [
    {
      "module_id": "sales_agent",
      "display_name": "Sales Agent Module",
      "description": "AI-powered sales agents",
      "category": "sales",
      "price_monthly": 49.00,
      "price_yearly": 490.00,
      "purchased": false
    }
  ]
}
```

### Purchase Module

```http
POST /api/v1/{tenant_id}/modules/{module_id}/purchase
```

**Response:**
```json
{
  "success": true,
  "tenant_id": "tenant_xxx",
  "module_id": "sales_agent",
  "module_name": "Sales Agent Module",
  "purchased_date": "2025-01-15T10:30:00"
}
```

## Billing

### Get Invoices

```http
GET /api/v1/{tenant_id}/billing/invoices?status=paid
```

**Response:**
```json
{
  "tenant_id": "tenant_xxx",
  "invoices": [
    {
      "invoice_id": "inv_xxx",
      "invoice_number": "INV-20250115-123456",
      "amount": 299.00,
      "currency": "SAR",
      "status": "paid",
      "due_date": "2025-01-29T00:00:00",
      "paid_date": "2025-01-16T14:30:00"
    }
  ]
}
```

### Create Subscription

```http
POST /api/v1/{tenant_id}/billing/subscription
Content-Type: application/json

{
  "plan_id": "professional",
  "billing_cycle": "monthly"
}
```

**Response:**
```json
{
  "subscription_id": "sub_xxx",
  "tenant_id": "tenant_xxx",
  "plan_id": "professional",
  "status": "active",
  "start_date": "2025-01-15T10:30:00",
  "end_date": "2025-02-15T10:30:00",
  "billing_cycle": "monthly"
}
```

## Monitoring

### Dashboard Overview

```http
GET /api/v1/{tenant_id}/dashboard/overview
```

**Response:**
```json
{
  "tenant_id": "tenant_xxx",
  "tenant_name": "Acme Corporation",
  "status": "active",
  "subscription_tier": "professional",
  "metrics": {
    "total_metrics": 150,
    "by_metric": {
      "api_calls": {
        "count": 50,
        "average": 200,
        "total": 10000
      }
    }
  },
  "usage": {
    "agents": 5,
    "workflows": 10,
    "api_calls": 5000
  },
  "agents": {
    "total": 5,
    "available": 3,
    "busy": 2
  },
  "quota": {
    "max_agents": 20,
    "max_workflows": 50
  }
}
```

### Get Metrics

```http
GET /api/v1/{tenant_id}/dashboard/metrics?metric_name=api_calls&limit=100
```

### Get Usage

```http
GET /api/v1/{tenant_id}/dashboard/usage
```

## Webhooks

### ERPNext Webhook

```http
POST /webhook/erpnext/{tenant_id}
Content-Type: application/json
X-Webhook-Signature: signature_xxx

{
  "event": "quotation_created",
  "data": {
    "quotation_id": "QUO-00001",
    "customer": "Customer ABC"
  }
}
```

**Response:**
```json
{
  "success": true,
  "tenant_id": "tenant_xxx",
  "event_type": "quotation_created",
  "message": "Webhook received and processed"
}
```

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad Request (missing/invalid parameters)
- `401` - Unauthorized (invalid API key)
- `403` - Forbidden (tenant not active)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

## Rate Limiting

API calls are tracked per tenant. Limits depend on subscription tier:
- **Starter**: 10,000 calls/month
- **Professional**: 100,000 calls/month
- **Enterprise**: Unlimited

When limit is exceeded, you'll receive:
```json
{
  "error": "Quota exceeded",
  "metric": "api_calls",
  "limit": 10000,
  "usage": 10001
}
```

## Pagination

List endpoints support pagination:

```http
GET /api/admin/tenants?limit=50&offset=0
```

**Parameters:**
- `limit`: Number of items per page (default: 100, max: 1000)
- `offset`: Number of items to skip (default: 0)

## Filtering

Many endpoints support filtering:

```http
GET /api/v1/{tenant_id}/agents?department=Sales&status=available
```

## Sorting

List endpoints return results sorted by creation date (newest first) by default.

## Examples

### Complete Tenant Setup Flow

```bash
# 1. Create tenant
TENANT=$(curl -X POST http://localhost:8002/api/admin/tenants \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Company",
    "subdomain": "mycompany",
    "subscription_tier": "professional"
  }' | jq -r '.tenant.tenant_id')

# 2. Create subscription
curl -X POST http://localhost:8006/api/v1/$TENANT/billing/subscription \
  -H "X-Tenant-ID: $TENANT" \
  -H "Content-Type: application/json" \
  -d '{"plan_id": "professional", "billing_cycle": "monthly"}'

# 3. Purchase module
curl -X POST http://localhost:8006/api/v1/$TENANT/modules/sales_agent/purchase \
  -H "X-Tenant-ID: $TENANT"

# 4. Get dashboard
curl http://localhost:8005/api/v1/$TENANT/dashboard/overview \
  -H "X-Tenant-ID: $TENANT"
```

## SDK Examples

### Python

```python
import requests

BASE_URL = "http://localhost:8006"
TENANT_ID = "tenant_xxx"
HEADERS = {"X-Tenant-ID": TENANT_ID}

# Get tenant info
response = requests.get(f"{BASE_URL}/api/v1/tenant/info", headers=HEADERS)
tenant = response.json()

# List agents
response = requests.get(f"{BASE_URL}/api/v1/{TENANT_ID}/agents", headers=HEADERS)
agents = response.json()
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8006';
const TENANT_ID = 'tenant_xxx';
const headers = { 'X-Tenant-ID': TENANT_ID };

// Get tenant info
const tenant = await axios.get(`${BASE_URL}/api/v1/tenant/info`, { headers });

// List agents
const agents = await axios.get(`${BASE_URL}/api/v1/${TENANT_ID}/agents`, { headers });
```

## Support

For API issues:
- Check response status codes
- Review error messages
- Verify tenant ID and API keys
- Check quota limits
