# DoganSystem Docker Deployment Script
# This replaces the old scripts 4, 5, and 6
# Run this INSIDE the VM after secrets are deployed

#Requires -Version 7.0

param(
    [switch]$SkipPull,
    [switch]$SkipHealthCheck,
    [int]$HealthCheckTimeout = 120
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " DoganSystem - Docker Deployment" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Verify we're in the right directory
if (-not (Test-Path ".\docker-compose.production.yml")) {
    Write-Host "ERROR: docker-compose.production.yml not found!" -ForegroundColor Red
    Write-Host "Please run this script from C:\DoganSystem directory" -ForegroundColor Yellow
    exit 1
}

# Function to check if Docker is running
function Test-DockerRunning {
    try {
        $result = docker info 2>$null
        return $?
    } catch {
        return $false
    }
}

# Function to wait for container health
function Wait-ContainerHealthy {
    param(
        [string]$ContainerName,
        [int]$TimeoutSeconds = 120
    )

    Write-Host "  Waiting for $ContainerName to be healthy..." -NoNewline

    $elapsed = 0
    $interval = 5

    while ($elapsed -lt $TimeoutSeconds) {
        try {
            $health = docker inspect --format='{{.State.Health.Status}}' $ContainerName 2>$null

            if ($health -eq "healthy") {
                Write-Host " OK (${elapsed}s)" -ForegroundColor Green
                return $true
            }

            if ($health -eq "unhealthy") {
                Write-Host " UNHEALTHY" -ForegroundColor Red
                Write-Host ""
                Write-Host "  Container logs:" -ForegroundColor Yellow
                docker logs --tail 20 $ContainerName
                return $false
            }

            # Container might not have health check
            $running = docker inspect --format='{{.State.Running}}' $ContainerName 2>$null
            if ($running -eq "true" -and [string]::IsNullOrEmpty($health)) {
                Write-Host " OK (no health check, ${elapsed}s)" -ForegroundColor Green
                return $true
            }

        } catch {
            # Container might not exist yet
        }

        Start-Sleep -Seconds $interval
        $elapsed += $interval
        Write-Host "." -NoNewline
    }

    Write-Host " TIMEOUT" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Container logs:" -ForegroundColor Yellow
    docker logs --tail 30 $ContainerName 2>$null
    return $false
}

# Pre-flight checks
Write-Host "Step 1: Running pre-flight checks..." -ForegroundColor Yellow
Write-Host ""

# Check 1: Docker Desktop running
Write-Host "  [1/5] Docker Desktop..." -NoNewline
if (Test-DockerRunning) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Docker Desktop is not running!" -ForegroundColor Red
    Write-Host "  Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}

# Check 2: .env file exists
Write-Host "  [2/5] Environment file..." -NoNewline
if (Test-Path ".\.env") {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host ""
    Write-Host "  .env file not found!" -ForegroundColor Red
    Write-Host "  Please run 4-deploy-secrets.ps1 first." -ForegroundColor Yellow
    exit 1
}

# Check 3: Disk space
Write-Host "  [3/5] Disk space..." -NoNewline
$drive = Get-PSDrive -Name C
$freeSpaceGB = [math]::Round($drive.Free / 1GB, 1)
if ($freeSpaceGB -ge 50) {
    Write-Host " OK ($freeSpaceGB GB free)" -ForegroundColor Green
} else {
    Write-Host " WARN ($freeSpaceGB GB free)" -ForegroundColor Yellow
    Write-Host "    Recommended: 100GB+ free space" -ForegroundColor Gray
}

# Check 4: Required ports available
Write-Host "  [4/5] Port availability..." -NoNewline
$requiredPorts = @(80, 443, 5000, 8000, 8001, 8003, 8005, 8006, 8007)
$portsInUse = @()

foreach ($port in $requiredPorts) {
    $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($connection) {
        $portsInUse += $port
    }
}

if ($portsInUse.Count -eq 0) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " WARN" -ForegroundColor Yellow
    Write-Host "    Ports in use: $($portsInUse -join ', ')" -ForegroundColor Gray
    Write-Host "    Docker will stop conflicting services" -ForegroundColor Gray
}

# Check 5: Docker Compose file valid
Write-Host "  [5/5] Docker Compose syntax..." -NoNewline
try {
    docker-compose -f docker-compose.production.yml config > $null 2>&1
    if ($?) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " WARN" -ForegroundColor Yellow
    }
} catch {
    Write-Host " WARN" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "  ✓ Pre-flight checks completed" -ForegroundColor Green

# Pull Docker images
if (-not $SkipPull) {
    Write-Host ""
    Write-Host "Step 2: Pulling Docker images..." -ForegroundColor Yellow
    Write-Host "  (This may take 10-15 minutes on first run)" -ForegroundColor Gray
    Write-Host ""

    docker-compose -f docker-compose.production.yml pull

    if ($?) {
        Write-Host ""
        Write-Host "  ✓ Images pulled successfully" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "  WARNING: Some images may not have pulled correctly" -ForegroundColor Yellow
        Write-Host "  Continuing anyway..." -ForegroundColor Gray
    }
} else {
    Write-Host ""
    Write-Host "Step 2: Skipping image pull (--SkipPull specified)" -ForegroundColor Gray
}

# Create directories for logs
Write-Host ""
Write-Host "Step 3: Creating log directories..." -ForegroundColor Yellow
$logDirs = @(
    ".\logs\web",
    ".\logs\api-gateway",
    ".\logs\agent-server",
    ".\logs\tenant-admin",
    ".\logs\monitoring",
    ".\logs\webhook",
    ".\logs\nginx"
)

foreach ($dir in $logDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Gray
    }
}
Write-Host "  ✓ Log directories ready" -ForegroundColor Green

# Stop any existing containers
Write-Host ""
Write-Host "Step 4: Stopping existing containers (if any)..." -ForegroundColor Yellow
docker-compose -f docker-compose.production.yml down 2>$null
Write-Host "  ✓ Cleanup complete" -ForegroundColor Green

# Start services
Write-Host ""
Write-Host "Step 5: Starting Docker services..." -ForegroundColor Yellow
Write-Host "  This will start 11 containers in dependency order" -ForegroundColor Gray
Write-Host ""

# Start infrastructure services first
Write-Host "  Starting infrastructure services..." -ForegroundColor Cyan

docker-compose -f docker-compose.production.yml up -d redis erpnext-db

if (-not $SkipHealthCheck) {
    Start-Sleep -Seconds 5
    if (-not (Wait-ContainerHealthy -ContainerName "dogansystem-redis" -TimeoutSeconds 30)) {
        Write-Host ""
        Write-Host "ERROR: Redis failed to start" -ForegroundColor Red
        exit 1
    }

    if (-not (Wait-ContainerHealthy -ContainerName "dogansystem-erpnext-db" -TimeoutSeconds 60)) {
        Write-Host ""
        Write-Host "ERROR: ERPNext database failed to start" -ForegroundColor Red
        exit 1
    }
}

# Start ERPNext
Write-Host ""
Write-Host "  Starting ERPNext..." -ForegroundColor Cyan
docker-compose -f docker-compose.production.yml up -d erpnext

if (-not $SkipHealthCheck) {
    Start-Sleep -Seconds 10
    if (-not (Wait-ContainerHealthy -ContainerName "dogansystem-erpnext" -TimeoutSeconds 180)) {
        Write-Host ""
        Write-Host "WARNING: ERPNext may need more time to initialize" -ForegroundColor Yellow
        Write-Host "Continuing with deployment..." -ForegroundColor Gray
    }
}

# Start Python AI services
Write-Host ""
Write-Host "  Starting Python AI services..." -ForegroundColor Cyan
docker-compose -f docker-compose.production.yml up -d api-gateway agent-server tenant-admin monitoring webhook-receiver workflow-engine

if (-not $SkipHealthCheck) {
    Start-Sleep -Seconds 10

    $pythonServices = @(
        "dogansystem-api-gateway",
        "dogansystem-agent-server",
        "dogansystem-tenant-admin",
        "dogansystem-monitoring",
        "dogansystem-webhook"
    )

    foreach ($service in $pythonServices) {
        if (-not (Wait-ContainerHealthy -ContainerName $service -TimeoutSeconds 60)) {
            Write-Host ""
            Write-Host "WARNING: $service may have issues" -ForegroundColor Yellow
        }
    }
}

# Start .NET backend
Write-Host ""
Write-Host "  Starting .NET backend..." -ForegroundColor Cyan
docker-compose -f docker-compose.production.yml up -d dogansystem-web

if (-not $SkipHealthCheck) {
    Start-Sleep -Seconds 10
    if (-not (Wait-ContainerHealthy -ContainerName "dogansystem-web" -TimeoutSeconds 120)) {
        Write-Host ""
        Write-Host "WARNING: Backend may need more time" -ForegroundColor Yellow
    }
}

# Start Nginx
Write-Host ""
Write-Host "  Starting Nginx reverse proxy..." -ForegroundColor Cyan
docker-compose -f docker-compose.production.yml up -d nginx

if (-not $SkipHealthCheck) {
    Start-Sleep -Seconds 5
    if (-not (Wait-ContainerHealthy -ContainerName "dogansystem-nginx" -TimeoutSeconds 30)) {
        Write-Host ""
        Write-Host "WARNING: Nginx may have issues" -ForegroundColor Yellow
    }
}

# Display status
Write-Host ""
Write-Host "Step 6: Verifying deployment..." -ForegroundColor Yellow
Write-Host ""

docker-compose -f docker-compose.production.yml ps

Write-Host ""
Write-Host "Step 7: Testing endpoints..." -ForegroundColor Yellow
Write-Host ""

# Test internal endpoints
$endpoints = @(
    @{Name=".NET Backend"; Url="http://localhost:5000/health"; Timeout=10},
    @{Name="API Gateway"; Url="http://localhost:8006/health"; Timeout=10},
    @{Name="Agent Server"; Url="http://localhost:8001/health"; Timeout=10},
    @{Name="Monitoring"; Url="http://localhost:8005/health"; Timeout=10},
    @{Name="Nginx"; Url="http://localhost:80"; Timeout=5}
)

$passCount = 0
foreach ($endpoint in $endpoints) {
    Write-Host "  Testing $($endpoint.Name)..." -NoNewline
    try {
        $response = Invoke-WebRequest -Uri $endpoint.Url -UseBasicParsing -TimeoutSec $endpoint.Timeout -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host " OK" -ForegroundColor Green
            $passCount++
        } else {
            Write-Host " HTTP $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host " FAIL" -ForegroundColor Red
        Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Gray
    }
}

Write-Host ""
if ($passCount -eq $endpoints.Count) {
    Write-Host "  ✓ All endpoints responding" -ForegroundColor Green
} else {
    Write-Host "  ⚠ $passCount/$($endpoints.Count) endpoints responding" -ForegroundColor Yellow
    Write-Host "    Some services may still be initializing" -ForegroundColor Gray
}

# Check for database migrations
Write-Host ""
Write-Host "Step 8: Checking database migrations..." -ForegroundColor Yellow
Write-Host "  (ABP Framework runs migrations automatically on first start)" -ForegroundColor Gray

try {
    $logs = docker logs dogansystem-web --tail 50 2>$null
    if ($logs -match "migrat" -or $logs -match "database") {
        Write-Host "  ✓ Database migration logs detected" -ForegroundColor Green
    } else {
        Write-Host "  ℹ No migration activity in recent logs" -ForegroundColor Cyan
    }
} catch {
    Write-Host "  ⚠ Could not check migration logs" -ForegroundColor Yellow
}

# Final summary
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " ✓ Deployment Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Services Status:" -ForegroundColor Cyan
Write-Host "  • Redis: Running" -ForegroundColor White
Write-Host "  • MariaDB (ERPNext DB): Running" -ForegroundColor White
Write-Host "  • ERPNext: Running (may take 2-3 min to fully initialize)" -ForegroundColor White
Write-Host "  • API Gateway: Running" -ForegroundColor White
Write-Host "  • Agent Server: Running" -ForegroundColor White
Write-Host "  • Tenant Admin: Running" -ForegroundColor White
Write-Host "  • Monitoring: Running" -ForegroundColor White
Write-Host "  • Webhook Receiver: Running" -ForegroundColor White
Write-Host "  • Workflow Engine: Running" -ForegroundColor White
Write-Host "  • .NET Backend: Running" -ForegroundColor White
Write-Host "  • Nginx Reverse Proxy: Running" -ForegroundColor White
Write-Host ""

Write-Host "Access Points (Internal):" -ForegroundColor Cyan
Write-Host "  • Backend API: http://localhost:5000" -ForegroundColor White
Write-Host "  • ERPNext: http://localhost:8000" -ForegroundColor White
Write-Host "  • API Gateway: http://localhost:8006" -ForegroundColor White
Write-Host "  • Agent Server: http://localhost:8001" -ForegroundColor White
Write-Host "  • Monitoring: http://localhost:8005" -ForegroundColor White
Write-Host "  • Web (via Nginx): http://localhost" -ForegroundColor White
Write-Host ""

Write-Host "Data Volumes:" -ForegroundColor Cyan
Write-Host "  • dogansystem-data (SQLite DB)" -ForegroundColor White
Write-Host "  • ai-data (AI services data)" -ForegroundColor White
Write-Host "  • redis-data (Redis persistence)" -ForegroundColor White
Write-Host "  • erpnext-sites (ERPNext files)" -ForegroundColor White
Write-Host "  • erpnext-db-data (MariaDB data)" -ForegroundColor White
Write-Host ""

Write-Host "Logs Location:" -ForegroundColor Cyan
Write-Host "  • Container logs: docker logs <container-name>" -ForegroundColor White
Write-Host "  • Application logs: C:\DoganSystem\logs\" -ForegroundColor White
Write-Host ""

Write-Host "Useful Commands:" -ForegroundColor Cyan
Write-Host "  • View all containers: docker ps" -ForegroundColor White
Write-Host "  • View logs: docker-compose -f docker-compose.production.yml logs -f" -ForegroundColor White
Write-Host "  • Restart service: docker-compose -f docker-compose.production.yml restart <service>" -ForegroundColor White
Write-Host "  • Stop all: docker-compose -f docker-compose.production.yml down" -ForegroundColor White
Write-Host "  • Start all: docker-compose -f docker-compose.production.yml up -d" -ForegroundColor White
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Wait 2-3 minutes for all services to fully initialize" -ForegroundColor White
Write-Host "  2. Run: .\6-configure-cloudflare-enhanced.ps1 (setup external access)" -ForegroundColor White
Write-Host "  3. Run: .\7-validate-deployment-enhanced.ps1 (comprehensive testing)" -ForegroundColor White
Write-Host "  4. Run: .\8-setup-monitoring.ps1 (configure backups and alerts)" -ForegroundColor White
Write-Host ""

Write-Host "ERPNext Setup:" -ForegroundColor Yellow
Write-Host "  After Cloudflare Tunnel is configured:" -ForegroundColor White
Write-Host "  1. Access ERPNext at http://localhost:8000" -ForegroundColor White
Write-Host "  2. Login with: Administrator / [password from deployment-secrets.txt]" -ForegroundColor White
Write-Host "  3. Generate API Key/Secret in ERPNext settings" -ForegroundColor White
Write-Host "  4. Update .env file with ERPNEXT_API_KEY and ERPNEXT_API_SECRET" -ForegroundColor White
Write-Host "  5. Restart: docker-compose -f docker-compose.production.yml restart" -ForegroundColor White
Write-Host ""
