# Port Allocation Plan - GrcMvc vs DoganSystem

## 🔴 RESERVED PORTS (GrcMvc - DO NOT USE)

### Active Ports (Currently Running):
| Port | Service | Application | Status |
|------|---------|-------------|--------|
| **5100** | GrcMvc Web App | GrcMvc | ✅ Running |
| **5432** | PostgreSQL DB | GrcMvc | ✅ Running (Docker: grc-db) |
| **6379** | Redis Cache | GrcMvc | ✅ Running (Docker: grc-redis) |

### Reserved Ports (Optional GrcMvc Services):
| Port | Service | Application | Reserved For |
|------|---------|-------------|--------------|
| **9092** | Kafka | GrcMvc | Future use |
| **2181** | Zookeeper | GrcMvc | Future use |
| **8123** | ClickHouse | GrcMvc | Future use |
| **3000** | Grafana | GrcMvc | Future use |
| **8080** | Kafka UI | GrcMvc | Future use |
| **3001** | Metabase | GrcMvc | Future use |
| **5678** | n8n Workflow | GrcMvc | Future use |
| **8088** | Superset | GrcMvc | Future use |
| **8081** | Camunda BPM | GrcMvc | Future use |

---

## 🟢 DOGANSYSTEM PORTS (No Conflicts!)

### External Access (via Cloudflare Tunnel):
| Port | Service | Notes |
|------|---------|-------|
| **N/A** | Cloudflare Tunnel | **No ports opened!** All traffic via Cloudflare |
| - | All external domains → Cloudflare → nginx:80 (internal) | Secure tunnel |

**External URLs** (all via Cloudflare, no port exposure):
- https://doganconsult.com
- https://www.doganconsult.com
- https://api.doganconsult.com
- https://ai.doganconsult.com
- https://ds.doganconsult.com
- https://login.doganconsult.com

### Internal Docker Services (localhost only):
| Port | Service | Container Name | Status |
|------|---------|----------------|--------|
| **80** | Nginx Reverse Proxy | dogansystem-nginx | Inside Docker |
| **5000** | .NET Backend API | dogansystem-web | Inside Docker |
| **5433** | PostgreSQL (DoganSystem) | dogansystem-postgres | Inside Docker ⚠️ Changed from 5432! |
| **6380** | Redis (DoganSystem) | dogansystem-redis | Inside Docker ⚠️ Changed from 6379! |
| **8000** | ERPNext | dogansystem-erpnext | Inside Docker |
| **8001** | AI Agent Server | dogansystem-agent-server | Inside Docker |
| **8003** | Webhook Receiver | dogansystem-webhook | Inside Docker |
| **8005** | Monitoring Dashboard | dogansystem-monitoring | Inside Docker |
| **8006** | API Gateway (Python) | dogansystem-api-gateway | Inside Docker |
| **8007** | Tenant Admin API | dogansystem-tenant-admin | Inside Docker |
| **3306** | MariaDB (ERPNext) | dogansystem-erpnext-db | Inside Docker |

---

## ✅ CONFLICT RESOLUTION

### Changes Made to DoganSystem:
1. **PostgreSQL**: Changed from port **5432** → **5433** (avoids GrcMvc PostgreSQL)
2. **Redis**: Changed from port **6379** → **6380** (avoids GrcMvc Redis)
3. **External Access**: Using **Cloudflare Tunnel** (no port 80/443 exposure needed)

### Why No Port 80/443 Conflicts?
- **Cloudflare Tunnel** runs entirely through an **outbound connection**
- No inbound ports opened on your machine
- All traffic: Internet → Cloudflare Edge → Tunnel → Docker nginx:80 (internal only)
- Your GrcMvc on port 5100 is completely isolated

---

## 📊 COMPLETE PORT SUMMARY

### Ports 0-1000:
- **80**: DoganSystem nginx (Docker internal only, not exposed)

### Ports 1000-5000:
- **3000**: RESERVED for GrcMvc Grafana
- **3001**: RESERVED for GrcMvc Metabase
- **3306**: DoganSystem MariaDB (Docker internal)

### Ports 5000-6000:
- **5000**: DoganSystem .NET API (Docker internal)
- **5100**: 🔴 **GrcMvc Web App** (ACTIVE - DO NOT USE)
- **5432**: 🔴 **GrcMvc PostgreSQL** (ACTIVE - DO NOT USE)
- **5433**: DoganSystem PostgreSQL (Docker internal)
- **5678**: RESERVED for GrcMvc n8n

### Ports 6000-7000:
- **6379**: 🔴 **GrcMvc Redis** (ACTIVE - DO NOT USE)
- **6380**: DoganSystem Redis (Docker internal)

### Ports 8000-9000:
- **8000**: DoganSystem ERPNext (Docker internal)
- **8001**: DoganSystem AI Agent Server (Docker internal)
- **8003**: DoganSystem Webhook Receiver (Docker internal)
- **8005**: DoganSystem Monitoring (Docker internal)
- **8006**: DoganSystem API Gateway (Docker internal)
- **8007**: DoganSystem Tenant Admin (Docker internal)
- **8080**: RESERVED for GrcMvc Kafka UI
- **8081**: RESERVED for GrcMvc Camunda
- **8088**: RESERVED for GrcMvc Superset
- **8123**: RESERVED for GrcMvc ClickHouse

### Ports 9000+:
- **9092**: RESERVED for GrcMvc Kafka

---

## 🛡️ SECURITY NOTES

### GrcMvc (Port 5100):
- Exposed on localhost:5100
- Directly accessible from browser
- Uses its own PostgreSQL (5432) and Redis (6379)

### DoganSystem:
- **NO direct port exposure** to internet
- All traffic through Cloudflare Tunnel (encrypted)
- Internal services on Docker network only
- PostgreSQL (5433) and Redis (6380) avoid conflicts
- Access via: https://doganconsult.com (no port numbers!)

---

## 🚀 DEPLOYMENT COORDINATION

### For Team Communication:

**Before Deployment:**
```
Team: We're deploying DoganSystem alongside GrcMvc.

Port Usage:
- GrcMvc keeps: 5100, 5432, 6379 (no changes)
- DoganSystem uses: 5433, 6380, 8000-8007 (different ports)
- External access: https://doganconsult.com (via Cloudflare Tunnel)

No conflicts! Both systems run independently.
```

### Testing Both Systems:
```bash
# Test GrcMvc
curl http://localhost:5100

# Test DoganSystem (after deployment)
curl http://localhost:5000        # Backend API
curl http://localhost:8000        # ERPNext
curl https://doganconsult.com     # Public access via Cloudflare
```

---

## 📋 QUICK REFERENCE

### When GrcMvc is Running:
✅ Safe to start DoganSystem - no port conflicts

### When DoganSystem is Running:
✅ Safe to start GrcMvc - no port conflicts

### Both Running Simultaneously:
✅ Fully compatible - different ports for everything

---

## 🔧 DOCKER COMPOSE CHANGES

I will update `docker-compose.production.yml` to use these ports:
- PostgreSQL: **5433** (changed from 5432)
- Redis: **6380** (changed from 6379)
- All other ports remain as designed (8000-8007)

---

**Last Updated:** 2026-01-13
**Approved By:** Team Coordination
**Status:** Ready for deployment - No conflicts with GrcMvc
