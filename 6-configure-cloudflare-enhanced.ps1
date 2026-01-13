# DoganSystem Cloudflare Tunnel Configuration Script
# Sets up Cloudflare Tunnel to expose Docker services to the internet
# Run this INSIDE the VM after deployment is complete

#Requires -Version 7.0

param(
    [string]$TunnelName = "dogansystem",
    [string]$Domain = "doganconsult.com",
    [string]$ConfigPath = "C:\DoganSystem\cloudflare\config.yml"
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " DoganSystem - Cloudflare Tunnel Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if cloudflared is installed
Write-Host "Step 1: Checking for cloudflared..." -ForegroundColor Yellow
$cloudflaredPath = "C:\Program Files\Cloudflared\cloudflared.exe"

if (-not (Test-Path $cloudflaredPath)) {
    Write-Host "  cloudflared not found, installing..." -ForegroundColor Yellow

    # Create directory
    $installDir = "C:\Program Files\Cloudflared"
    if (-not (Test-Path $installDir)) {
        New-Item -Path $installDir -ItemType Directory -Force | Out-Null
    }

    # Download cloudflared
    Write-Host "  Downloading cloudflared..." -ForegroundColor Gray
    $downloadUrl = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    Invoke-WebRequest -Uri $downloadUrl -OutFile $cloudflaredPath -UseBasicParsing

    # Add to PATH
    $env:Path += ";$installDir"
    [System.Environment]::SetEnvironmentVariable("Path", $env:Path, "Machine")

    Write-Host "  ✓ cloudflared installed" -ForegroundColor Green
} else {
    Write-Host "  ✓ cloudflared found" -ForegroundColor Green
    # Ensure it's in PATH
    if ($env:Path -notlike "*Cloudflared*") {
        $env:Path += ";C:\Program Files\Cloudflared"
    }
}

# Verify Docker is running
Write-Host ""
Write-Host "Step 2: Verifying Docker services..." -ForegroundColor Yellow
try {
    docker ps > $null 2>&1
    if ($?) {
        Write-Host "  ✓ Docker is running" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: Docker is not running!" -ForegroundColor Red
        Write-Host "  Please start Docker Desktop and try again" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "  ERROR: Could not connect to Docker" -ForegroundColor Red
    exit 1
}

# Check nginx container
$nginxRunning = docker ps --filter "name=dogansystem-nginx" --format "{{.Names}}" 2>$null
if ($nginxRunning) {
    Write-Host "  ✓ Nginx container is running" -ForegroundColor Green
} else {
    Write-Host "  WARNING: Nginx container not found" -ForegroundColor Yellow
    Write-Host "  Make sure deployment (script 5) completed successfully" -ForegroundColor Gray
}

# Login to Cloudflare
Write-Host ""
Write-Host "Step 3: Cloudflare authentication..." -ForegroundColor Yellow
Write-Host "  This will open a browser window for login" -ForegroundColor Gray
Write-Host ""

$credentialsPath = "$env:USERPROFILE\.cloudflared"
if (-not (Test-Path $credentialsPath)) {
    New-Item -Path $credentialsPath -ItemType Directory -Force | Out-Null
}

# Check if already logged in
$certPath = Join-Path $credentialsPath "cert.pem"
if (Test-Path $certPath) {
    Write-Host "  ✓ Already authenticated with Cloudflare" -ForegroundColor Green
} else {
    Write-Host "  Please login to Cloudflare in the browser window..." -ForegroundColor Cyan
    & $cloudflaredPath tunnel login

    if ($?) {
        Write-Host "  ✓ Authentication successful" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: Authentication failed" -ForegroundColor Red
        exit 1
    }
}

# Create or update tunnel
Write-Host ""
Write-Host "Step 4: Setting up tunnel..." -ForegroundColor Yellow

# Check if tunnel exists
$existingTunnel = & $cloudflaredPath tunnel list | Select-String $TunnelName

if ($existingTunnel) {
    Write-Host "  Tunnel '$TunnelName' already exists" -ForegroundColor Gray
    $response = Read-Host "  Delete and recreate? (y/N)"

    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "  Deleting existing tunnel..." -ForegroundColor Yellow
        & $cloudflaredPath tunnel delete $TunnelName
        $createTunnel = $true
    } else {
        Write-Host "  Using existing tunnel" -ForegroundColor Gray
        $createTunnel = $false
    }
} else {
    $createTunnel = $true
}

if ($createTunnel) {
    Write-Host "  Creating tunnel '$TunnelName'..." -ForegroundColor Gray
    & $cloudflaredPath tunnel create $TunnelName

    if ($?) {
        Write-Host "  ✓ Tunnel created" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: Failed to create tunnel" -ForegroundColor Red
        exit 1
    }
}

# Get tunnel ID
$tunnelInfo = & $cloudflaredPath tunnel info $TunnelName 2>$null
$tunnelId = ($tunnelInfo | Select-String "ID: (.+)").Matches.Groups[1].Value.Trim()

Write-Host "  Tunnel ID: $tunnelId" -ForegroundColor White

# Create config file if it doesn't exist
Write-Host ""
Write-Host "Step 5: Configuring tunnel..." -ForegroundColor Yellow

$configDir = Split-Path $ConfigPath -Parent
if (-not (Test-Path $configDir)) {
    New-Item -Path $configDir -ItemType Directory -Force | Out-Null
}

# Find credentials file
$credFile = Get-ChildItem "$env:USERPROFILE\.cloudflared" -Filter "*.json" | Select-Object -First 1

if ($credFile) {
    Write-Host "  Found credentials: $($credFile.Name)" -ForegroundColor Gray

    # Update config with correct credentials path
    if (Test-Path $ConfigPath) {
        $config = Get-Content $ConfigPath -Raw
        $config = $config -replace "credentials-file:.*", "credentials-file: $($credFile.FullName)"
        $config = $config -replace "tunnel:.*", "tunnel: $tunnelId"
        $config | Out-File -FilePath $ConfigPath -Encoding UTF8 -Force
        Write-Host "  ✓ Config updated: $ConfigPath" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: Config template not found: $ConfigPath" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  ERROR: Credentials file not found" -ForegroundColor Red
    exit 1
}

# Configure DNS routes
Write-Host ""
Write-Host "Step 6: Configuring DNS routes..." -ForegroundColor Yellow
Write-Host "  This will create DNS records in your Cloudflare account" -ForegroundColor Gray
Write-Host ""

$subdomains = @(
    $Domain,
    "www",
    "api",
    "ai",
    "ds",
    "login"
)

foreach ($subdomain in $subdomains) {
    $hostname = if ($subdomain -eq $Domain) { $Domain } else { "$subdomain.$Domain" }

    Write-Host "  Configuring $hostname..." -NoNewline

    # Route DNS to tunnel
    & $cloudflaredPath tunnel route dns $TunnelName $hostname 2>&1 | Out-Null

    if ($?) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " (may already exist)" -ForegroundColor Gray
    }
}

Write-Host "  ✓ DNS routes configured" -ForegroundColor Green

# Install as Windows Service
Write-Host ""
Write-Host "Step 7: Installing as Windows Service..." -ForegroundColor Yellow

$serviceName = "cloudflared"
$existingService = Get-Service $serviceName -ErrorAction SilentlyContinue

if ($existingService) {
    Write-Host "  Service already exists, reinstalling..." -ForegroundColor Gray
    Stop-Service $serviceName -Force -ErrorAction SilentlyContinue
    & $cloudflaredPath service uninstall
}

Write-Host "  Installing service..." -ForegroundColor Gray
& $cloudflaredPath service install

if ($?) {
    Write-Host "  ✓ Service installed" -ForegroundColor Green

    # Start service
    Write-Host "  Starting service..." -ForegroundColor Gray
    Start-Service $serviceName

    Start-Sleep -Seconds 3

    $service = Get-Service $serviceName
    if ($service.Status -eq "Running") {
        Write-Host "  ✓ Service is running" -ForegroundColor Green
    } else {
        Write-Host "  WARNING: Service may not have started correctly" -ForegroundColor Yellow
        Write-Host "  Status: $($service.Status)" -ForegroundColor Gray
    }
} else {
    Write-Host "  ERROR: Failed to install service" -ForegroundColor Red
    exit 1
}

# Test connectivity
Write-Host ""
Write-Host "Step 8: Testing tunnel connectivity..." -ForegroundColor Yellow
Write-Host "  Waiting for tunnel to establish..." -ForegroundColor Gray

Start-Sleep -Seconds 5

# Check tunnel status
$tunnelStatus = & $cloudflaredPath tunnel info $TunnelName 2>$null

if ($tunnelStatus -match "Conn" -or $tunnelStatus -match "Registered") {
    Write-Host "  ✓ Tunnel is connected" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Tunnel status unclear, check logs" -ForegroundColor Yellow
}

# Final summary
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " ✓ Cloudflare Tunnel Configured!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Tunnel Information:" -ForegroundColor Cyan
Write-Host "  Name: $TunnelName" -ForegroundColor White
Write-Host "  ID: $tunnelId" -ForegroundColor White
Write-Host "  Config: $ConfigPath" -ForegroundColor White
Write-Host "  Service: $serviceName (Running as Windows Service)" -ForegroundColor White
Write-Host ""

Write-Host "Configured Domains:" -ForegroundColor Cyan
Write-Host "  • https://$Domain" -ForegroundColor White
Write-Host "  • https://www.$Domain" -ForegroundColor White
Write-Host "  • https://api.$Domain" -ForegroundColor White
Write-Host "  • https://ai.$Domain" -ForegroundColor White
Write-Host "  • https://ds.$Domain" -ForegroundColor White
Write-Host "  • https://login.$Domain" -ForegroundColor White
Write-Host ""

Write-Host "All domains point to: http://host.docker.internal:80 (nginx container)" -ForegroundColor Gray
Write-Host ""

Write-Host "IMPORTANT: DNS Propagation" -ForegroundColor Yellow
Write-Host "  • DNS changes may take 5-15 minutes to propagate globally" -ForegroundColor White
Write-Host "  • You can test local resolution: nslookup $Domain" -ForegroundColor White
Write-Host "  • Check Cloudflare dashboard for DNS records" -ForegroundColor White
Write-Host ""

Write-Host "Useful Commands:" -ForegroundColor Cyan
Write-Host "  • View tunnel status: cloudflared tunnel info $TunnelName" -ForegroundColor White
Write-Host "  • View service status: Get-Service cloudflared" -ForegroundColor White
Write-Host "  • Restart service: Restart-Service cloudflared" -ForegroundColor White
Write-Host "  • View logs: Get-EventLog -LogName Application -Source cloudflared" -ForegroundColor White
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Wait 5-10 minutes for DNS propagation" -ForegroundColor White
Write-Host "  2. Test: curl https://$Domain" -ForegroundColor White
Write-Host "  3. Run: .\7-validate-deployment-enhanced.ps1 (comprehensive testing)" -ForegroundColor White
Write-Host "  4. Run: .\8-setup-monitoring.ps1 (configure backups and alerts)" -ForegroundColor White
Write-Host ""
