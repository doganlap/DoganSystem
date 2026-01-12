# DoganSystem Docker Production Deployment Guide

## Quick Start

```bash
# 1. Copy environment template
cp .env.production .env

# 2. Edit .env with your API keys
nano .env

# 3. Deploy
./deploy.sh deploy
```

## Files Created for Production

| File | Purpose |
|------|---------|
| `docker-compose.production.yml` | Main Docker orchestration |
| `.env.production` | Environment variables template |
| `deploy.sh` | Deployment automation script |
| `nginx/nginx.conf` | Generic nginx config |
| `nginx/nginx.production.conf` | Domain-specific nginx config |
| `Dockerfile` | C# Web Application |
| `agent-setup/Dockerfile` | Python AI Services |

## Services & Ports

| Service | Port | Description |
|---------|------|-------------|
| `dogansystem-web` | 5000 | C# MVC Web Application |
| `api-gateway` | 8006 | AI Services Entry Point |
| `agent-server` | 8001 | Claude AI Agents |
| `tenant-admin` | 8007 | Tenant Management API |
| `workflow-engine` | - | Autonomous Workflows |
| `monitoring` | 8005 | Monitoring Dashboard |
| `webhook-receiver` | 8003 | Webhook Handler |
| `redis` | 6379 | Message Queue & Cache |
| `nginx` | 80/443 | Reverse Proxy |

## Domain Configuration (saudibusinessgate.com)

| Subdomain | Service |
|-----------|---------|
| `saudibusinessgate.com` | Main Web Application |
| `www.saudibusinessgate.com` | Main Web Application |
| `api.saudibusinessgate.com` | API Gateway |
| `ai.saudibusinessgate.com` | Claude AI Agents |
| `ds.saudibusinessgate.com` | Admin Dashboard |

## Required Environment Variables

### CRITICAL (Must Configure)

```env
# Claude AI (Get from https://console.anthropic.com/)
CLAUDE_API_KEY=sk-ant-api03-YOUR_KEY_HERE

# ERPNext (Get from ERPNext Settings > API Access)
ERPNEXT_BASE_URL=http://your-erpnext:8000
ERPNEXT_API_KEY=your_key
ERPNEXT_API_SECRET=your_secret
```

### Optional (Email Notifications)

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=app-specific-password
```

## Deployment Commands

```bash
# Full deployment
./deploy.sh deploy

# Start services
./deploy.sh start

# Stop services
./deploy.sh stop

# Restart services
./deploy.sh restart

# View logs
./deploy.sh logs                    # All logs
./deploy.sh logs api-gateway        # Specific service

# Check status
./deploy.sh status

# Rebuild and redeploy
./deploy.sh rebuild
```

## Docker Hub Integration

### Build and Push Images

```bash
# Build and push to Docker Hub (requires login)
./scripts/build-and-push-docker.sh v1.0.0

# Build only (skip push)
./scripts/build-and-push-docker.sh v1.0.0 false

# Use default 'latest' tag
./scripts/build-and-push-docker.sh
```

### Using Pre-built Images

Update `docker-compose.production.yml` to use Docker Hub images:

```yaml
services:
  dogansystem-web:
    image: doganlap/dogansystem-web:latest
    # Remove build section when using pre-built images

  api-gateway:
    image: doganlap/dogansystem-ai:latest
    # Remove build section when using pre-built images
```

See `DOCKER_HUB_SETUP.md` for detailed Docker Hub configuration.

## SSL Certificates

### Development (Self-signed)
The deploy script automatically generates self-signed certificates.

### Production (Let's Encrypt)
```bash
# Install certbot
apt install certbot

# Generate certificates
certbot certonly --standalone -d saudibusinessgate.com -d www.saudibusinessgate.com -d api.saudibusinessgate.com -d ai.saudibusinessgate.com -d ds.saudibusinessgate.com

# Copy to nginx/ssl/
cp /etc/letsencrypt/live/saudibusinessgate.com/fullchain.pem nginx/ssl/
cp /etc/letsencrypt/live/saudibusinessgate.com/privkey.pem nginx/ssl/
```

## AI Features Status

| Feature | Default | Environment Variable |
|---------|---------|---------------------|
| Claude AI Agents | Enabled | `CLAUDE_API_KEY` required |
| Autonomous Workflows | Enabled | `ENABLE_AUTONOMOUS_WORKFLOWS=true` |
| Self-Healing System | Enabled | `ENABLE_SELF_HEALING=true` |
| Email Processing | Enabled | `ENABLE_EMAIL_PROCESSING=true` |
| Multi-Tenant | Enabled | `ENABLE_MULTI_TENANT=true` |
| KSA Localization | Enabled | `ENABLE_KSA_LOCALIZATION=true` |
| Monitoring | Enabled | `ENABLE_MONITORING=true` |

## Health Check Endpoints

```bash
# Web Application
curl http://localhost:5000/health

# API Gateway
curl http://localhost:8006/health

# Agent Server
curl http://localhost:8001/health

# All services via nginx
curl https://saudibusinessgate.com/health
curl https://api.saudibusinessgate.com/health
curl https://ai.saudibusinessgate.com/health
```

## Troubleshooting

### Container not starting
```bash
# Check logs
docker logs dogansystem-api-gateway

# Check health
docker inspect --format='{{.State.Health.Status}}' dogansystem-api-gateway
```

### Claude API errors
- Verify `CLAUDE_API_KEY` is set correctly
- Check API key hasn't expired
- Ensure no extra spaces in .env file

### ERPNext connection failed
- Verify ERPNext is accessible from Docker network
- Check API key/secret are correct
- Ensure API user has required permissions

### Services can't communicate
```bash
# Check network
docker network inspect dogansystem-network

# Test connectivity
docker exec dogansystem-web curl http://api-gateway:8006/health
```

## Production Checklist

- [ ] Claude API Key configured
- [ ] ERPNext API Keys configured
- [ ] SSL certificates installed (Let's Encrypt)
- [ ] DNS records pointing to server (91.98.34.142)
- [ ] SMTP configured for notifications
- [ ] Firewall allows ports 80, 443
- [ ] Backup strategy configured
- [ ] Monitoring alerts set up
