# Security Setup Guide - DoganSystem

This guide provides step-by-step instructions for securely deploying DoganSystem to production.

## ⚠️ CRITICAL: Pre-Deployment Security Checklist

**DO NOT DEPLOY** until all items in this checklist are completed:

- [ ] All passwords in `.env.production` replaced with strong values (16+ characters)
- [ ] All API keys updated with real production values
- [ ] SSL/TLS certificates installed and configured
- [ ] Firewall rules configured
- [ ] Redis password configured
- [ ] Database passwords rotated from defaults
- [ ] Environment variable validation passing
- [ ] All placeholder values removed

---

## 1. Generate Strong Passwords

All passwords must be at least **16 characters** and contain:
- Uppercase letters (A-Z)
- Lowercase letters (a-z)
- Numbers (0-9)
- Special characters (!@#$%^&*)

### Generate Secure Passwords

```bash
# Option 1: Using OpenSSL (Recommended)
openssl rand -base64 32

# Option 2: Using Python
python3 -c "import secrets; print(secrets.token_urlsafe(24))"

# Option 3: Using pwgen (if installed)
pwgen -s 24 1
```

Generate unique passwords for each of the following:

```bash
ERPNEXT_ADMIN_PASSWORD=<generate-here>
MYSQL_ROOT_PASSWORD=<generate-here>
MYSQL_PASSWORD=<generate-here>
REDIS_PASSWORD=<generate-here>
GRAFANA_ADMIN_PASSWORD=<generate-here>
```

---

## 2. Configure API Keys

### 2.1 Claude AI API Key

1. Visit [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign in or create an account
3. Navigate to **API Keys**
4. Create a new API key
5. Copy the key and update `.env.production`:

```bash
CLAUDE_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

### 2.2 ERPNext API Keys

ERPNext API keys are generated after first login:

1. Deploy ERPNext and access the web interface
2. Login with admin credentials
3. Go to: **User Menu** → **API Access** → **Generate Keys**
4. Copy both the API Key and API Secret
5. Update `.env.production`:

```bash
ERPNEXT_API_KEY=<api-key-here>
ERPNEXT_API_SECRET=<api-secret-here>
```

### 2.3 Stripe API Keys (Optional - for SaaS billing)

If using Stripe for billing:

1. Visit [https://dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys)
2. Use **Test Mode** for development, **Live Mode** for production
3. Copy your **Secret Key** (starts with `sk_live_` or `sk_test_`)
4. Set up webhook endpoint and get the webhook secret
5. Update `.env.production`:

```bash
STRIPE_SECRET_KEY=sk_live_xxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

---

## 3. SSL/TLS Certificate Setup

### Option A: Let's Encrypt (Free - Recommended)

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot

# Generate certificate
sudo certbot certonly --standalone -d doganconsult.com -d www.doganconsult.com

# Certificates will be generated at:
# /etc/letsencrypt/live/doganconsult.com/fullchain.pem
# /etc/letsencrypt/live/doganconsult.com/privkey.pem

# Copy to project directory
sudo cp /etc/letsencrypt/live/doganconsult.com/fullchain.pem ./nginx/ssl/
sudo cp /etc/letsencrypt/live/doganconsult.com/privkey.pem ./nginx/ssl/
sudo chmod 644 ./nginx/ssl/fullchain.pem
sudo chmod 600 ./nginx/ssl/privkey.pem
```

### Option B: Custom Certificate

If you have a purchased SSL certificate:

1. Copy certificate files to `./nginx/ssl/`:
   - `fullchain.pem` (certificate + intermediate certificates)
   - `privkey.pem` (private key)

2. Update `.env.production`:

```bash
SSL_CERTIFICATE_PATH=/etc/nginx/ssl/fullchain.pem
SSL_PRIVATE_KEY_PATH=/etc/nginx/ssl/privkey.pem
DOMAIN_NAME=doganconsult.com
```

### Certificate Renewal (Let's Encrypt)

Set up automatic renewal:

```bash
# Test renewal
sudo certbot renew --dry-run

# Add cron job for automatic renewal
sudo crontab -e

# Add this line (runs twice daily):
0 0,12 * * * certbot renew --quiet --post-hook "docker-compose -f /path/to/DoganSystem/docker-compose.production.yml restart nginx"
```

---

## 4. Environment Configuration

### 4.1 Update .env.production

Edit `.env.production` and replace ALL placeholder values:

```bash
# Copy template
cp .env.production .env.production.local

# Edit with your values
nano .env.production
```

**Critical Variables:**
```bash
CLAUDE_API_KEY=<your-anthropic-api-key>
ERPNEXT_ADMIN_PASSWORD=<strong-password-16chars>
MYSQL_ROOT_PASSWORD=<strong-password-16chars>
MYSQL_PASSWORD=<strong-password-16chars>
REDIS_PASSWORD=<strong-password-16chars>
GRAFANA_ADMIN_PASSWORD=<strong-password-16chars>
ERPNEXT_API_KEY=<generated-after-erpnext-setup>
ERPNEXT_API_SECRET=<generated-after-erpnext-setup>
DOMAIN_NAME=doganconsult.com
APP_SELF_URL=https://doganconsult.com
```

### 4.2 Validate Configuration

The application includes automatic validation that runs at startup:

```bash
# Test validation
cd agent-setup
python3 env_validator.py
```

**Expected output if successful:**
```
✅ All environment variables validated successfully
```

**If validation fails, you'll see:**
```
❌ CRITICAL: CLAUDE_API_KEY contains placeholder value
❌ CRITICAL: ERPNEXT_ADMIN_PASSWORD contains weak/default password
⚠️  WARNING: STRIPE_SECRET_KEY contains placeholder value
```

Fix all errors before proceeding.

---

## 5. Database Security

### 5.1 ERPNext/MySQL Security

After first deployment:

```bash
# Connect to ERPNext database container
docker exec -it dogansystem-erpnext-db mysql -u root -p

# Run these commands:
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
FLUSH PRIVILEGES;
```

### 5.2 Backup Configuration

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups/$DATE"
mkdir -p $BACKUP_DIR

# Backup databases
docker exec dogansystem-erpnext-db mysqldump -u root -p$MYSQL_ROOT_PASSWORD --all-databases > $BACKUP_DIR/mysql_backup.sql
docker cp dogansystem-web:/app/data/DoganSystem.db $BACKUP_DIR/
docker cp dogansystem-api-gateway:/app/data/ $BACKUP_DIR/tenant_data/

# Compress
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "Backup completed: $BACKUP_DIR.tar.gz"
EOF

chmod +x backup.sh

# Add to crontab (daily at 2 AM)
0 2 * * * /path/to/DoganSystem/backup.sh
```

---

## 6. Firewall Configuration

### 6.1 UFW (Ubuntu/Debian)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Block direct access to backend services
sudo ufw deny 5000/tcp
sudo ufw deny 8000/tcp
sudo ufw deny 8001/tcp
sudo ufw deny 8002/tcp
sudo ufw deny 8003/tcp
sudo ufw deny 8004/tcp
sudo ufw deny 8005/tcp
sudo ufw deny 8006/tcp
sudo ufw deny 6379/tcp
sudo ufw deny 3306/tcp

# Check status
sudo ufw status verbose
```

### 6.2 Cloud Provider Firewall

If using AWS, Azure, or GCP, also configure security groups:

**Inbound Rules:**
- Port 22 (SSH) - Your IP only
- Port 80 (HTTP) - 0.0.0.0/0
- Port 443 (HTTPS) - 0.0.0.0/0

**Outbound Rules:**
- All traffic allowed (for API calls, updates, etc.)

---

## 7. Docker Security

### 7.1 Non-Root User

Ensure Docker containers run as non-root:

```bash
# Check Dockerfile includes:
USER nonroot

# Verify
docker exec dogansystem-web whoami
```

### 7.2 Docker Socket Security

```bash
# Restrict Docker socket permissions
sudo chmod 660 /var/run/docker.sock
sudo chown root:docker /var/run/docker.sock
```

### 7.3 Resource Limits

Add to `docker-compose.production.yml`:

```yaml
services:
  dogansystem-web:
    # ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## 8. Application Security Headers

Verify nginx configuration includes security headers:

```nginx
# Already configured in nginx/nginx.conf
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

---

## 9. Monitoring & Logging

### 9.1 Access Grafana

After deployment, access monitoring:

```
URL: https://doganconsult.com:3000
Username: admin
Password: <GRAFANA_ADMIN_PASSWORD from .env.production>
```

**First login:** Change the password immediately.

### 9.2 Log Aggregation

```bash
# View logs
docker-compose -f docker-compose.production.yml logs -f

# View specific service
docker logs -f dogansystem-web

# Save logs to file
docker-compose -f docker-compose.production.yml logs > system.log
```

### 9.3 Set Up Alerts

Configure alerts in Grafana for:
- High CPU usage (> 80%)
- High memory usage (> 90%)
- Failed login attempts (> 10/hour)
- API errors (> 5% error rate)
- Database connection failures

---

## 10. Deployment Steps

### 10.1 Pre-Deployment Validation

```bash
# 1. Validate environment variables
cd agent-setup && python3 env_validator.py

# 2. Check Docker configuration
docker-compose -f docker-compose.production.yml config

# 3. Test SSL certificates
openssl x509 -in nginx/ssl/fullchain.pem -text -noout
```

### 10.2 Deploy

```bash
# Build and start services
docker-compose -f docker-compose.production.yml up -d --build

# Check health
docker-compose -f docker-compose.production.yml ps

# View logs
docker-compose -f docker-compose.production.yml logs -f
```

### 10.3 Post-Deployment Verification

```bash
# Test HTTPS
curl -I https://doganconsult.com

# Test API endpoint
curl -X GET https://api.doganconsult.com/health

# Check all services are running
docker ps --filter "name=dogansystem"
```

---

## 11. Security Maintenance

### Monthly Tasks

- [ ] Review access logs for suspicious activity
- [ ] Update all Docker images to latest versions
- [ ] Rotate API keys and passwords
- [ ] Review and update firewall rules
- [ ] Test backup restoration procedure
- [ ] Review Grafana alerts and metrics
- [ ] Check SSL certificate expiration (Let's Encrypt: 90 days)

### Security Updates

```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Update Docker images
docker-compose -f docker-compose.production.yml pull
docker-compose -f docker-compose.production.yml up -d

# Restart services
docker-compose -f docker-compose.production.yml restart
```

---

## 12. Incident Response

### Security Incident Checklist

1. **Isolate**: Disconnect affected services from network
2. **Assess**: Review logs to understand the breach
3. **Contain**: Stop the attack vector
4. **Eradicate**: Remove malicious code/access
5. **Recover**: Restore from clean backups
6. **Review**: Update security measures to prevent recurrence

### Emergency Contacts

- **System Administrator**: [email]
- **Security Team**: [email]
- **Anthropic Support**: [https://support.anthropic.com](https://support.anthropic.com)

---

## 13. Compliance (KSA Requirements)

For Saudi Arabia deployments, ensure:

- [ ] Data stored within KSA borders (use local cloud regions)
- [ ] All user data encrypted at rest and in transit
- [ ] Audit logging enabled for all data access
- [ ] Privacy policy compliant with PDPL
- [ ] User consent mechanisms implemented
- [ ] Data retention policies configured
- [ ] Right to deletion procedures implemented

### Audit Log Review

```bash
# View audit logs
docker exec dogansystem-api-gateway cat /app/logs/audit.log | grep "tenant_id"

# Export audit logs
docker cp dogansystem-api-gateway:/app/logs/audit.log ./audit_$(date +%Y%m%d).log
```

---

## Support

For security issues or questions:
- Email: security@doganconsult.com
- GitHub Issues: https://github.com/doganlap/DoganSystem/issues
- Documentation: https://doganconsult.com/docs

---

**Last Updated:** 2026-01-13
**Version:** 1.0.0
