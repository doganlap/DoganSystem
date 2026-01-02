# Deployment Guide - Multi-Tenant SaaS Platform

## Quick Start with Docker

### 1. Build and Start Services

```bash
cd agent-setup
docker-compose up -d
```

This will start:
- API Gateway (port 8006)
- Tenant Management API (port 8002)
- Webhook Receiver (port 8003)
- Monitoring Dashboard (port 8005)
- Tenant Admin API (port 8007)
- Redis (port 6379)

### 2. Initialize Platform

```bash
docker-compose exec api-gateway python setup_platform.py
```

### 3. Run Tests

```bash
docker-compose exec api-gateway python test_tenant_system.py
```

### 4. View Logs

```bash
docker-compose logs -f api-gateway
```

## Production Deployment

### Using Docker Compose

1. **Configure Environment**

Create `.env.production`:
```env
PLATFORM_DB_PATH=/app/data/platform.db
TENANT_DB_DIR=/app/data/tenant_databases
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
REDIS_HOST=redis
REDIS_PORT=6379
```

2. **Start with Production Profile**

```bash
docker-compose --profile production up -d
```

3. **Setup Persistent Volumes**

Ensure `./data` directory exists and has proper permissions:
```bash
mkdir -p data/tenant_databases
chmod 755 data
```

### Using Kubernetes

#### 1. Create Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dogansystem
```

#### 2. Deploy Services

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  namespace: dogansystem
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: api-gateway
        image: dogansystem/api-gateway:latest
        ports:
        - containerPort: 8006
        env:
        - name: PLATFORM_DB_PATH
          value: "/app/data/platform.db"
        - name: REDIS_HOST
          value: "redis"
        volumeMounts:
        - name: data
          mountPath: /app/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: dogansystem-data
---
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
  namespace: dogansystem
spec:
  selector:
    app: api-gateway
  ports:
  - port: 80
    targetPort: 8006
  type: LoadBalancer
```

#### 3. Setup Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: dogansystem-ingress
  namespace: dogansystem
spec:
  rules:
  - host: api.dogansystem.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-gateway
            port:
              number: 80
  - host: "*.dogansystem.com"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-gateway
            port:
              number: 80
```

## Environment Configuration

### Required Variables

```env
# Multi-Tenancy
PLATFORM_DB_PATH=platform.db
TENANT_DB_DIR=tenant_databases
TENANT_ISOLATION_MODE=database

# Billing
BILLING_PROVIDER=stripe
STRIPE_SECRET_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...
USAGE_TRACKING_ENABLED=true

# SaaS Settings
TRIAL_PERIOD_DAYS=14
DEFAULT_PLAN=starter
```

### Optional Variables

```env
# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# PostgreSQL (for production)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Monitoring
PROMETHEUS_PORT=8004

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log
```

## Scaling

### Horizontal Scaling

```bash
# Scale API Gateway
docker-compose up -d --scale api-gateway=3

# Or with Kubernetes
kubectl scale deployment api-gateway --replicas=5 -n dogansystem
```

### Load Balancing

Use Nginx or Traefik for load balancing:

```nginx
upstream api_gateway {
    least_conn;
    server api-gateway-1:8006;
    server api-gateway-2:8006;
    server api-gateway-3:8006;
}

server {
    listen 80;
    server_name *.dogansystem.com;

    location / {
        proxy_pass http://api_gateway;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Tenant-ID $http_x_tenant_id;
    }
}
```

## Database Setup

### SQLite (Development)

No setup required - automatically created.

### PostgreSQL (Production)

```bash
# Create database
createdb dogansystem

# Run migrations (if using Alembic)
alembic upgrade head
```

## Monitoring

### Prometheus

Metrics are exposed on port 8004:

```yaml
scrape_configs:
  - job_name: 'dogansystem'
    static_configs:
      - targets: ['api-gateway:8004']
```

### Health Checks

All services expose health endpoints:
- `GET /` - Health check
- `GET /health` - Detailed health status

## Backup and Recovery

### Backup Script

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/$DATE"

mkdir -p $BACKUP_DIR

# Backup platform database
cp platform.db $BACKUP_DIR/

# Backup tenant databases
cp -r tenant_databases $BACKUP_DIR/

# Backup to S3 (optional)
aws s3 sync $BACKUP_DIR s3://dogansystem-backups/$DATE/
```

### Recovery

```bash
# Restore from backup
cp backups/20250115_120000/platform.db .
cp -r backups/20250115_120000/tenant_databases .
```

## Security

### API Keys

Generate API keys for tenants:
```python
from tenant_security import TenantSecurity
from tenant_manager import TenantManager
from tenant_isolation import TenantIsolation

security = TenantSecurity(manager, tenant_isolation)
keys = security.generate_api_key(tenant_id, "production")
```

### SSL/TLS

Use reverse proxy (Nginx/Traefik) with SSL certificates:

```nginx
server {
    listen 443 ssl;
    server_name *.dogansystem.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://api-gateway:8006;
    }
}
```

## Troubleshooting

### Service Won't Start

1. Check logs: `docker-compose logs service-name`
2. Verify environment variables
3. Check port availability
4. Verify database connectivity

### Database Issues

1. Check file permissions
2. Verify database path
3. Check disk space
4. Review database logs

### Performance Issues

1. Check resource usage: `docker stats`
2. Review metrics in Prometheus
3. Scale services horizontally
4. Optimize database queries

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t dogansystem/api-gateway:${{ github.sha }} .
      
      - name: Push to registry
        run: docker push dogansystem/api-gateway:${{ github.sha }}
      
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/api-gateway \
            api-gateway=dogansystem/api-gateway:${{ github.sha }} \
            -n dogansystem
```

## Support

For deployment issues:
- Check logs in `logs/` directory
- Review Docker logs: `docker-compose logs`
- Verify environment configuration
- Test connectivity between services
