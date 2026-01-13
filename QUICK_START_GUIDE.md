# DoganSystem Deployment - Quick Start Guide

## Current Status: ✅ Hyper-V Enabled & Restarted

---

## NEXT STEPS (Do These Now):

### Step 1: Create VM in Hyper-V Manager (10 minutes)

1. Open Hyper-V Manager: Press `Win+R`, type `virtmgmt.msc`, press Enter
2. Right-click computer name → New → Virtual Machine
3. Name: `DoganSystem-Production`
4. Generation 2
5. Memory: 24576 MB, check "Use Dynamic Memory"
6. Network: Default Switch
7. Disk: 150 GB
8. ISO: Browse to Windows Server 2022 ISO (download from https://microsoft.com/evalcenter if needed)
9. After creation, right-click VM → Settings → Processor → Set to 10 cores
10. Start VM

### Step 2: Install Windows Server (20 minutes)

1. Connect to VM
2. Install Windows Server 2022 Standard Evaluation (Desktop Experience)
3. Set Administrator password: `DoganAdmin2024!`
4. Login

### Step 3: Copy Files to VM (5 minutes)

In VM PowerShell:
```powershell
New-Item -Path "C:\DoganSystem" -ItemType Directory
# Copy files from host using network share or enhanced session
```

### Step 4: Run Deployment Scripts (90 minutes)

In VM PowerShell as Administrator:
```powershell
cd C:\DoganSystem
.\3-install-software.ps1          # 45 min
.\4-deploy-backend.ps1           # 10 min
.\5-deploy-python-services.ps1   # 15 min
.\6-deploy-frontend.ps1          # 10 min
```

---

## Tell me when each step completes!

Type:
- "vm created" when Step 1 done
- "windows installed" when Step 2 done
- "files copied" when Step 3 done
- "deployment done" when Step 4 done

Then I'll provide Cloudflare Tunnel setup and DNS migration scripts!
