# Environment Variables Documentation - DoganSystem

Complete reference for all environment variables used in DoganSystem.

## Table of Contents

1. [Critical Configuration](#critical-configuration)
2. [AI & Claude Configuration](#ai--claude-configuration)
3. [ERPNext Configuration](#erpnext-configuration)
4. [Database Configuration](#database-configuration)
5. [Email Configuration](#email-configuration)
6. [Redis Configuration](#redis-configuration)
7. [Security & Authentication](#security--authentication)
8. [Application Settings](#application-settings)
9. [Feature Flags](#feature-flags)
10. [Monitoring & Logging](#monitoring--logging)
11. [Network & Domain](#network--domain)
12. [Billing Configuration](#billing-configuration)

---

## Critical Configuration

### CLAUDE_API_KEY
- **Type:** String (Required)
- **Default:** None
- **Format:** `sk-ant-api03-xxxxxxxxxxxxx`
- **Description:** Anthropic Claude AI API key for AI agent functionality
- **How to Obtain:**
  1. Visit [https://console.anthropic.com/](https://console.anthropic.com/)
  2. Create account or sign in
  3. Navigate to API Keys section
  4. Generate new API key
- **Validation:** Must not contain placeholders like "YOUR_ANTHROPIC_API_KEY", "REPLACE", "TODO"
- **Used By:** API Gateway, Agent Server, all AI services

### CLAUDE_MODEL
- **Type:** String (Optional)
- **Default:** `claude-sonnet-4-20250514`
- **Options:**
  - `claude-opus-4-5-20251101` (most capable)
  - `claude-sonnet-4-20250514` (balanced)
  - `claude-haiku-3-5-20241022` (fast)
- **Description:** Claude model version to use for AI operations
- **Used By:** All Python AI services

---

## AI & Claude Configuration

### MAX_AGENTS
- **Type:** Integer
- **Default:** `10`
- **Range:** 1-100
- **Description:** Maximum number of concurrent AI agents per tenant
- **Used By:** Agent Orchestrator

### RATE_LIMIT_PER_AGENT
- **Type:** Integer
- **Default:** `100`
- **Description:** Maximum API calls per agent within the time window
- **Used By:** API Gateway rate limiting

### RATE_LIMIT_WINDOW
- **Type:** Integer
- **Default:** `60`
- **Unit:** Seconds
- **Description:** Time window for rate limiting calculations
- **Used By:** API Gateway rate limiting

---

## ERPNext Configuration

### ERPNEXT_BASE_URL
- **Type:** URL (Required)
- **Default:** `http://erpnext:8000`
- **Format:** `http://hostname:port` or `https://hostname`
- **Description:** Base URL for ERPNext instance
- **Examples:**
  - Docker: `http://erpnext:8000`
  - External: `https://erp.yourdomain.com`
- **Used By:** All services connecting to ERPNext

### ERPNEXT_API_KEY
- **Type:** String (Required after setup)
- **Default:** `REPLACE_AFTER_SETUP`
- **Description:** ERPNext API key for authentication
- **How to Obtain:**
  1. Login to ERPNext as Administrator
  2. Go to User Menu → API Access
  3. Click "Generate Keys"
  4. Copy the API Key
- **Validation:** Must not contain "REPLACE", "TODO", or other placeholders
- **Used By:** ERPNext integration services

### ERPNEXT_API_SECRET
- **Type:** String (Required after setup)
- **Default:** `REPLACE_AFTER_SETUP`
- **Description:** ERPNext API secret for authentication
- **How to Obtain:** Generated alongside ERPNEXT_API_KEY
- **Validation:** Must not contain placeholders
- **Used By:** ERPNext integration services

### ERPNEXT_TIMEOUT
- **Type:** Integer
- **Default:** `30`
- **Unit:** Seconds
- **Description:** Timeout for ERPNext API requests
- **Range:** 10-300
- **Used By:** ERPNext HTTP client

### ERPNEXT_ADMIN_PASSWORD
- **Type:** String (Required)
- **Default:** `REPLACE_WITH_STRONG_PASSWORD_MIN_16_CHARS`
- **Requirements:**
  - Minimum 16 characters
  - Must not be "admin", "admin123", "password"
- **Description:** Administrator password for ERPNext
- **Security:** Change immediately after first setup
- **Used By:** ERPNext container initialization

---

## Database Configuration

### MYSQL_ROOT_PASSWORD
- **Type:** String (Required)
- **Default:** `REPLACE_WITH_STRONG_PASSWORD_MIN_16_CHARS`
- **Requirements:** Minimum 16 characters, strong password
- **Description:** MySQL/MariaDB root password for ERPNext database
- **Validation:** Checked at startup, must be strong
- **Used By:** ERPNext database (MariaDB)

### MYSQL_PASSWORD
- **Type:** String (Required)
- **Default:** `REPLACE_WITH_STRONG_PASSWORD_MIN_16_CHARS`
- **Requirements:** Minimum 16 characters
- **Description:** MySQL password for 'erpnext' database user
- **Used By:** ERPNext application database access

### PLATFORM_DB_PATH
- **Type:** File Path
- **Default:** `/app/data/platform.db`
- **Description:** SQLite database path for platform-level data
- **Format:** Absolute path
- **Used By:** API Gateway, Tenant Manager

### TENANT_DB_DIR
- **Type:** Directory Path
- **Default:** `/app/data/tenant_databases`
- **Description:** Directory for tenant-specific SQLite databases
- **Format:** Absolute path
- **Used By:** Tenant Isolation system

---

## Email Configuration

### SMTP_SERVER
- **Type:** Hostname (Required for email features)
- **Default:** `smtp.gmail.com`
- **Description:** SMTP server hostname for sending emails
- **Examples:**
  - Gmail: `smtp.gmail.com`
  - Office 365: `smtp.office365.com`
  - AWS SES: `email-smtp.us-east-1.amazonaws.com`
- **Used By:** Email notification services

### SMTP_PORT
- **Type:** Integer
- **Default:** `587`
- **Common Ports:**
  - `587` - TLS (recommended)
  - `465` - SSL
  - `25` - Unencrypted (not recommended)
- **Description:** SMTP server port
- **Used By:** Email SMTP client

### SMTP_USERNAME
- **Type:** String (Required for email)
- **Default:** `your-email@gmail.com`
- **Description:** SMTP authentication username (usually email address)
- **Used By:** Email authentication

### SMTP_PASSWORD
- **Type:** String (Required for email)
- **Default:** `your-app-specific-password`
- **Description:** SMTP authentication password
- **Note:** For Gmail, use App-Specific Password, not account password
- **How to Obtain (Gmail):**
  1. Enable 2-Factor Authentication
  2. Go to Google Account → Security → App Passwords
  3. Generate password for "Mail" application
- **Used By:** Email authentication

### SMTP_USE_TLS
- **Type:** Boolean
- **Default:** `true`
- **Options:** `true`, `false`
- **Description:** Enable TLS encryption for SMTP
- **Used By:** Email client configuration

### IMAP_SERVER
- **Type:** Hostname (Optional)
- **Default:** `imap.gmail.com`
- **Description:** IMAP server for email processing features
- **Used By:** Email processing agent (if enabled)

### IMAP_PORT
- **Type:** Integer
- **Default:** `993`
- **Description:** IMAP server port (993 for SSL)
- **Used By:** Email processing agent

---

## Redis Configuration

### REDIS_HOST
- **Type:** Hostname (Required)
- **Default:** `redis`
- **Description:** Redis server hostname
- **Examples:**
  - Docker: `redis`
  - External: `redis.yourdomain.com`
- **Used By:** All services using caching/message queue

### REDIS_PORT
- **Type:** Integer
- **Default:** `6379`
- **Description:** Redis server port
- **Used By:** Redis client connection

### REDIS_PASSWORD
- **Type:** String (Required)
- **Default:** `REPLACE_WITH_STRONG_PASSWORD_MIN_16_CHARS`
- **Requirements:** Minimum 16 characters
- **Description:** Redis authentication password
- **Validation:** Checked at startup
- **Used By:** Redis server and all Redis clients

---

## Security & Authentication

### GRAFANA_ADMIN_PASSWORD
- **Type:** String (Required)
- **Default:** `REPLACE_WITH_STRONG_PASSWORD_MIN_16_CHARS`
- **Requirements:** Minimum 16 characters
- **Description:** Grafana dashboard admin password
- **Used By:** Grafana container

### ADMIN_PASSWORD
- **Type:** String (Required)
- **Description:** ABP Framework admin user password
- **Requirements:** Strong password as per validation rules
- **Used By:** C# application user seeding

### DB_PASSWORD
- **Type:** String (Required)
- **Description:** PostgreSQL database password (if using PostgreSQL)
- **Used By:** Main application database connection

---

## Application Settings

### ASPNETCORE_ENVIRONMENT
- **Type:** String
- **Default:** `Production`
- **Options:** `Development`, `Staging`, `Production`
- **Description:** ASP.NET Core application environment
- **Used By:** C# web application

### ASPNETCORE_URLS
- **Type:** URL
- **Default:** `http://+:5000`
- **Description:** URLs the web application listens on
- **Used By:** C# web application Kestrel server

### APP_SELF_URL
- **Type:** URL (Required)
- **Default:** `https://doganconsult.com`
- **Description:** Public URL where application is accessible
- **Used By:** CORS, redirects, email links

### CORS_ORIGINS
- **Type:** Comma-separated URLs (Required)
- **Default:** `https://doganconsult.com,https://www.doganconsult.com,...`
- **Description:** Allowed origins for CORS requests
- **Format:** Comma-separated list of full URLs (no trailing slash)
- **Used By:** API Gateway, Web Application CORS middleware

---

## Feature Flags

### ENABLE_AUTONOMOUS_WORKFLOWS
- **Type:** Boolean
- **Default:** `true`
- **Options:** `true`, `false`
- **Description:** Enable AI agents to execute workflows autonomously
- **Used By:** Unified Orchestrator

### ENABLE_SELF_HEALING
- **Type:** Boolean
- **Default:** `true`
- **Description:** Enable automatic error recovery and self-healing
- **Used By:** Monitoring service

### ENABLE_EMAIL_PROCESSING
- **Type:** Boolean
- **Default:** `true`
- **Description:** Enable email monitoring and processing by AI agents
- **Used By:** Email processing agent

### ENABLE_EMPLOYEE_AGENTS
- **Type:** Boolean
- **Default:** `true`
- **Description:** Enable virtual employee agents functionality
- **Used By:** Employee agent system

### ENABLE_MULTI_TENANT
- **Type:** Boolean
- **Default:** `true`
- **Description:** Enable multi-tenant mode
- **Used By:** Tenant isolation system

### ENABLE_KSA_LOCALIZATION
- **Type:** Boolean
- **Default:** `true`
- **Description:** Enable Saudi Arabia-specific features and localization
- **Used By:** Localization services

### ENABLE_MONITORING
- **Type:** Boolean
- **Default:** `true`
- **Description:** Enable system monitoring and metrics collection
- **Used By:** Metrics collector

### AUTO_PROVISION_NEW_TENANTS
- **Type:** Boolean
- **Default:** `true`
- **Description:** Automatically provision resources for new tenants
- **Used By:** Tenant manager

---

## Monitoring & Logging

### LOG_LEVEL
- **Type:** String
- **Default:** `INFO`
- **Options:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Description:** Logging verbosity level
- **Used By:** All Python services

### LOG_AGENT_ACTIONS
- **Type:** Boolean
- **Default:** `true`
- **Description:** Log all AI agent actions for audit trail
- **Used By:** Agent orchestrator, audit system

---

## Network & Domain

### DOMAIN_NAME
- **Type:** Domain name (Required)
- **Default:** `doganconsult.com`
- **Description:** Primary domain name for the application
- **Used By:** Nginx configuration, SSL certificate

### SSL_CERTIFICATE_PATH
- **Type:** File path (Required for HTTPS)
- **Default:** `/etc/nginx/ssl/fullchain.pem`
- **Description:** Path to SSL certificate file
- **Used By:** Nginx SSL configuration

### SSL_PRIVATE_KEY_PATH
- **Type:** File path (Required for HTTPS)
- **Default:** `/etc/nginx/ssl/privkey.pem`
- **Description:** Path to SSL private key file
- **Used By:** Nginx SSL configuration

---

## Billing Configuration

### BILLING_PROVIDER
- **Type:** String (Optional)
- **Default:** `stripe`
- **Options:** `stripe`, `paypal`, `manual`
- **Description:** Payment provider for SaaS billing
- **Used By:** Billing service

### STRIPE_SECRET_KEY
- **Type:** String (Required if using Stripe)
- **Default:** `sk_live_REPLACE_WITH_YOUR_STRIPE_KEY`
- **Format:** Starts with `sk_live_` (production) or `sk_test_` (test)
- **Description:** Stripe API secret key
- **How to Obtain:**
  1. Visit [https://dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys)
  2. Copy Secret Key from dashboard
- **Used By:** Stripe integration service

### STRIPE_WEBHOOK_SECRET
- **Type:** String (Required if using Stripe)
- **Default:** `whsec_REPLACE_WITH_YOUR_WEBHOOK_SECRET`
- **Format:** Starts with `whsec_`
- **Description:** Stripe webhook endpoint secret for signature verification
- **How to Obtain:**
  1. Go to Stripe Dashboard → Developers → Webhooks
  2. Add endpoint: `https://yourdomain.com/api/stripe/webhook`
  3. Copy Signing Secret
- **Used By:** Stripe webhook handler

### USAGE_TRACKING_ENABLED
- **Type:** Boolean
- **Default:** `true`
- **Description:** Enable usage tracking for billing
- **Used By:** Usage tracker service

### TRIAL_PERIOD_DAYS
- **Type:** Integer
- **Default:** `14`
- **Range:** 1-90
- **Description:** Number of days for trial period
- **Used By:** Trial registration service

### DEFAULT_PLAN
- **Type:** String
- **Default:** `starter`
- **Options:** `starter`, `professional`, `enterprise`
- **Description:** Default subscription plan for new tenants
- **Used By:** Tenant provisioning

---

## Environment Variable Validation

The application includes automatic validation that runs at startup via `env_validator.py`:

### Validation Rules

1. **Required Variables**: Must be set and not empty
2. **No Placeholders**: Cannot contain:
   - `YOUR_`, `REPLACE`, `TODO`, `CHANGEME`, `EXAMPLE`
3. **Password Strength**: Minimum 16 characters for passwords
4. **No Weak Passwords**: Cannot be:
   - `admin`, `admin123`, `password`, `PASSWORD`, `root`
5. **Format Validation**: API keys must match expected formats

### Testing Validation

```bash
# Run validation manually
cd agent-setup
python3 env_validator.py

# Expected output (success):
✅ All environment variables validated successfully

# Expected output (failure):
❌ CRITICAL: CLAUDE_API_KEY contains placeholder value
❌ CRITICAL: ERPNEXT_ADMIN_PASSWORD contains weak/default password
⚠️  WARNING: STRIPE_SECRET_KEY contains placeholder value
```

---

## Quick Setup Template

Create a `.env.production` file with these values:

```bash
# Critical AI Configuration
CLAUDE_API_KEY=sk-ant-api03-xxxxx
CLAUDE_MODEL=claude-sonnet-4-20250514

# ERPNext Configuration
ERPNEXT_BASE_URL=http://erpnext:8000
ERPNEXT_API_KEY=<generate-after-setup>
ERPNEXT_API_SECRET=<generate-after-setup>
ERPNEXT_ADMIN_PASSWORD=<strong-password-here>
ERPNEXT_TIMEOUT=30

# Database Passwords
MYSQL_ROOT_PASSWORD=<strong-password-here>
MYSQL_PASSWORD=<strong-password-here>

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=notifications@yourdomain.com
SMTP_PASSWORD=<app-specific-password>
SMTP_USE_TLS=true

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=<strong-password-here>

# Monitoring
GRAFANA_ADMIN_PASSWORD=<strong-password-here>

# Domain & SSL
DOMAIN_NAME=yourdomain.com
APP_SELF_URL=https://yourdomain.com
SSL_CERTIFICATE_PATH=/etc/nginx/ssl/fullchain.pem
SSL_PRIVATE_KEY_PATH=/etc/nginx/ssl/privkey.pem

# Feature Flags
ENABLE_AUTONOMOUS_WORKFLOWS=true
ENABLE_SELF_HEALING=true
ENABLE_EMAIL_PROCESSING=true
ENABLE_EMPLOYEE_AGENTS=true
ENABLE_MULTI_TENANT=true
ENABLE_KSA_LOCALIZATION=true
ENABLE_MONITORING=true

# Logging
LOG_LEVEL=INFO
LOG_AGENT_ACTIONS=true
```

---

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use strong, unique passwords** for each variable (16+ characters)
3. **Rotate credentials regularly** (every 90 days)
4. **Store secrets securely** using secret management tools
5. **Use environment-specific files** (`.env.development`, `.env.production`)
6. **Validate configuration** before deployment
7. **Monitor access** to environment variables
8. **Backup configuration** securely

---

## Troubleshooting

### Application Won't Start

```bash
# Check validation errors
python3 agent-setup/env_validator.py

# Common issues:
# - Placeholder values not replaced
# - Weak passwords
# - Missing required variables
# - Invalid format (URLs, email addresses)
```

### Services Can't Connect

```bash
# Verify connectivity
docker exec dogansystem-web curl -v http://api-gateway:8006/health
docker exec dogansystem-api-gateway redis-cli -h redis -p 6379 -a $REDIS_PASSWORD ping

# Check environment variables
docker exec dogansystem-web env | grep -E "ERPNEXT|REDIS|CLAUDE"
```

### Email Not Sending

```bash
# Test SMTP connection
docker exec dogansystem-api-gateway python3 -c "
import smtplib
import os
server = smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
server.starttls()
server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
print('SMTP connection successful')
server.quit()
"
```

---

**Last Updated:** 2026-01-13
**Version:** 1.0.0
