# 🖥️ VM Local Development Guide

This guide explains how to set up and use Virtual Machines (VMs) on your local PC or laptop to create server environments for developing and testing DoganSystem without cloud provider costs.

## 📋 Overview

Running VMs locally allows you to:
- **Simulate production environments** without cloud costs
- **Test multi-tenant setups** in isolated environments
- **Develop and test** ABP MVC, ERPNext, and Python services separately
- **Practice deployments** in a safe, isolated environment
- **Test different OS configurations** (Windows Server, Linux)

## 🛠️ Available VM Tools

### Free Options

#### 1. **VirtualBox** (Recommended for Beginners)
- **Cost**: Free and open-source
- **Platform**: Windows, macOS, Linux
- **Best for**: General development and testing
- **Download**: https://www.virtualbox.org/
- **Pros**: Easy to use, extensive documentation, large community
- **Cons**: Slightly slower than commercial alternatives

#### 2. **VMware Workstation Player**
- **Cost**: Free for personal/non-commercial use
- **Platform**: Windows, Linux
- **Best for**: Better performance than VirtualBox
- **Download**: https://www.vmware.com/products/workstation-player.html
- **Pros**: Better performance, good Windows integration
- **Cons**: Limited features in free version

#### 3. **KVM/QEMU** (Linux)
- **Cost**: Free and open-source
- **Platform**: Linux only
- **Best for**: Linux-native virtualization
- **Install**: `sudo apt install qemu-kvm libvirt-daemon-system`
- **Pros**: Native Linux integration, excellent performance
- **Cons**: Linux-only, requires more setup

#### 4. **Hyper-V** (Windows)
- **Cost**: Free (built into Windows Pro/Enterprise)
- **Platform**: Windows 10/11 Pro, Windows Server
- **Best for**: Windows Server testing
- **Enable**: `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All`
- **Pros**: Native Windows integration, no additional software
- **Cons**: Requires Windows Pro/Enterprise

### Enterprise/Advanced Options

#### 5. **Proxmox VE**
- **Cost**: Free and open-source
- **Platform**: Debian-based Linux
- **Best for**: Advanced users, multiple VMs, web-based management
- **Download**: https://www.proxmox.com/
- **Pros**: Web UI, container support, clustering
- **Cons**: Requires dedicated server or VM

#### 6. **Xen**
- **Cost**: Free and open-source
- **Platform**: Linux
- **Best for**: Enterprise-grade virtualization
- **Pros**: Type-1 hypervisor, excellent performance
- **Cons**: Complex setup, requires expertise

## 🚀 Quick Start with VirtualBox

### Step 1: Install VirtualBox

1. Download from https://www.virtualbox.org/
2. Install with default settings
3. Install VirtualBox Extension Pack (for USB 3.0, RDP, etc.)

### Step 2: Create Your First VM

#### Option A: Ubuntu Server 22.04 LTS (Recommended for DoganSystem)

```bash
# Download Ubuntu Server ISO
# https://ubuntu.com/download/server

# In VirtualBox:
# 1. Click "New"
# 2. Name: "DoganSystem-Dev"
# 3. Type: Linux
# 4. Version: Ubuntu (64-bit)
# 5. Memory: 4096 MB (4GB minimum, 8GB recommended)
# 6. Hard disk: Create virtual hard disk (VDI, 40GB+)
# 7. Click "Create"
```

#### Option B: Windows Server 2022 (For Windows-specific testing)

```bash
# Download Windows Server ISO (Evaluation)
# https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2022

# In VirtualBox:
# 1. Click "New"
# 2. Name: "DoganSystem-Windows"
# 3. Type: Microsoft Windows
# 4. Version: Windows 2022 (64-bit)
# 5. Memory: 8192 MB (8GB minimum)
# 6. Hard disk: 60GB+
```

### Step 3: Configure VM Settings

**Before starting the VM, configure:**

1. **System → Processor**
   - Enable "Enable PAE/NX" (if needed)
   - Processors: 2-4 cores (based on host CPU)

2. **Network → Adapter 1**
   - Attached to: NAT (for internet access)
   - Or: Bridged Adapter (for network access)

3. **Storage → Controller: IDE**
   - Add Ubuntu/Windows ISO to optical drive

4. **Shared Folders** (Optional)
   - Add host folder for easy file sharing

### Step 4: Install Guest OS

1. Start the VM
2. Follow OS installation wizard
3. Install Guest Additions (for better performance):
   - VirtualBox menu: Devices → Insert Guest Additions CD
   - In VM: Mount and run the installer

## 🏗️ Setting Up DoganSystem in VM

### Ubuntu Server VM Setup

#### 1. Install Prerequisites

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install .NET 8.0 SDK
wget https://dot.net/v1/dotnet-install.sh
chmod +x dotnet-install.sh
./dotnet-install.sh --channel 8.0

# Add to PATH
echo 'export DOTNET_ROOT=$HOME/.dotnet' >> ~/.bashrc
echo 'export PATH=$PATH:$HOME/.dotnet:$HOME/.dotnet/tools' >> ~/.bashrc
source ~/.bashrc

# Install SQL Server (or use SQLite for testing)
# For SQL Server on Linux:
curl -o /tmp/mssql-server.deb https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb
sudo dpkg -i /tmp/mssql-server.deb
sudo apt-get update
sudo apt-get install -y mssql-server

# Or use SQLite (simpler for testing)
sudo apt install sqlite3

# Install Python 3.10+
sudo apt install python3.10 python3-pip python3-venv

# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Git
sudo apt install git
```

#### 2. Clone and Build DoganSystem

```bash
# Clone repository (or copy from host via shared folder)
git clone https://github.com/doganlap/DoganSystem.git
cd DoganSystem

# Restore and build
dotnet restore
dotnet build DoganSystem.sln --configuration Release

# Setup database
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add Initial --startup-project ../DoganSystem.Web.Mvc
dotnet ef database update --startup-project ../DoganSystem.Web.Mvc
```

#### 3. Configure Network Access

```bash
# Find VM IP address
ip addr show

# Or configure static IP (optional)
sudo nano /etc/netplan/00-installer-config.yaml
```

#### 4. Run DoganSystem

```bash
cd src/DoganSystem.Web.Mvc
dotnet run --urls "http://0.0.0.0:5000"
```

**Access from host machine:**
- Find VM IP: `ip addr show` or check VirtualBox network settings
- Access: `http://<VM_IP>:5000`

### Windows Server VM Setup

#### 1. Install Prerequisites

```powershell
# Install .NET 8.0 SDK
# Download from: https://dotnet.microsoft.com/download/dotnet/8.0

# Install SQL Server Express
# Download from: https://www.microsoft.com/en-us/sql-server/sql-server-downloads

# Install Python 3.10+
# Download from: https://www.python.org/downloads/

# Install Node.js 18+
# Download from: https://nodejs.org/
```

#### 2. Configure Windows Firewall

```powershell
# Allow port 5000 for DoganSystem
New-NetFirewallRule -DisplayName "DoganSystem HTTP" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

#### 3. Build and Run

```powershell
# Same as Ubuntu setup
cd DoganSystem
dotnet restore
dotnet build DoganSystem.sln --configuration Release
cd src\DoganSystem.Web.Mvc
dotnet run --urls "http://0.0.0.0:5000"
```

## 🔧 VM Configuration Scenarios

### Scenario 1: Full Stack Testing

**Setup:**
- **VM 1**: Ubuntu Server - ABP MVC Application
- **VM 2**: Ubuntu Server - ERPNext Instance
- **VM 3**: Ubuntu Server - Python Services

**Network**: Use Bridged Adapter so VMs can communicate

**Benefits**: Test complete multi-tenant architecture

### Scenario 2: Multi-Tenant Testing

**Setup:**
- **VM 1**: Main DoganSystem (Tenant Management)
- **VM 2**: Tenant A ERPNext Instance
- **VM 3**: Tenant B ERPNext Instance

**Benefits**: Test tenant isolation and management

### Scenario 3: Production Simulation

**Setup:**
- **VM 1**: Web Server (Nginx + ABP MVC)
- **VM 2**: Database Server (SQL Server)
- **VM 3**: Application Server (Python Services)

**Benefits**: Practice production-like deployments

## 📊 Resource Recommendations

### Minimum Requirements (Single VM)

- **RAM**: 4GB (8GB recommended)
- **CPU**: 2 cores (4 cores recommended)
- **Storage**: 40GB (60GB+ recommended)
- **Network**: NAT or Bridged Adapter

### Recommended for Multi-VM Setup

- **Host RAM**: 16GB+ (allocate 4-8GB per VM)
- **Host CPU**: 4+ cores (2 cores per VM)
- **Host Storage**: 200GB+ SSD
- **Network**: Bridged Adapter for VM communication

## 🔐 Security Best Practices

1. **Isolate VMs**: Use separate VMs for testing untrusted code
2. **Snapshots**: Create snapshots before major changes
3. **Network Isolation**: Use NAT for internet-only access, Bridged for local network
4. **Updates**: Keep guest OS updated
5. **Firewall**: Configure firewall rules in guest OS

## 💾 VM Management Tips

### Snapshots

```bash
# VirtualBox: Create snapshot before major changes
# Right-click VM → Snapshots → Take Snapshot

# Restore snapshot if something breaks
# Right-click VM → Snapshots → Restore Snapshot
```

### Cloning VMs

```bash
# VirtualBox: Right-click VM → Clone
# Useful for creating multiple test environments
```

### Shared Folders

```bash
# VirtualBox: Settings → Shared Folders
# Add host folder, mount in guest:
sudo mount -t vboxsf <share_name> /mnt/shared
```

### Export/Import

```bash
# Export VM for backup or sharing
# VirtualBox: File → Export Appliance

# Import VM
# VirtualBox: File → Import Appliance
```

## 🐛 Troubleshooting

### VM Won't Start

- **Check**: Host has enough RAM/CPU resources
- **Solution**: Close other applications, reduce VM memory allocation

### Slow Performance

- **Enable**: Hardware acceleration (VT-x/AMD-V) in BIOS
- **Install**: Guest Additions
- **Allocate**: More RAM/CPU to VM
- **Use**: SSD instead of HDD

### Network Issues

- **NAT**: VM can access internet, but host can't access VM directly
- **Bridged**: VM gets IP on local network, accessible from host
- **Host-Only**: VMs can communicate, but no internet access

### Can't Access VM from Host

```bash
# Check VM IP
ip addr show  # Linux
ipconfig      # Windows

# Check firewall
sudo ufw status  # Linux
# Allow port in Windows Firewall

# Test connection
ping <VM_IP>
curl http://<VM_IP>:5000
```

## 📚 Additional Resources

- **VirtualBox Manual**: https://www.virtualbox.org/manual/
- **VMware Documentation**: https://docs.vmware.com/
- **KVM Documentation**: https://www.linux-kvm.org/page/Documents
- **Hyper-V Guide**: https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/

## 🎯 Use Cases for DoganSystem

### 1. Development Environment
- Isolated development without affecting host system
- Test different .NET/Python versions
- Experiment with configurations

### 2. Testing
- Test multi-tenant scenarios
- Load testing in isolated environment
- Integration testing with multiple services

### 3. Training
- Practice deployments
- Learn Linux/Windows Server administration
- Test disaster recovery procedures

### 4. Demo Environment
- Create clean demo environment
- Reset easily with snapshots
- Showcase to clients without cloud costs

## ✅ Quick Checklist

- [ ] Choose VM tool (VirtualBox recommended for beginners)
- [ ] Install VM software
- [ ] Download OS ISO (Ubuntu Server 22.04 recommended)
- [ ] Create VM with adequate resources (4GB RAM, 40GB disk)
- [ ] Install guest OS
- [ ] Install Guest Additions
- [ ] Install DoganSystem prerequisites (.NET, Python, Node.js)
- [ ] Clone and build DoganSystem
- [ ] Configure network (Bridged or NAT)
- [ ] Test access from host machine
- [ ] Create snapshot for easy rollback

---

**Ready to develop and test DoganSystem in isolated VM environments!** 🚀

For questions or issues, refer to the main [README.md](README.md) or [QUICK_START.md](QUICK_START.md).
