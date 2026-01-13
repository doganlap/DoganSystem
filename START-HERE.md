# DoganSystem Hyper-V Deployment - START HERE

## Quick Setup Guide

Follow these steps in order to deploy DoganSystem to a Hyper-V VM:

---

## Phase 1: Hyper-V Setup (15 minutes)

### Step 1: Enable Hyper-V ✅ IN PROGRESS

**I've launched the script for you!**

A command window should have opened asking for Administrator approval.

**What to do:**
1. Look for the UAC (User Account Control) prompt
2. Click **Yes** to allow
3. The script will enable Hyper-V features
4. **You will need to RESTART your computer** after this completes

**If nothing happened:**
- Run manually: Right-click `d:\DoganSystem\1-enable-hyperv.bat` → Run as Administrator

---

### Step 2: Download Windows Server 2022 ISO (While Waiting)

**While your computer restarts, download the ISO:**

1. Go to: https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2022
2. Fill in the form (you can use fake info for evaluation)
3. Select:
   - **Product:** Windows Server 2022
   - **Edition:** Standard
   - **Language:** English
   - **Format:** ISO
4. Download and save to: `C:\ISOs\WindowsServer2022.iso`
   - Create the `C:\ISOs` folder if it doesn't exist
5. **File size:** ~5 GB
6. **Download time:** 10-30 minutes

---

### Step 3: Create the VM (After Restart)

**After your computer restarts:**

1. **Option A:** Double-click `d:\DoganSystem\2-create-vm.bat`
   - Or right-click → Run as Administrator

2. **Option B:** Open PowerShell as Admin and run:
   ```powershell
   cd d:\DoganSystem
   .\create-vm.ps1
   ```

**The script will:**
- ✅ Check for the ISO file
- ✅ Create a 150 GB virtual hard disk
- ✅ Create the VM with 10 CPU cores and 24 GB RAM
- ✅ Attach the ISO
- ✅ Configure settings
- ✅ Ask if you want to start it

---

### Step 4: Install Windows Server 2022

**Once the VM starts:**

1. **Hyper-V Manager will open** (or open it manually: Press `Win+R`, type `virtmgmt.msc`)

2. **Connect to the VM:**
   - Find "DoganSystem-Production" in the list
   - Right-click → **Connect**
   - Double-click to open the window
   - Click **Start** if not already started

3. **Windows Installation:**
   - Press any key to boot from DVD
   - Select language: **English**
   - Click **Install now**
   - When asked for product key, click **I don't have a product key**
   - Select: **Windows Server 2022 Standard Evaluation (Desktop Experience)**
   - Accept license terms
   - Choose: **Custom: Install Windows only (advanced)**
   - Select the disk → Click **Next**
   - Wait 15-20 minutes for installation

4. **Initial Setup:**
   - Set Administrator password (REMEMBER THIS!)
     - Example: `DoganAdmin2024!`
   - Log in with the password

---

## Phase 2: Software Installation (1 hour)

**After Windows is installed, we'll install:**

1. IIS (Internet Information Services)
2. .NET 8.0 Hosting Bundle
3. SQL Server 2022 Express
4. Python 3.11
5. Node.js 18 LTS
6. Redis
7. Git
8. Cloudflare Tunnel (cloudflared)

**I'll provide PowerShell scripts for this once Phase 1 is complete.**

---

## Phase 3-7: Application Deployment (2-3 hours)

1. Deploy DoganSystem backend (ASP.NET Core)
2. Deploy Python AI services
3. Deploy React frontend
4. Setup Cloudflare Tunnel
5. Migrate DNS from old server (91.98.34.142)

---

## Current Status

| Phase | Status | Duration |
|-------|--------|----------|
| **Phase 1: Hyper-V & VM Setup** | 🟡 IN PROGRESS | 15-30 min |
| Phase 2: Software Installation | ⏳ Waiting | 1 hour |
| Phase 3: Backend Deployment | ⏳ Waiting | 30 min |
| Phase 4: Python Services | ⏳ Waiting | 30 min |
| Phase 5: Frontend Deployment | ⏳ Waiting | 20 min |
| Phase 6: Cloudflare Tunnel | ⏳ Waiting | 20 min |
| Phase 7: DNS Migration | ⏳ Waiting | 10 min |

**Total Time:** ~3-4 hours of active work

---

## What's Next?

### Right Now:
1. ✅ Hyper-V enablement script is running
2. ⏳ **Wait for restart prompt**
3. ⏳ **Restart your computer**
4. ⏳ **Download Windows Server ISO** (while computer restarts)
5. ⏳ **Run Step 3** after restart

### After Windows Installation:
- Tell me "Windows installed" and I'll provide the next scripts

---

## Troubleshooting

### Issue: "Hyper-V cannot be installed"
**Check Windows edition:**
```powershell
Get-ComputerInfo | Select-Object WindowsProductName
```
- Hyper-V requires Windows 10/11 Pro, Enterprise, or Education
- If you have Windows Home, you'll need to upgrade or use VirtualBox instead

### Issue: "Virtualization is not enabled"
- This shouldn't happen - your system already has virtualization enabled
- If it does, reboot and enable AMD-V in BIOS

### Issue: ISO download failed
- Try alternative link: https://go.microsoft.com/fwlink/p/?LinkID=2195280&clcid=0x409&culture=en-us&country=US
- Or use any Windows Server 2022 Evaluation ISO

### Issue: VM won't start
```powershell
# Check VM status
Get-VM "DoganSystem-Production"

# Try starting manually
Start-VM -Name "DoganSystem-Production"

# Check logs
Get-VMIntegrationService -VMName "DoganSystem-Production"
```

---

## Files in This Directory

| File | Purpose |
|------|---------|
| `START-HERE.md` | ← YOU ARE HERE |
| `1-enable-hyperv.bat` | Enable Hyper-V features |
| `2-create-vm.bat` | Create the VM |
| `create-vm.ps1` | PowerShell script for VM creation |
| `HYPER-V-SETUP-INSTRUCTIONS.md` | Detailed instructions |
| `check_hardware.ps1` | Hardware compatibility check |

---

## Need Help?

**Common commands:**

```powershell
# List all VMs
Get-VM

# Start VM
Start-VM -Name "DoganSystem-Production"

# Stop VM
Stop-VM -Name "DoganSystem-Production"

# Connect to VM
vmconnect localhost "DoganSystem-Production"

# Check Hyper-V status
Get-WindowsOptionalFeature -Online -FeatureName *Hyper-V*
```

---

## Architecture Reminder

```
Internet → Cloudflare DNS → Cloudflare Tunnel → Host Machine → Hyper-V VM → DoganSystem
```

Your current server: **DOGAN-LAP06**
- CPU: AMD Ryzen AI 9 HX 370 (12 cores/24 threads) ✅
- RAM: 95 GB ✅
- Disk: 1.4 TB free on C:, 343 GB free on D: ✅
- Virtualization: Enabled ✅

**Perfect for this deployment!**

---

Last Updated: 2026-01-13
