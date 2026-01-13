# DoganSystem Enhanced VM Creation Script
# Creates a Hyper-V VM optimized for Docker workloads
# Run this on the Windows 11 Pro HOST machine

#Requires -Version 7.0
#Requires -RunAsAdministrator
#Requires -Modules Hyper-V

param(
    [string]$VMName = "DoganSystem-Production",
    [string]$ISOPath = "C:\ISOs\WindowsServer2022.iso",
    [int]$ProcessorCount = 10,
    [long]$MemoryStartupGB = 8,
    [long]$MemoryMaximumGB = 24,
    [long]$DiskSizeGB = 150,
    [long]$DataDiskSizeGB = 100,
    [string]$VHDPath = "C:\Hyper-V\Virtual Hard Disks",
    [string]$VMPath = "C:\Hyper-V\Virtual Machines",
    [string]$SwitchName = "Default Switch",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " DoganSystem - Enhanced VM Creation" -ForegroundColor Cyan
Write-Host " Optimized for Docker Workloads" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Validate Hyper-V
Write-Host "Step 1: Validating Hyper-V..." -ForegroundColor Yellow
try {
    $hypervFeature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All
    if ($hypervFeature.State -ne "Enabled") {
        Write-Host "  ERROR: Hyper-V is not enabled!" -ForegroundColor Red
        Write-Host "  Run: .\1-enable-hyperv.bat" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "  ✓ Hyper-V is enabled" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Could not check Hyper-V status" -ForegroundColor Red
    exit 1
}

# Check if VM already exists
Write-Host ""
Write-Host "Step 2: Checking for existing VM..." -ForegroundColor Yellow
$existingVM = Get-VM -Name $VMName -ErrorAction SilentlyContinue

if ($existingVM) {
    if ($Force) {
        Write-Host "  Existing VM found - removing (Force specified)" -ForegroundColor Yellow
        if ($existingVM.State -eq "Running") {
            Stop-VM -Name $VMName -Force
        }
        Remove-VM -Name $VMName -Force
        Write-Host "  ✓ Existing VM removed" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: VM '$VMName' already exists!" -ForegroundColor Red
        Write-Host "  Use -Force to remove it, or choose a different name with -VMName" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "  ✓ VM name available" -ForegroundColor Green
}

# Validate ISO
Write-Host ""
Write-Host "Step 3: Validating Windows Server ISO..." -ForegroundColor Yellow
if (-not (Test-Path $ISOPath)) {
    Write-Host "  ERROR: ISO not found: $ISOPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Download Windows Server 2022 from:" -ForegroundColor Yellow
    Write-Host "  https://www.microsoft.com/en-us/evalcenter/download-windows-server-2022" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Or specify a different path with -ISOPath parameter" -ForegroundColor Yellow
    exit 1
}

$isoSize = [math]::Round((Get-Item $ISOPath).Length / 1GB, 2)
Write-Host "  ✓ ISO found: $ISOPath ($isoSize GB)" -ForegroundColor Green

# Check virtual switch
Write-Host ""
Write-Host "Step 4: Checking virtual switch..." -ForegroundColor Yellow
$vSwitch = Get-VMSwitch -Name $SwitchName -ErrorAction SilentlyContinue

if (-not $vSwitch) {
    Write-Host "  Switch '$SwitchName' not found" -ForegroundColor Yellow
    Write-Host "  Available switches:" -ForegroundColor Gray
    Get-VMSwitch | ForEach-Object {
        Write-Host "    - $($_.Name) ($($_.SwitchType))" -ForegroundColor White
    }

    Write-Host ""
    Write-Host "  Creating internal switch with NAT..." -ForegroundColor Yellow
    $SwitchName = "DoganSystem-Switch"

    New-VMSwitch -Name $SwitchName -SwitchType Internal | Out-Null
    $ifIndex = (Get-NetAdapter -Name "vEthernet ($SwitchName)").ifIndex
    New-NetIPAddress -IPAddress 192.168.100.1 -PrefixLength 24 -InterfaceIndex $ifIndex | Out-Null
    New-NetNAT -Name "DoganSystem-NAT" -InternalIPInterfaceAddressPrefix 192.168.100.0/24 | Out-Null

    Write-Host "  ✓ Switch created: $SwitchName" -ForegroundColor Green
} else {
    Write-Host "  ✓ Switch found: $SwitchName ($($vSwitch.SwitchType))" -ForegroundColor Green
}

# Create VM directories
Write-Host ""
Write-Host "Step 5: Creating VM directories..." -ForegroundColor Yellow
if (-not (Test-Path $VHDPath)) {
    New-Item -Path $VHDPath -ItemType Directory -Force | Out-Null
    Write-Host "  Created: $VHDPath" -ForegroundColor Gray
}
if (-not (Test-Path $VMPath)) {
    New-Item -Path $VMPath -ItemType Directory -Force | Out-Null
    Write-Host "  Created: $VMPath" -ForegroundColor Gray
}
Write-Host "  ✓ Directories ready" -ForegroundColor Green

# Create VHD paths
$osDisk = Join-Path $VHDPath "$VMName-OS.vhdx"
$dataDisk = Join-Path $VHDPath "$VMName-Data.vhdx"

# Create the VM
Write-Host ""
Write-Host "Step 6: Creating virtual machine..." -ForegroundColor Yellow
Write-Host "  Name: $VMName" -ForegroundColor White
Write-Host "  Generation: 2 (UEFI)" -ForegroundColor White
Write-Host "  Processors: $ProcessorCount cores" -ForegroundColor White
Write-Host "  Memory: $MemoryStartupGB GB (startup), $MemoryMaximumGB GB (maximum)" -ForegroundColor White
Write-Host "  OS Disk: $DiskSizeGB GB" -ForegroundColor White
Write-Host "  Data Disk: $DataDiskSizeGB GB (for Docker volumes)" -ForegroundColor White
Write-Host ""

# Create VM
New-VM -Name $VMName `
    -Path $VMPath `
    -MemoryStartupBytes ($MemoryStartupGB * 1GB) `
    -Generation 2 `
    -NewVHDPath $osDisk `
    -NewVHDSizeBytes ($DiskSizeGB * 1GB) `
    -SwitchName $SwitchName | Out-Null

Write-Host "  ✓ VM created" -ForegroundColor Green

# Configure VM
Write-Host ""
Write-Host "Step 7: Configuring VM..." -ForegroundColor Yellow

# Set processor count
Set-VMProcessor -VMName $VMName -Count $ProcessorCount
Write-Host "  Set processors: $ProcessorCount cores" -ForegroundColor Gray

# Configure dynamic memory
Set-VMMemory -VMName $VMName `
    -DynamicMemoryEnabled $true `
    -StartupBytes ($MemoryStartupGB * 1GB) `
    -MinimumBytes ($MemoryStartupGB * 1GB) `
    -MaximumBytes ($MemoryMaximumGB * 1GB)
Write-Host "  Set dynamic memory: $MemoryStartupGB-$MemoryMaximumGB GB" -ForegroundColor Gray

# Enable nested virtualization (CRITICAL for Docker)
Set-VMProcessor -VMName $VMName -ExposeVirtualizationExtensions $true
Write-Host "  ✓ Enabled nested virtualization (required for Docker)" -ForegroundColor Green

# Disable checkpoints (for better performance)
Set-VM -VMName $VMName -CheckpointType Disabled
Write-Host "  Disabled automatic checkpoints" -ForegroundColor Gray

# Enable Enhanced Session Mode
Set-VM -VMName $VMName -EnhancedSessionTransportType HvSocket
Write-Host "  Enabled Enhanced Session Mode (for easy file copy)" -ForegroundColor Gray

# Configure automatic start/stop
Set-VM -VMName $VMName -AutomaticStartAction Start -AutomaticStopAction ShutDown
Write-Host "  Configured auto-start on host boot" -ForegroundColor Gray

# Add DVD drive for ISO
Add-VMDvdDrive -VMName $VMName -Path $ISOPath
Write-Host "  Attached ISO: $ISOPath" -ForegroundColor Gray

# Set boot order (DVD first)
$dvd = Get-VMDvdDrive -VMName $VMName
$disk = Get-VMHardDiskDrive -VMName $VMName
$net = Get-VMNetworkAdapter -VMName $VMName
Set-VMFirmware -VMName $VMName -BootOrder $dvd, $disk, $net
Write-Host "  Set boot order: DVD, Disk, Network" -ForegroundColor Gray

# Disable Secure Boot (for compatibility)
Set-VMFirmware -VMName $VMName -EnableSecureBoot Off
Write-Host "  Disabled Secure Boot (for broader OS compatibility)" -ForegroundColor Gray

Write-Host "  ✓ VM configured" -ForegroundColor Green

# Create and attach data disk for Docker
Write-Host ""
Write-Host "Step 8: Creating data disk for Docker volumes..." -ForegroundColor Yellow
New-VHD -Path $dataDisk -SizeBytes ($DataDiskSizeGB * 1GB) -Dynamic | Out-Null
Add-VMHardDiskDrive -VMName $VMName -Path $dataDisk
Write-Host "  ✓ Data disk created and attached: $DataDiskSizeGB GB" -ForegroundColor Green
Write-Host "    (Initialize this disk in Windows after installation)" -ForegroundColor Gray

# Display configuration
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " ✓ VM Created Successfully!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "VM Configuration:" -ForegroundColor Cyan
Write-Host "  Name: $VMName" -ForegroundColor White
Write-Host "  Generation: 2 (UEFI)" -ForegroundColor White
Write-Host "  Processors: $ProcessorCount cores" -ForegroundColor White
Write-Host "  Memory: $MemoryStartupGB-$MemoryMaximumGB GB (dynamic)" -ForegroundColor White
Write-Host "  OS Disk: $osDisk ($DiskSizeGB GB)" -ForegroundColor White
Write-Host "  Data Disk: $dataDisk ($DataDiskSizeGB GB)" -ForegroundColor White
Write-Host "  Network: $SwitchName" -ForegroundColor White
Write-Host "  ISO: $ISOPath" -ForegroundColor White
Write-Host ""

Write-Host "Special Features:" -ForegroundColor Cyan
Write-Host "  ✓ Nested Virtualization (for Docker)" -ForegroundColor White
Write-Host "  ✓ Enhanced Session Mode (for file copy)" -ForegroundColor White
Write-Host "  ✓ Dynamic Memory" -ForegroundColor White
Write-Host "  ✓ Auto-start on host boot" -ForegroundColor White
Write-Host "  ✓ Separate data disk for Docker" -ForegroundColor White
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Start VM: Start-VM -Name '$VMName'" -ForegroundColor White
Write-Host "  2. Connect: vmconnect localhost '$VMName'" -ForegroundColor White
Write-Host "  3. Install Windows Server 2022 (Desktop Experience)" -ForegroundColor White
Write-Host "  4. After Windows is installed:" -ForegroundColor White
Write-Host "     a. Initialize the data disk (Disk Management)" -ForegroundColor White
Write-Host "     b. Format as D: drive (or E:)" -ForegroundColor White
Write-Host "     c. Enable Enhanced Session in VM (Settings → Remote Desktop)" -ForegroundColor White
Write-Host "     d. Copy deployment-package.zip to VM" -ForegroundColor White
Write-Host "     e. Extract and run 3-initialize-vm.ps1" -ForegroundColor White
Write-Host ""

$response = Read-Host "Start VM now? (Y/n)"
if ($response -eq '' -or $response -eq 'Y' -or $response -eq 'y') {
    Write-Host ""
    Write-Host "Starting VM..." -ForegroundColor Yellow
    Start-VM -Name $VMName

    Start-Sleep -Seconds 2

    Write-Host "Launching VM Connect..." -ForegroundColor Yellow
    vmconnect localhost $VMName

    Write-Host ""
    Write-Host "VM is starting. Install Windows Server 2022 from the ISO." -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "VM created but not started." -ForegroundColor Yellow
    Write-Host "Start manually: Start-VM -Name '$VMName'" -ForegroundColor White
    Write-Host ""
}
