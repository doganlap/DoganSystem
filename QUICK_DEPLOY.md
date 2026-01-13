# 🚀 DoganSystem - Quick Deployment Guide

The fastest way to get DoganSystem running on your local PC/laptop using Docker or VMs.

---

## ⚡ Super Quick Start (5 Minutes)

### Prerequisites
- Docker Desktop installed (Windows/Mac) or Docker Engine (Linux)
- 8GB RAM, 20GB disk space

### One Command Deploy

**Linux/Mac:**
```bash
docker-compose up -d
```

**Windows (PowerShell):**
```powershell
docker-compose up -d
```

**Access:**
- Frontend: http://localhost
- Backend API: http://localhost:5000

That's it! 🎉

---

## 🐳 Docker Deployment (Recommended)

### What You Get

```
┌──────────────────────────────────────┐
│      Frontend (React + Vite)         │
│      ✓ Bilingual (AR/EN)            │
│      ✓ Modern Dashboard              │
│      ✓ All UI Features               │
│      http://localhost                │
└───────────────┬──────────────────────┘
                │ Nginx Reverse Proxy
┌───────────────▼──────────────────────┐
│      Backend (.NET 8 API)            │
│      ✓ Multi-tenant Support         │
│      ✓ ABP Framework                 │
│      ✓ ERPNext Integration           │
│      http://localhost:5000           │
└──────────────────────────────────────┘
```

### Step-by-Step

#### 1. Install Docker

**Windows:**
- Download: https://www.docker.com/products/docker-desktop
- Install and restart
- Docker icon appears in system tray

**Mac:**
- Download: https://www.docker.com/products/docker-desktop
- Drag to Applications folder
- Launch Docker

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and log back in
```

#### 2. Clone Repository

```bash
git clone https://github.com/doganlap/DoganSystem.git
cd DoganSystem
```

#### 3. Deploy

```bash
docker-compose up -d
```

#### 4. Verify

```bash
# Check services are running
docker-compose ps

# View logs
docker-compose logs -f

# Check health
curl http://localhost/health
curl http://localhost:5000/health
```

### Management Commands

```bash
# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f frontend
docker-compose logs -f dogansystem

# Rebuild and redeploy
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 🖥️ VM Deployment (No Cloud Costs)

Deploy in a local VM for isolated testing.

### Quick VM Setup

#### 1. Install VirtualBox (Free)

Download: https://www.virtualbox.org/

#### 2. Create Ubuntu VM

```
Name: DoganSystem
Type: Linux
Version: Ubuntu (64-bit)
Memory: 8192 MB (8GB)
Disk: 60GB VDI
Network: Bridged Adapter
```

#### 3. Install Ubuntu Server 22.04

Download ISO: https://ubuntu.com/download/server

#### 4. Setup in VM

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Log out and back in

# Clone and deploy
git clone https://github.com/doganlap/DoganSystem.git
cd DoganSystem
docker-compose up -d
```

#### 5. Access from Host

```bash
# Find VM IP
ip addr show

# Access from host browser
http://<VM_IP>
http://<VM_IP>:5000
```

### VM Tools Comparison

| Tool | Cost | Best For |
|------|------|----------|
| **VirtualBox** | Free | Beginners |
| **VMware Player** | Free | Better performance |
| **Hyper-V** | Free (Windows Pro) | Windows integration |
| **KVM** | Free | Linux native |
| **Proxmox** | Free | Enterprise features |

For detailed VM setup, see: [VM_LOCAL_DEVELOPMENT_GUIDE.md](VM_LOCAL_DEVELOPMENT_GUIDE.md)

---

## 📊 What's Included

### Frontend (React)
- ✅ Modern React 18 + Vite
- ✅ Tailwind CSS styling
- ✅ Bilingual support (Arabic RTL/English LTR)
- ✅ Dashboard with charts
- ✅ Tenant management UI
- ✅ Agent management UI
- ✅ ERPNext integration UI
- ✅ Subscription/billing UI
- ✅ System monitoring UI

### Backend (.NET 8)
- ✅ ABP Framework
- ✅ Multi-tenant architecture
- ✅ RESTful API
- ✅ ERPNext integration
- ✅ Agent orchestration
- ✅ Policy management
- ✅ Subscription handling

### Infrastructure
- ✅ Docker containerized
- ✅ Nginx reverse proxy
- ✅ Health checks
- ✅ Auto-restart on failure
- ✅ Volume persistence
- ✅ Network isolation

---

## 🔧 Configuration

### Environment Variables

**Frontend** (`frontend/.env.production`):
```env
VITE_API_URL=/api
VITE_APP_NAME=DoganSystem
VITE_DEFAULT_LANGUAGE=ar
```

**Backend** (in `docker-compose.yml`):
```yaml
environment:
  - ASPNETCORE_ENVIRONMENT=Production
  - ASPNETCORE_URLS=http://+:5000
  - ConnectionStrings__Default=Data Source=/app/data/DoganSystem.db
```

### Ports

| Service | Port | URL |
|---------|------|-----|
| Frontend | 80 | http://localhost |
| Frontend HTTPS | 443 | https://localhost (if SSL configured) |
| Backend API | 5000 | http://localhost:5000 |

### Data Persistence

Data is stored in Docker volumes:
- `./data` - Database files
- `./logs` - Application logs
- `./etc/policies` - Policy configurations

**Backup:**
```bash
# Backup data
tar -czf backup-$(date +%Y%m%d).tar.gz data/ logs/ etc/

# Restore
tar -xzf backup-20260113.tar.gz
```

---

## 🐛 Troubleshooting

### Port Already in Use

**Problem:** `Error: port 80 is already in use`

**Solution:**
```bash
# Option 1: Stop the conflicting service
# On Windows: Stop IIS or other web server
# On Linux: sudo systemctl stop apache2

# Option 2: Change port in docker-compose.yml
# ports:
#   - "8080:80"  # Use port 8080 instead
# Access: http://localhost:8080
```

### Docker Not Running

**Problem:** `Cannot connect to Docker daemon`

**Solution:**
- Windows/Mac: Start Docker Desktop
- Linux: `sudo systemctl start docker`

### Cannot Access Frontend

**Problem:** Frontend loads but shows errors

**Solution:**
```bash
# Check backend is running
curl http://localhost:5000/health

# Check logs
docker-compose logs -f dogansystem

# Restart services
docker-compose restart
```

### Database Errors

**Problem:** Backend won't start, database errors

**Solution:**
```bash
# Reset database (CAUTION: Deletes all data)
docker-compose down
rm -rf data/*
docker-compose up -d
```

### Out of Memory

**Problem:** Services crash or slow

**Solution:**
- Docker Desktop: Settings → Resources → Increase memory to 8GB+
- VM: Increase RAM allocation to 8GB+

---

## 📈 Next Steps

### After Deployment

1. **Configure CORS** (if needed for external access)
2. **Set up SSL** for HTTPS (production)
3. **Configure backups** (automated)
4. **Set up monitoring** (logs, health checks)
5. **Configure domain** (DNS, reverse proxy)

### For Production

See: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:
- SSL/HTTPS setup
- Domain configuration
- Production optimizations
- Security hardening
- Monitoring setup

### For Development

See: [VM_LOCAL_DEVELOPMENT_GUIDE.md](VM_LOCAL_DEVELOPMENT_GUIDE.md) for:
- Multi-VM setups
- Network configurations
- Development workflows
- Testing scenarios

---

## 📚 Documentation

- **Deployment Guide**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **VM Setup Guide**: [VM_LOCAL_DEVELOPMENT_GUIDE.md](VM_LOCAL_DEVELOPMENT_GUIDE.md)
- **Frontend Integration**: [FRONTEND_INTEGRATION_REPORT.md](FRONTEND_INTEGRATION_REPORT.md)
- **Architecture**: [frontend/ARCHITECTURE.md](frontend/ARCHITECTURE.md)
- **Code Quality**: [frontend/CODE_QUALITY.md](frontend/CODE_QUALITY.md)

---

## ✅ Deployment Checklist

- [ ] Docker installed and running
- [ ] Repository cloned
- [ ] Ports 80 and 5000 available
- [ ] Run: `docker-compose up -d`
- [ ] Services healthy: `docker-compose ps`
- [ ] Frontend accessible: http://localhost
- [ ] Backend accessible: http://localhost:5000
- [ ] Logs show no errors: `docker-compose logs`

---

**You're ready to deploy!** 🚀

Choose Docker for the quickest setup, or VM for isolated testing.

Both methods give you a fully functional DoganSystem with frontend and backend in minutes!
