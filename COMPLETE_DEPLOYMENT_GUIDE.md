# DoganSystem Complete Deployment Guide

## 🎯 Current Status: Ready to Create VM

You have successfully:
- ✅ Enabled Hyper-V
- ✅ Restarted your computer
- ✅ All deployment scripts are prepared

---

## 📋 Complete Step-by-Step Process

### PHASE 1: Create VM (10 minutes) - DO THIS NOW

1. **Open Hyper-V Manager:**
   ```
   Win + R → type: virtmgmt.msc → Enter
   ```

2. **Create New VM:**
   - Right-click computer name → New → Virtual Machine
   - **Name:** DoganSystem-Production
   - **Generation:** 2
   - **Memory:** 24576 MB (check "Use Dynamic Memory")
   - **Network:** Default Switch
   - **Disk:** Create new, 150 GB
   - **ISO:** Browse to Windows Server 2022 ISO file
     - Download from: https://www.microsoft.com/evalcenter if needed

3. **Configure CPU:**
   - Right-click VM → Settings → Processor
   - Set to **10** virtual processors

4. **Start VM:**
   - Right-click VM → Connect
   - Click Start button

---

### PHASE 2: Install Windows (20 minutes)

1. Boot from ISO
2. Select: **Windows Server 2022 Standard Evaluation (Desktop Experience)**
3. Accept license
4. Custom installation
5. Install to the 150GB disk
6. Set Admin password: `DoganAdmin2024!` (remember this!)
7. Login

---

### PHASE 3: Copy Files to VM (5 minutes)

**In the VM**, open PowerShell as Administrator:

```powershell
# Create directory
New-Item -Path "C:\DoganSystem" -ItemType Directory -Force

# If enhanced session is enabled, copy directly:
Copy-Item -Path "\\tsclient\d\DoganSystem\*" -Destination "C:\DoganSystem\" -Recurse -Force
```

**If that doesn't work:**
1. On host, share `D:\DoganSystem`
2. In VM, map network drive
3. Copy files manually

---

### PHASE 4-8: Run Deployment Scripts (90 minutes)

**Run each script in PowerShell as Administrator:**

```powershell
cd C:\DoganSystem

# 1. Install Software (45 minutes)
# Installs: IIS, .NET 8, SQL Server, Python, Node.js, Git, Cloudflared
.\3-install-software.ps1

# 2. Deploy Backend (10 minutes)
# Builds and deploys ASP.NET Core application
.\4-deploy-backend.ps1

# 3. Deploy Python AI Services (15 minutes)
# Installs and starts 5 AI microservices
.\5-deploy-python-services.ps1

# 4. Deploy Frontend (10 minutes)
# Builds React app and deploys to IIS
.\6-deploy-frontend.ps1

# 5. Setup Cloudflare Tunnel (5 minutes)
# Connects your domains to the VM
.\7-setup-cloudflare-tunnel.ps1

# 6. Test Everything (2 minutes)
# Verifies all services are working
.\8-test-deployment.ps1
```

---

### PHASE 9: DNS Migration (After testing)

**24 hours before migration:**
1. In Cloudflare, lower TTL to 300 seconds (5 minutes)

**During migration:**
1. Verify all tests pass in script 8
2. DNS is already configured by script 7
3. Test domains:
   - https://doganconsult.com
   - https://api.doganconsult.com
   - https://ds.doganconsult.com

**After migration:**
1. Monitor for 48 hours
2. Keep old server (91.98.34.142) as backup for 30 days
3. Raise TTL back to normal

---

## 📊 Progress Tracking

Tell me when you complete each phase:

| Phase | Command to Tell Me | Status |
|-------|-------------------|--------|
| VM Created | "vm created" | ⏳ Pending |
| Windows Installed | "windows installed" | ⏳ Pending |
| Files Copied | "files copied" | ⏳ Pending |
| Software Installed | "software done" | ⏳ Pending |
| Backend Deployed | "backend done" | ⏳ Pending |
| Python Services | "services done" | ⏳ Pending |
| Frontend Deployed | "frontend done" | ⏳ Pending |
| Tunnel Setup | "tunnel done" | ⏳ Pending |
| Testing Complete | "tests passed" | ⏳ Pending |

---

## 📂 All Script Files

Location: `d:\DoganSystem\`

| Script | Purpose | Time |
|--------|---------|------|
| `3-install-software.ps1` | Installs all required software | 45 min |
| `4-deploy-backend.ps1` | Deploys ASP.NET Core backend | 10 min |
| `5-deploy-python-services.ps1` | Deploys AI microservices | 15 min |
| `6-deploy-frontend.ps1` | Builds and deploys React app | 10 min |
| `7-setup-cloudflare-tunnel.ps1` | Configures Cloudflare Tunnel | 5 min |
| `8-test-deployment.ps1` | Tests entire deployment | 2 min |

---

## 🎯 What Each Script Does

### Script 3: Install Software
- IIS with all required features
- .NET 8.0 Hosting Bundle
- SQL Server 2022 Express
- Python 3.11
- Node.js 18 LTS
- Git, NSSM, Cloudflared

### Script 4: Deploy Backend
- Builds DoganSystem from source
- Creates SQL Server database
- Configures IIS with app pool
- Sets up appsettings.Production.json
- Starts backend API on port 5000

### Script 5: Deploy Python Services
- Creates virtual environment
- Installs Python dependencies
- Creates 5 Windows Services:
  - API Gateway (8006)
  - Agent Server (8001)
  - Tenant Admin (8007)
  - Monitoring (8005)
  - Webhook Receiver (8003)

### Script 6: Deploy Frontend
- Installs npm dependencies
- Builds React production bundle
- Deploys to IIS on port 3000
- Configures SPA routing

### Script 7: Cloudflare Tunnel
- Authenticates with Cloudflare
- Creates tunnel named "dogansystem"
- Routes 6 domains to local services
- Installs as Windows Service
- Provides SSL automatically

### Script 8: Test Deployment
- Tests 7 categories:
  - Windows Services
  - HTTP Endpoints
  - Database Connection
  - IIS Configuration
  - Cloudflare Tunnel
  - Firewall Rules
  - DNS Resolution

---

## 🆘 Troubleshooting

### Script fails with "Access Denied"
- Right-click PowerShell → Run as Administrator

### Cannot copy files to VM
- Enable Enhanced Session in Hyper-V
- Or manually copy via USB/network share

### Service won't start
```powershell
# Check logs
Get-Content C:\PythonServices\DoganSystem\logs\*-error.log -Tail 50

# Restart service
Restart-Service <ServiceName>
```

### Backend returns 500 error
```powershell
# Check logs
Get-Content C:\inetpub\wwwroot\DoganSystem\logs\*.log -Tail 50

# Restart IIS
iisreset
```

### Cloudflare Tunnel not working
```powershell
# Check service
Get-Service cloudflared

# Check tunnel status
cloudflared tunnel info dogansystem

# View logs
Get-EventLog -LogName Application -Source cloudflared -Newest 50
```

---

## 📞 Support

If you encounter any issues:
1. Check the logs (locations in troubleshooting section)
2. Run the test script: `.\8-test-deployment.ps1`
3. Tell me the error message

---

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ All 7 test categories pass in script 8
- ✅ Can access https://doganconsult.com
- ✅ Backend API responds at https://api.doganconsult.com
- ✅ Monitoring dashboard loads at https://ds.doganconsult.com
- ✅ No errors in logs for 24 hours

---

## ⏱️ Total Timeline

| Phase | Time |
|-------|------|
| Create VM | 10 min |
| Install Windows | 20 min |
| Copy Files | 5 min |
| Run All Scripts | 90 min |
| **TOTAL** | **~2 hours** |

---

**YOU ARE HERE:** Ready to create VM in Hyper-V Manager

**START NOW:** Open Hyper-V Manager and follow PHASE 1 above! 🚀
