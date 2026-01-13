# Hyper-V Setup Instructions for DoganSystem

## Quick Start (3 Steps)

### Step 1: Enable Hyper-V and Create Virtual Switch

**Open PowerShell as Administrator** (Right-click PowerShell → Run as Administrator)

```powershell
cd d:\DoganSystem
.\setup-hyperv.ps1
```

- This will enable Hyper-V features if needed
- Create virtual network switch
- Set up storage paths
- **May require a restart**

---

### Step 2: Download Windows Server 2022 ISO

**Download from Microsoft:**
- URL: https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2022
- Select: **Windows Server 2022 Standard**
- Edition: **64-bit**
- Format: **ISO**
- Save to: `C:\ISOs\WindowsServer2022.iso` (or remember the path)

**File size:** ~5 GB
**Download time:** 10-30 minutes depending on your internet speed

---

### Step 3: Create the VM

**Open PowerShell as Administrator again:**

```powershell
cd d:\DoganSystem
.\create-hyperv-vm.ps1
```

- Script will prompt for ISO file location
- Enter the path where you saved the ISO
- Confirm VM creation
- VM will be created with:
  - **10 CPU cores**
  - **24 GB RAM** (dynamic 8-32 GB)
  - **150 GB disk**
  - Windows Server 2022 ISO attached

---

## After VM Creation

### Install Windows Server 2022

1. **Open Hyper-V Manager:**
   - Press `Win + R`
   - Type: `virtmgmt.msc`
   - Press Enter

2. **Connect to VM:**
   - In Hyper-V Manager, find `DoganSystem-Production`
   - Right-click → **Connect**
   - Click **Start**

3. **Windows Installation:**
   - Select language: **English**
   - Click **Install now**
   - Select: **Windows Server 2022 Standard (Desktop Experience)**
   - Accept license terms
   - Choose: **Custom: Install Windows only (advanced)**
   - Select the disk → Click **Next**
   - Wait for installation (15-20 minutes)

4. **Initial Configuration:**
   - Set Administrator password: **Use a strong password!**
   - Press `Ctrl+Alt+Delete` → Log in
   - Complete setup

---

## Quick Commands Reference

### Check Hyper-V Status
```powershell
Get-WindowsOptionalFeature -Online -FeatureName *Hyper-V*
```

### List Virtual Switches
```powershell
Get-VMSwitch
```

### List VMs
```powershell
Get-VM
```

### Start VM
```powershell
Start-VM -Name "DoganSystem-Production"
```

### Stop VM
```powershell
Stop-VM -Name "DoganSystem-Production"
```

### Connect to VM
```powershell
vmconnect localhost "DoganSystem-Production"
```

---

## Troubleshooting

### Issue: "Hyper-V cannot be installed"
**Solution:** Your CPU supports virtualization (AMD-V enabled), but Windows Pro/Enterprise is required. Check your Windows edition:
```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion
```

### Issue: "Virtual switch creation failed"
**Solution:** No problem - the script will create an Internal switch instead. You can use Cloudflare Tunnel for internet connectivity (Phase 6).

### Issue: "Not enough disk space"
**Solution:** You have 1,398 GB free on C: and 343 GB on D:, which is plenty. The script uses C: drive by default.

### Issue: "Cannot start VM - memory error"
**Solution:** Close other applications to free up RAM. You have 95 GB total, so this shouldn't happen.

---

## Next Steps After Windows Installation

Once Windows Server 2022 is installed in the VM, we'll proceed with:

1. **Phase 2:** Install software (IIS, .NET, SQL Server, Python, Node.js)
2. **Phase 3:** Deploy DoganSystem backend
3. **Phase 4:** Deploy Python AI services
4. **Phase 5:** Deploy frontend
5. **Phase 6:** Setup Cloudflare Tunnel
6. **Phase 7:** Migrate DNS to new infrastructure

---

## Download Links Summary

| Software | URL |
|----------|-----|
| Windows Server 2022 ISO | https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2022 |
| .NET 8.0 Hosting Bundle | https://dotnet.microsoft.com/download/dotnet/8.0 |
| SQL Server 2022 Express | https://www.microsoft.com/en-us/sql-server/sql-server-downloads |
| Python 3.11 | https://www.python.org/downloads/ |
| Node.js 18 LTS | https://nodejs.org/ |
| Cloudflared | https://github.com/cloudflare/cloudflared/releases |

---

## Support

If you encounter any issues, check:
1. Windows Event Viewer (eventvwr.msc)
2. Hyper-V event logs
3. Script output messages

All scripts are located in: `d:\DoganSystem\`
