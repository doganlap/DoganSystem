# Check ERPNext Installation Status
# Run: .\check-erpnext-status.ps1

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "ERPNext Installation Status Check" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

$status = @{
    BenchInstalled = $false
    BenchFound = $false
    ERPNextInstalled = $false
    SiteCreated = $false
    Running = $false
}

# Check if bench CLI is installed
Write-Host "1. Checking Bench CLI..." -ForegroundColor Yellow
try {
    $benchVersion = bench --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Bench CLI installed: $benchVersion" -ForegroundColor Green
        $status.BenchInstalled = $true
    } else {
        Write-Host "   ✗ Bench CLI not found" -ForegroundColor Red
        Write-Host "   → Install with: pip install frappe-bench" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ✗ Bench CLI not found" -ForegroundColor Red
    Write-Host "   → Install with: pip install frappe-bench" -ForegroundColor Yellow
}

# Check for frappe-bench directory
Write-Host "`n2. Checking for Frappe Bench directory..." -ForegroundColor Yellow
$possibleLocations = @(
    "$env:USERPROFILE\frappe-bench",
    "D:\frappe-bench",
    "C:\frappe-bench",
    ".\frappe-bench"
)

$benchPath = $null
foreach ($location in $possibleLocations) {
    if (Test-Path $location) {
        $benchPath = $location
        Write-Host "   ✓ Found bench at: $location" -ForegroundColor Green
        $status.BenchFound = $true
        break
    }
}

if (-not $benchPath) {
    Write-Host "   ✗ Frappe Bench directory not found" -ForegroundColor Red
    Write-Host "   → Create with: bench init --frappe-branch version-16 frappe-bench" -ForegroundColor Yellow
}

# Check if ERPNext app is installed
if ($benchPath) {
    Write-Host "`n3. Checking ERPNext installation..." -ForegroundColor Yellow
    $erpnextPath = Join-Path $benchPath "apps\erpnext"
    if (Test-Path $erpnextPath) {
        Write-Host "   ✓ ERPNext app found" -ForegroundColor Green
        $status.ERPNextInstalled = $true
    } else {
        Write-Host "   ✗ ERPNext app not found" -ForegroundColor Red
        Write-Host "   → Install with: bench get-app erpnext --branch version-16" -ForegroundColor Yellow
    }
    
    # Check for sites
    Write-Host "`n4. Checking for sites..." -ForegroundColor Yellow
    $sitesPath = Join-Path $benchPath "sites"
    if (Test-Path $sitesPath) {
        $sites = Get-ChildItem -Path $sitesPath -Directory -ErrorAction SilentlyContinue
        if ($sites) {
            Write-Host "   ✓ Found $($sites.Count) site(s):" -ForegroundColor Green
            foreach ($site in $sites) {
                Write-Host "     - $($site.Name)" -ForegroundColor Cyan
            }
            $status.SiteCreated = $true
        } else {
            Write-Host "   ✗ No sites found" -ForegroundColor Red
            Write-Host "   → Create with: bench new-site your-site.local" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ✗ Sites directory not found" -ForegroundColor Red
    }
}

# Check if ERPNext is running
Write-Host "`n5. Checking if ERPNext is running..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "   ✓ ERPNext is running on http://localhost:8000" -ForegroundColor Green
        $status.Running = $true
    }
} catch {
    Write-Host "   ✗ ERPNext is not running" -ForegroundColor Red
    Write-Host "   → Start with: bench start" -ForegroundColor Yellow
}

# Summary
Write-Host "`n===========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

if ($status.BenchInstalled -and $status.BenchFound -and $status.ERPNextInstalled -and $status.SiteCreated -and $status.Running) {
    Write-Host "✓ ERPNext is FULLY SETUP and RUNNING!" -ForegroundColor Green
} elseif ($status.BenchInstalled -and $status.BenchFound -and $status.ERPNextInstalled -and $status.SiteCreated) {
    Write-Host "⚠ ERPNext is INSTALLED but NOT RUNNING" -ForegroundColor Yellow
    Write-Host "  → Run: bench start" -ForegroundColor Yellow
} elseif ($status.BenchInstalled -and $status.BenchFound) {
    Write-Host "⚠ ERPNext is PARTIALLY SETUP" -ForegroundColor Yellow
    Write-Host "  → Complete installation steps" -ForegroundColor Yellow
} else {
    Write-Host "✗ ERPNext is NOT INSTALLED" -ForegroundColor Red
    Write-Host "  → Follow installation guide in README.md" -ForegroundColor Yellow
}

Write-Host ""
