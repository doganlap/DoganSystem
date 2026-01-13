# Start Cloudflare Tunnel with Docker
# Run this after deployment to expose your services to the internet
#
# IMPORTANT: Replace YOUR_TOKEN_HERE with your actual tunnel token from Cloudflare

param(
    [Parameter(Mandatory=$false)]
    [string]$Token = "YOUR_TOKEN_HERE"
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Cloudflare Tunnel - Docker Deployment" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if token is provided
if ($Token -eq "YOUR_TOKEN_HERE") {
    Write-Host "ERROR: Please provide your Cloudflare Tunnel token!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\start-cloudflare-tunnel.ps1 -Token `"eyJhIjoiNj...your-full-token...`"" -ForegroundColor White
    Write-Host ""
    Write-Host "Get your token from:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://dash.cloudflare.com/" -ForegroundColor White
    Write-Host "  2. Select your domain: doganconsult.com" -ForegroundColor White
    Write-Host "  3. Go to: Zero Trust → Networks → Tunnels" -ForegroundColor White
    Write-Host "  4. Click on your tunnel → Configure" -ForegroundColor White
    Write-Host "  5. Copy the full token (starts with eyJh...)" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "Step 1: Checking Docker..." -ForegroundColor Yellow
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

Write-Host ""
Write-Host "Step 2: Checking if tunnel is already running..." -ForegroundColor Yellow
$existingTunnel = docker ps --filter "name=cloudflared-tunnel" --format "{{.Names}}" 2>$null

if ($existingTunnel) {
    Write-Host "  Tunnel container already exists, stopping it..." -ForegroundColor Gray
    docker stop cloudflared-tunnel 2>$null
    docker rm cloudflared-tunnel 2>$null
    Write-Host "  ✓ Old container removed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 3: Pulling latest Cloudflare image..." -ForegroundColor Yellow
docker pull cloudflare/cloudflared:latest

Write-Host ""
Write-Host "Step 4: Starting Cloudflare Tunnel..." -ForegroundColor Yellow
Write-Host "  Container name: cloudflared-tunnel" -ForegroundColor Gray
Write-Host "  Restart policy: unless-stopped" -ForegroundColor Gray
Write-Host "  Network mode: host (to access localhost services)" -ForegroundColor Gray
Write-Host ""

# Run tunnel in Docker with host network to access localhost services
docker run -d `
    --name cloudflared-tunnel `
    --restart unless-stopped `
    --network host `
    cloudflare/cloudflared:latest `
    tunnel --no-autoupdate run --token $Token

if ($?) {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host " ✓ Cloudflare Tunnel Started!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""

    Write-Host "Container Information:" -ForegroundColor Cyan
    Write-Host "  Name: cloudflared-tunnel" -ForegroundColor White
    Write-Host "  Status: Running in background" -ForegroundColor White
    Write-Host "  Restart: Automatic (unless stopped manually)" -ForegroundColor White
    Write-Host "  Network: Host mode (can access all localhost ports)" -ForegroundColor White
    Write-Host ""

    Write-Host "Your Domains (via Cloudflare):" -ForegroundColor Cyan
    Write-Host "  • https://doganconsult.com" -ForegroundColor White
    Write-Host "  • https://www.doganconsult.com" -ForegroundColor White
    Write-Host "  • https://api.doganconsult.com" -ForegroundColor White
    Write-Host "  • https://ai.doganconsult.com" -ForegroundColor White
    Write-Host "  • https://ds.doganconsult.com" -ForegroundColor White
    Write-Host "  • https://login.doganconsult.com" -ForegroundColor White
    Write-Host ""

    Write-Host "Port Allocation:" -ForegroundColor Cyan
    Write-Host "  ✅ No conflicts with GrcMvc (ports 5100, 5432, 6379)" -ForegroundColor White
    Write-Host "  ✅ DoganSystem uses internal Docker network only" -ForegroundColor White
    Write-Host "  ✅ External access via Cloudflare Tunnel (encrypted)" -ForegroundColor White
    Write-Host ""

    Write-Host "Useful Commands:" -ForegroundColor Cyan
    Write-Host "  View logs:        docker logs -f cloudflared-tunnel" -ForegroundColor White
    Write-Host "  Check status:     docker ps | findstr cloudflared" -ForegroundColor White
    Write-Host "  Stop tunnel:      docker stop cloudflared-tunnel" -ForegroundColor White
    Write-Host "  Start tunnel:     docker start cloudflared-tunnel" -ForegroundColor White
    Write-Host "  Remove tunnel:    docker rm -f cloudflared-tunnel" -ForegroundColor White
    Write-Host ""

    Write-Host "Testing Connection:" -ForegroundColor Cyan
    Write-Host "  Wait 30-60 seconds for DNS propagation, then try:" -ForegroundColor White
    Write-Host "  curl https://doganconsult.com" -ForegroundColor Gray
    Write-Host ""

    Write-Host "View Tunnel Logs:" -ForegroundColor Yellow
    Write-Host "  Showing last 20 lines..." -ForegroundColor Gray
    Write-Host ""
    Start-Sleep -Seconds 3
    docker logs --tail 20 cloudflared-tunnel
    Write-Host ""

} else {
    Write-Host ""
    Write-Host "ERROR: Failed to start tunnel!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible issues:" -ForegroundColor Yellow
    Write-Host "  1. Invalid token (check if you copied the full token)" -ForegroundColor White
    Write-Host "  2. Docker not running properly" -ForegroundColor White
    Write-Host "  3. Network connectivity issues" -ForegroundColor White
    Write-Host ""
    Write-Host "Try running with verbose output:" -ForegroundColor Cyan
    Write-Host "  docker run cloudflare/cloudflared:latest tunnel run --token YOUR_TOKEN" -ForegroundColor Gray
    Write-Host ""
    exit 1
}
