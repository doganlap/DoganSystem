# DoganSystem VM Initialization Script
# Installs Docker Desktop and prepares the VM for deployment
# Run this INSIDE the VM after Windows Server installation
#
# CRITICAL CHANGE from old script 3:
# - Does NOT install IIS, SQL Server, Python, Node.js
# - ONLY installs Docker Desktop and utilities
# - All services will run in Docker containers

#Requires -Version 7.0
#Requires -RunAsAdministrator

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " DoganSystem - VM Initialization" -ForegroundColor Cyan
Write-Host " Docker-Based Deployment" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "IMPORTANT: This script installs Docker Desktop ONLY" -ForegroundColor Yellow
Write-Host "Old approach (IIS/SQL Server/Python) is replaced with containers" -ForegroundColor Yellow
Write-Host ""

# Create directories
Write-Host "Step 1: Creating directory structure..." -ForegroundColor Yellow
$directories = @(
    "C:\Installers",
    "C:\DoganSystem",
    "C:\DoganSystem\logs",
    "C:\DoganSystem\backups",
    "C:\Scripts"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Gray
    } else {
        Write-Host "  Exists: $dir" -ForegroundColor Gray
    }
}
Write-Host "  ✓ Directory structure ready" -ForegroundColor Green

# Set execution policy
Write-Host ""
Write-Host "Step 2: Configuring PowerShell..." -ForegroundColor Yellow
Set-ExecutionPolicy RemoteSigned -Force -Scope LocalMachine
Write-Host "  ✓ Execution policy set to RemoteSigned" -ForegroundColor Green

# Check if PowerShell 7 is installed
$ps7Installed = Test-Path "C:\Program Files\PowerShell\7\pwsh.exe"
if (-not $ps7Installed) {
    Write-Host ""
    Write-Host "Step 3: Installing PowerShell 7..." -ForegroundColor Yellow
    Write-Host "  Downloading installer..." -ForegroundColor Gray

    $ps7Url = "https://github.com/PowerShell/PowerShell/releases/download/v7.4.0/PowerShell-7.4.0-win-x64.msi"
    $ps7Installer = "C:\Installers\PowerShell-7.4.0.msi"

    try {
        Invoke-WebRequest -Uri $ps7Url -OutFile $ps7Installer -UseBasicParsing
        Write-Host "  Installing..." -ForegroundColor Gray
        Start-Process msiexec.exe -ArgumentList "/i `"$ps7Installer`" /quiet /norestart ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ADD_FILE_CONTEXT_MENU_RUNPOWERSHELL=1 ENABLE_PSREMOTING=1 REGISTER_MANIFEST=1" -Wait
        Write-Host "  ✓ PowerShell 7 installed" -ForegroundColor Green
    } catch {
        Write-Host "  WARNING: Could not install PowerShell 7" -ForegroundColor Yellow
        Write-Host "  Error: $_" -ForegroundColor Gray
    }
} else {
    Write-Host ""
    Write-Host "Step 3: PowerShell 7 already installed" -ForegroundColor Green
}

# Install Git
Write-Host ""
Write-Host "Step 4: Installing Git..." -ForegroundColor Yellow
$gitInstalled = Test-Path "C:\Program Files\Git\bin\git.exe"

if (-not $gitInstalled) {
    Write-Host "  Downloading Git..." -ForegroundColor Gray
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstaller = "C:\Installers\Git-2.43.0-64-bit.exe"

    Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller -UseBasicParsing
    Write-Host "  Installing..." -ForegroundColor Gray
    Start-Process $gitInstaller -ArgumentList "/VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS=`"icons,ext\Git\ShellHere,assoc,assoc_sh`"" -Wait
    Write-Host "  ✓ Git installed" -ForegroundColor Green

    # Add Git to PATH
    $env:Path += ";C:\Program Files\Git\bin"
    [System.Environment]::SetEnvironmentVariable("Path", $env:Path, "Machine")
} else {
    Write-Host "  ✓ Git already installed" -ForegroundColor Green
}

# Install Docker Desktop
Write-Host ""
Write-Host "Step 5: Installing Docker Desktop..." -ForegroundColor Yellow
Write-Host "  This is the ONLY service runtime we need!" -ForegroundColor Cyan
Write-Host ""

$dockerInstalled = Test-Path "C:\Program Files\Docker\Docker\Docker Desktop.exe"

if (-not $dockerInstalled) {
    Write-Host "  Downloading Docker Desktop..." -ForegroundColor Gray
    Write-Host "  (This may take 10-15 minutes - file is ~500MB)" -ForegroundColor Gray

    $dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
    $dockerInstaller = "C:\Installers\DockerDesktopInstaller.exe"

    try {
        Invoke-WebRequest -Uri $dockerUrl -OutFile $dockerInstaller -UseBasicParsing
        Write-Host "  Installing Docker Desktop..." -ForegroundColor Gray
        Write-Host "  (This takes 5-10 minutes)" -ForegroundColor Gray

        # Install Docker Desktop
        Start-Process $dockerInstaller -ArgumentList "install --quiet --accept-license" -Wait

        Write-Host "  ✓ Docker Desktop installed" -ForegroundColor Green
        Write-Host ""
        Write-Host "  IMPORTANT: Docker Desktop requires a reboot!" -ForegroundColor Yellow
        Write-Host "  After reboot, Docker Desktop will start automatically" -ForegroundColor Yellow

    } catch {
        Write-Host "  ERROR: Docker Desktop installation failed" -ForegroundColor Red
        Write-Host "  Error: $_" -ForegroundColor Gray
        Write-Host ""
        Write-Host "  Manual installation:" -ForegroundColor Yellow
        Write-Host "  1. Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor White
        Write-Host "  2. Run the installer" -ForegroundColor White
        Write-Host "  3. Restart the VM" -ForegroundColor White
        Write-Host "  4. Continue with deployment scripts" -ForegroundColor White
    }
} else {
    Write-Host "  ✓ Docker Desktop already installed" -ForegroundColor Green

    # Check if Docker is running
    $dockerRunning = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
    if ($dockerRunning) {
        Write-Host "  ✓ Docker Desktop is running" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Docker Desktop is not running" -ForegroundColor Yellow
        Write-Host "  Starting Docker Desktop..." -ForegroundColor Gray
        Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        Write-Host "  Docker Desktop is starting (this takes 1-2 minutes)" -ForegroundColor Gray
    }
}

# Configure Windows Defender exclusions for Docker
Write-Host ""
Write-Host "Step 6: Configuring Windows Defender..." -ForegroundColor Yellow
Write-Host "  Adding Docker directories to exclusions for better performance" -ForegroundColor Gray

try {
    Add-MpPreference -ExclusionPath "C:\ProgramData\Docker" -ErrorAction SilentlyContinue
    Add-MpPreference -ExclusionPath "C:\Program Files\Docker" -ErrorAction SilentlyContinue
    Add-MpPreference -ExclusionPath "C:\DoganSystem" -ErrorAction SilentlyContinue
    Write-Host "  ✓ Defender exclusions configured" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Could not configure Defender exclusions" -ForegroundColor Yellow
}

# Configure Windows Firewall
Write-Host ""
Write-Host "Step 7: Configuring Windows Firewall..." -ForegroundColor Yellow
Write-Host "  Opening ports for Docker services" -ForegroundColor Gray

$firewallRules = @(
    @{Name="Docker-HTTP"; Port=80; Protocol="TCP"},
    @{Name="Docker-HTTPS"; Port=443; Protocol="TCP"},
    @{Name="Docker-Backend"; Port=5000; Protocol="TCP"},
    @{Name="Docker-ERPNext"; Port=8000; Protocol="TCP"},
    @{Name="Docker-Agent"; Port=8001; Protocol="TCP"},
    @{Name="Docker-Webhook"; Port=8003; Protocol="TCP"},
    @{Name="Docker-Monitoring"; Port=8005; Protocol="TCP"},
    @{Name="Docker-Gateway"; Port=8006; Protocol="TCP"},
    @{Name="Docker-TenantAdmin"; Port=8007; Protocol="TCP"}
)

foreach ($rule in $firewallRules) {
    $existing = Get-NetFirewallRule -DisplayName $rule.Name -ErrorAction SilentlyContinue
    if (-not $existing) {
        New-NetFirewallRule -DisplayName $rule.Name -Direction Inbound -Protocol $rule.Protocol -LocalPort $rule.Port -Action Allow -ErrorAction SilentlyContinue | Out-Null
        Write-Host "  Added rule: $($rule.Name) (port $($rule.Port))" -ForegroundColor Gray
    }
}
Write-Host "  ✓ Firewall configured" -ForegroundColor Green

# Disable unnecessary Windows services for better performance
Write-Host ""
Write-Host "Step 8: Optimizing Windows services..." -ForegroundColor Yellow
Write-Host "  Disabling unnecessary services for Docker workload" -ForegroundColor Gray

$servicesToDisable = @(
    "wuauserv",       # Windows Update (manual)
    "BITS",           # Background Intelligent Transfer
    "Spooler"         # Print Spooler (not needed)
)

foreach ($service in $servicesToDisable) {
    try {
        $svc = Get-Service $service -ErrorAction SilentlyContinue
        if ($svc -and $svc.StartType -ne "Disabled") {
            Stop-Service $service -Force -ErrorAction SilentlyContinue
            Set-Service $service -StartupType Manual -ErrorAction SilentlyContinue
            Write-Host "  Disabled: $service" -ForegroundColor Gray
        }
    } catch {
        # Service might not exist
    }
}
Write-Host "  ✓ Services optimized" -ForegroundColor Green

# Configure Docker daemon settings
Write-Host ""
Write-Host "Step 9: Configuring Docker daemon..." -ForegroundColor Yellow

$dockerConfigPath = "$env:ProgramData\Docker\config\daemon.json"
$dockerConfig = @{
    "log-driver" = "json-file"
    "log-opts" = @{
        "max-size" = "10m"
        "max-file" = "3"
    }
    "storage-driver" = "windowsfilter"
    "experimental" = $false
}

$dockerConfigDir = Split-Path $dockerConfigPath -Parent
if (-not (Test-Path $dockerConfigDir)) {
    New-Item -Path $dockerConfigDir -ItemType Directory -Force | Out-Null
}

$dockerConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $dockerConfigPath -Encoding UTF8 -Force
Write-Host "  ✓ Docker daemon configured" -ForegroundColor Green
Write-Host "    (Log rotation: 10MB x 3 files per container)" -ForegroundColor Gray

# Create helper scripts directory
Write-Host ""
Write-Host "Step 10: Setting up helper scripts..." -ForegroundColor Yellow
if (-not (Test-Path "C:\DoganSystem\scripts")) {
    New-Item -Path "C:\DoganSystem\scripts" -ItemType Directory -Force | Out-Null
}
Write-Host "  ✓ Scripts directory ready" -ForegroundColor Green

# System information
Write-Host ""
Write-Host "Step 11: System information..." -ForegroundColor Yellow
$computerInfo = Get-ComputerInfo

Write-Host "  OS: $($computerInfo.WindowsProductName)" -ForegroundColor White
Write-Host "  Version: $($computerInfo.WindowsVersion)" -ForegroundColor White
Write-Host "  RAM: $([math]::Round($computerInfo.CsTotalPhysicalMemory / 1GB, 2)) GB" -ForegroundColor White
Write-Host "  Processors: $($computerInfo.CsNumberOfLogicalProcessors) cores" -ForegroundColor White

$drive = Get-PSDrive -Name C
Write-Host "  C: Drive Free: $([math]::Round($drive.Free / 1GB, 1)) GB" -ForegroundColor White

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " ✓ VM Initialization Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Installed Software:" -ForegroundColor Cyan
Write-Host "  ✓ PowerShell 7" -ForegroundColor White
Write-Host "  ✓ Git" -ForegroundColor White
Write-Host "  ✓ Docker Desktop" -ForegroundColor White
Write-Host ""

Write-Host "NOT Installed (not needed):" -ForegroundColor Cyan
Write-Host "  • IIS (replaced by nginx container)" -ForegroundColor Gray
Write-Host "  • SQL Server (using SQLite in container)" -ForegroundColor Gray
Write-Host "  • Python (runs in containers)" -ForegroundColor Gray
Write-Host "  • Node.js (not needed, frontend pre-built)" -ForegroundColor Gray
Write-Host ""

Write-Host "IMPORTANT: Restart Required!" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Docker Desktop requires a system restart to complete installation." -ForegroundColor White
Write-Host "  After restart:" -ForegroundColor White
Write-Host "  1. Wait for Docker Desktop to start (check system tray)" -ForegroundColor White
Write-Host "  2. Verify Docker: docker --version" -ForegroundColor White
Write-Host "  3. Copy deployment-package.zip from host to C:\\" -ForegroundColor White
Write-Host "  4. Extract: Expand-Archive C:\deployment-package.zip -DestinationPath C:\DoganSystem" -ForegroundColor White
Write-Host "  5. Run: cd C:\DoganSystem; .\4-deploy-secrets.ps1" -ForegroundColor White
Write-Host ""

$response = Read-Host "Restart now? (Y/n)"
if ($response -eq '' -or $response -eq 'Y' -or $response -eq 'y') {
    Write-Host ""
    Write-Host "Restarting in 10 seconds..." -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to cancel" -ForegroundColor Gray
    Start-Sleep -Seconds 10
    Restart-Computer -Force
} else {
    Write-Host ""
    Write-Host "Restart cancelled. Please restart manually before continuing deployment." -ForegroundColor Yellow
    Write-Host "Run: Restart-Computer" -ForegroundColor White
    Write-Host ""
}
