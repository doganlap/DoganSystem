# Phase 6: Setup Cloudflare Tunnel
# Run this INSIDE the VM after frontend deployment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Cloudflare Tunnel" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if cloudflared exists
if (-not (Test-Path "C:\Program Files\Cloudflared\cloudflared.exe")) {
    Write-Host "ERROR: Cloudflared not found!" -ForegroundColor Red
    Write-Host "Please run 3-install-software.ps1 first" -ForegroundColor Yellow
    exit 1
}

$env:Path += ";C:\Program Files\Cloudflared"

# Login to Cloudflare
Write-Host "Step 1: Login to Cloudflare..." -ForegroundColor Yellow
Write-Host "  A browser window will open for authentication" -ForegroundColor Cyan
Write-Host "  Login with your Cloudflare account" -ForegroundColor Cyan
pause

cloudflared tunnel login

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Login failed!" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Logged in successfully" -ForegroundColor Green

# Create tunnel
Write-Host ""
Write-Host "Step 2: Creating tunnel..." -ForegroundColor Yellow
cloudflared tunnel create dogansystem

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Tunnel creation failed!" -ForegroundColor Red
    exit 1
}

# Get tunnel ID
$tunnelInfo = cloudflared tunnel list | Select-String "dogansystem"
$tunnelId = ($tunnelInfo -split '\s+')[0]
Write-Host "  ✓ Tunnel created: $tunnelId" -ForegroundColor Green

# Create config file
Write-Host ""
Write-Host "Step 3: Creating tunnel configuration..." -ForegroundColor Yellow
New-Item -Path "C:\Program Files\Cloudflared" -ItemType Directory -Force | Out-Null

$config = @"
tunnel: dogansystem
credentials-file: C:\Users\Administrator\.cloudflared\$tunnelId.json

ingress:
  # Main website
  - hostname: doganconsult.com
    service: http://localhost:3000

  - hostname: www.doganconsult.com
    service: http://localhost:3000

  # API Backend
  - hostname: api.doganconsult.com
    service: http://localhost:5000

  # AI Services
  - hostname: ai.doganconsult.com
    service: http://localhost:8006

  # Dashboard
  - hostname: ds.doganconsult.com
    service: http://localhost:8005

  # Login/Auth
  - hostname: login.doganconsult.com
    service: http://localhost:5000

  # Catch-all
  - service: http_status:404
"@

$config | Out-File -FilePath "C:\Program Files\Cloudflared\config.yml" -Encoding UTF8
Write-Host "  ✓ Configuration created" -ForegroundColor Green

# Route DNS
Write-Host ""
Write-Host "Step 4: Routing DNS to tunnel..." -ForegroundColor Yellow
$domains = @(
    "doganconsult.com",
    "www.doganconsult.com",
    "api.doganconsult.com",
    "ai.doganconsult.com",
    "ds.doganconsult.com",
    "login.doganconsult.com"
)

foreach ($domain in $domains) {
    Write-Host "  Routing $domain..." -ForegroundColor Cyan
    cloudflared tunnel route dns dogansystem $domain
}
Write-Host "  ✓ DNS routes configured" -ForegroundColor Green

# Install as service
Write-Host ""
Write-Host "Step 5: Installing as Windows Service..." -ForegroundColor Yellow
cloudflared service install
Start-Service cloudflared
Set-Service cloudflared -StartupType Automatic
Write-Host "  ✓ Service installed and started" -ForegroundColor Green

# Test tunnel
Write-Host ""
Write-Host "Step 6: Testing tunnel..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
cloudflared tunnel info dogansystem
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "Cloudflare Tunnel Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your domains are now connected:" -ForegroundColor Cyan
Write-Host "  • https://doganconsult.com" -ForegroundColor White
Write-Host "  • https://www.doganconsult.com" -ForegroundColor White
Write-Host "  • https://api.doganconsult.com" -ForegroundColor White
Write-Host "  • https://ai.doganconsult.com" -ForegroundColor White
Write-Host "  • https://ds.doganconsult.com" -ForegroundColor White
Write-Host "  • https://login.doganconsult.com" -ForegroundColor White
Write-Host ""
Write-Host "NOTE: DNS propagation may take 5-15 minutes" -ForegroundColor Yellow
Write-Host ""
