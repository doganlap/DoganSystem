# DoganSystem Pre-Flight Check
# Validates all prerequisites before deployment
# Run this FIRST before starting deployment

param(
    [switch]$Verbose
)

$ErrorActionPreference = "SilentlyContinue"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " DoganSystem Pre-Flight Check" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$checks = @()
$warnings = @()

# Helper function to add check result
function Add-CheckResult {
    param($Name, $Pass, $Value = "", $Required = $true)
    $script:checks += [PSCustomObject]@{
        Name = $Name
        Pass = $Pass
        Value = $value
        Required = $Required
    }
}

# Helper function to add warning
function Add-Warning {
    param($Message)
    $script:warnings += $Message
}

Write-Host "Checking system prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check 1: Windows Version
Write-Host "  [1/15] Checking Windows version..." -NoNewline
$os = Get-CimInstance Win32_OperatingSystem
$isProOrEnterprise = $os.Caption -match "Pro|Enterprise|Server"
$winVersion = $os.Version
Add-CheckResult -Name "Windows Pro/Enterprise" -Pass $isProOrEnterprise -Value $os.Caption
if ($isProOrEnterprise) { Write-Host " OK" -ForegroundColor Green } else { Write-Host " FAIL" -ForegroundColor Red }

# Check 2: Hyper-V Feature
Write-Host "  [2/15] Checking Hyper-V..." -NoNewline
try {
    $hypervFeature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All
    $hypervEnabled = $hypervFeature.State -eq "Enabled"
} catch {
    $hypervEnabled = $false
}
Add-CheckResult -Name "Hyper-V Enabled" -Pass $hypervEnabled -Value $(if($hypervEnabled){"Enabled"}else{"Not Enabled"})
if ($hypervEnabled) { Write-Host " OK" -ForegroundColor Green } else { Write-Host " FAIL" -ForegroundColor Red }

# Check 3: Hyper-V Service Running
Write-Host "  [3/15] Checking Hyper-V services..." -NoNewline
$hypervRunning = $false
if ($hypervEnabled) {
    $vmms = Get-Service -Name vmms -ErrorAction SilentlyContinue
    $hypervRunning = $vmms -and $vmms.Status -eq "Running"
}
Add-CheckResult -Name "Hyper-V Service Running" -Pass $hypervRunning -Value $(if($hypervRunning){"Running"}else{"Stopped"})
if ($hypervRunning) { Write-Host " OK" -ForegroundColor Green } else { Write-Host " FAIL" -ForegroundColor Red }

# Check 4: RAM
Write-Host "  [4/15] Checking RAM..." -NoNewline
$ram = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
$ramPass = $ram -ge 40
Add-CheckResult -Name "RAM (40GB+ required)" -Pass $ramPass -Value "$ram GB"
if ($ramPass) {
    Write-Host " OK ($ram GB)" -ForegroundColor Green
} else {
    Write-Host " WARN ($ram GB)" -ForegroundColor Yellow
    Add-Warning "Recommended: 40GB+ RAM for optimal VM performance (24GB for VM + 16GB for host)"
}

# Check 5: Disk Space
Write-Host "  [5/15] Checking disk space..." -NoNewline
$drive = Get-PSDrive -Name C
$freeSpaceGB = [math]::Round($drive.Free / 1GB, 1)
$diskPass = $freeSpaceGB -ge 250
Add-CheckResult -Name "Disk Space (250GB+ required)" -Pass $diskPass -Value "$freeSpaceGB GB free"
if ($diskPass) {
    Write-Host " OK ($freeSpaceGB GB free)" -ForegroundColor Green
} else {
    Write-Host " FAIL ($freeSpaceGB GB free)" -ForegroundColor Red
}

# Check 6: CPU Cores
Write-Host "  [6/15] Checking CPU cores..." -NoNewline
$cores = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors
$cpuPass = $cores -ge 10
Add-CheckResult -Name "CPU Cores (10+ recommended)" -Pass $cpuPass -Value "$cores cores" -Required $false
if ($cpuPass) {
    Write-Host " OK ($cores cores)" -ForegroundColor Green
} elseif ($cores -ge 8) {
    Write-Host " WARN ($cores cores)" -ForegroundColor Yellow
    Add-Warning "Recommended: 10+ CPU cores. You have $cores which may work but VM will have reduced performance."
} else {
    Write-Host " FAIL ($cores cores)" -ForegroundColor Red
}

# Check 7: PowerShell Version
Write-Host "  [7/15] Checking PowerShell version..." -NoNewline
$psVersion = $PSVersionTable.PSVersion
$psPass = $psVersion.Major -ge 7
Add-CheckResult -Name "PowerShell 7+" -Pass $psPass -Value "v$($psVersion.Major).$($psVersion.Minor)"
if ($psPass) {
    Write-Host " OK (v$($psVersion.Major).$($psVersion.Minor))" -ForegroundColor Green
} else {
    Write-Host " FAIL (v$($psVersion.Major).$($psVersion.Minor))" -ForegroundColor Red
    Add-Warning "Install PowerShell 7+: https://aka.ms/powershell"
}

# Check 8: Windows Server 2022 ISO
Write-Host "  [8/15] Checking Windows Server ISO..." -NoNewline
$isoPath = "C:\ISOs\WindowsServer2022.iso"
$isoExists = Test-Path $isoPath
$isoSize = if ($isoExists) { [math]::Round((Get-Item $isoPath).Length / 1GB, 2) } else { 0 }
Add-CheckResult -Name "Windows Server 2022 ISO" -Pass $isoExists -Value $(if($isoExists){"Found ($isoSize GB)"}else{"Not found"})
if ($isoExists) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " WARN" -ForegroundColor Yellow
    Add-Warning "Windows Server 2022 ISO not found at: $isoPath"
    Add-Warning "Download from: https://www.microsoft.com/en-us/evalcenter/download-windows-server-2022"
}

# Check 9: docker-compose.production.yml
Write-Host "  [9/15] Checking docker-compose file..." -NoNewline
$composeFile = "d:\DoganSystem\docker-compose.production.yml"
$composeExists = Test-Path $composeFile
Add-CheckResult -Name "docker-compose.production.yml" -Pass $composeExists -Value $(if($composeExists){"Found"}else{"Missing"})
if ($composeExists) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
}

# Check 10: Dockerfile (Backend)
Write-Host " [10/15] Checking Dockerfile (backend)..." -NoNewline
$dockerfileBackend = "d:\DoganSystem\Dockerfile"
$dockerfileBackendExists = Test-Path $dockerfileBackend
Add-CheckResult -Name "Dockerfile (backend)" -Pass $dockerfileBackendExists -Value $(if($dockerfileBackendExists){"Found"}else{"Missing"})
if ($dockerfileBackendExists) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
}

# Check 11: Dockerfile (Python services)
Write-Host " [11/15] Checking Dockerfile (Python)..." -NoNewline
$dockerfilePython = "d:\DoganSystem\agent-setup\Dockerfile"
$dockerfilePythonExists = Test-Path $dockerfilePython
Add-CheckResult -Name "Dockerfile (Python)" -Pass $dockerfilePythonExists -Value $(if($dockerfilePythonExists){"Found"}else{"Missing"})
if ($dockerfilePythonExists) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
}

# Check 12: .NET Source Code
Write-Host " [12/15] Checking .NET source code..." -NoNewline
$dotnetSource = "d:\DoganSystem\src\DoganSystem.Web.Mvc\DoganSystem.Web.Mvc.csproj"
$dotnetSourceExists = Test-Path $dotnetSource
Add-CheckResult -Name ".NET Source Code" -Pass $dotnetSourceExists -Value $(if($dotnetSourceExists){"Found"}else{"Missing"})
if ($dotnetSourceExists) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
}

# Check 13: Python Source Code
Write-Host " [13/15] Checking Python source code..." -NoNewline
$pythonSource = "d:\DoganSystem\agent-setup"
$pythonFiles = @("api-gateway.py", "api-server.py", "tenant-admin-api.py", "monitoring-dashboard.py", "webhook-receiver.py")
$pythonSourceExists = Test-Path $pythonSource
$pythonFilesExist = $true
if ($pythonSourceExists) {
    foreach ($file in $pythonFiles) {
        if (-not (Test-Path (Join-Path $pythonSource $file))) {
            $pythonFilesExist = $false
            break
        }
    }
}
Add-CheckResult -Name "Python Source Code" -Pass ($pythonSourceExists -and $pythonFilesExist) -Value $(if($pythonSourceExists -and $pythonFilesExist){"Found"}else{"Missing files"})
if ($pythonSourceExists -and $pythonFilesExist) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " WARN" -ForegroundColor Yellow
    Add-Warning "Some Python service files may be missing in agent-setup/"
}

# Check 14: Internet Connectivity
Write-Host " [14/15] Checking internet connectivity..." -NoNewline
$internetPass = $false
try {
    $response = Invoke-WebRequest -Uri "https://www.google.com" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    $internetPass = $response.StatusCode -eq 200
} catch {
    $internetPass = $false
}
Add-CheckResult -Name "Internet Connectivity" -Pass $internetPass -Value $(if($internetPass){"Connected"}else{"No connection"})
if ($internetPass) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
}

# Check 15: Execution Policy
Write-Host " [15/15] Checking PowerShell execution policy..." -NoNewline
$execPolicy = Get-ExecutionPolicy
$execPolicyPass = $execPolicy -ne "Restricted"
Add-CheckResult -Name "Execution Policy" -Pass $execPolicyPass -Value $execPolicy -Required $false
if ($execPolicyPass) {
    Write-Host " OK ($execPolicy)" -ForegroundColor Green
} else {
    Write-Host " WARN ($execPolicy)" -ForegroundColor Yellow
    Add-Warning "Run: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"
}

# Display Results
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Results Summary" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$passCount = ($checks | Where-Object { $_.Pass -eq $true }).Count
$failCount = ($checks | Where-Object { $_.Pass -eq $false -and $_.Required -eq $true }).Count
$warnCount = ($checks | Where-Object { $_.Pass -eq $false -and $_.Required -eq $false }).Count
$totalRequired = ($checks | Where-Object { $_.Required -eq $true }).Count

# Display detailed results in verbose mode
if ($Verbose) {
    foreach ($check in $checks) {
        $icon = if ($check.Pass) { "✓" } elseif ($check.Required) { "✗" } else { "⚠" }
        $color = if ($check.Pass) { "Green" } elseif ($check.Required) { "Red" } else { "Yellow" }
        Write-Host "$icon $($check.Name): $($check.Value)" -ForegroundColor $color
    }
    Write-Host ""
}

Write-Host "Passed:   $passCount / $($checks.Count)" -ForegroundColor Green
if ($failCount -gt 0) {
    Write-Host "Failed:   $failCount (blocking)" -ForegroundColor Red
}
if ($warnCount -gt 0) {
    Write-Host "Warnings: $warnCount (non-blocking)" -ForegroundColor Yellow
}

# Display warnings
if ($warnings.Count -gt 0) {
    Write-Host ""
    Write-Host "Warnings and Recommendations:" -ForegroundColor Yellow
    Write-Host ""
    foreach ($warning in $warnings) {
        Write-Host "  ⚠ $warning" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan

# Final verdict
if ($failCount -eq 0) {
    Write-Host " ✓ ALL CRITICAL CHECKS PASSED!" -ForegroundColor Green
    Write-Host " Ready to proceed with deployment." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Run: .\1-prepare-host.ps1" -ForegroundColor White
    Write-Host "  2. Enter your Claude API key and SMTP credentials when prompted" -ForegroundColor White
    Write-Host "  3. Follow the deployment guide" -ForegroundColor White
    Write-Host ""
    exit 0
} else {
    Write-Host " ✗ SOME CRITICAL CHECKS FAILED" -ForegroundColor Red
    Write-Host " Please fix the issues above before proceeding." -ForegroundColor Red
    Write-Host ""
    Write-Host "Common fixes:" -ForegroundColor Cyan
    if (-not $hypervEnabled) {
        Write-Host "  - Enable Hyper-V: Run 1-enable-hyperv.bat" -ForegroundColor White
    }
    if ($freeSpaceGB -lt 250) {
        Write-Host "  - Free up disk space (need $([math]::Round(250-$freeSpaceGB,0))GB more)" -ForegroundColor White
    }
    if (-not $psPass) {
        Write-Host "  - Install PowerShell 7+: winget install Microsoft.PowerShell" -ForegroundColor White
    }
    if (-not $internetPass) {
        Write-Host "  - Check your internet connection" -ForegroundColor White
    }
    Write-Host ""
    exit 1
}
