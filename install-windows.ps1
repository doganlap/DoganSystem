# ERPNext v16 Windows Installation Script
# Run this script in PowerShell as Administrator

Write-Host "ERPNext v16 Installation Script for Windows" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: Please run this script as Administrator" -ForegroundColor Red
    exit 1
}

# Check Python
Write-Host "`nChecking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
    $pythonMajor = (python -c "import sys; print(sys.version_info.major)" 2>&1)
    $pythonMinor = (python -c "import sys; print(sys.version_info.minor)" 2>&1)
    if ($pythonMajor -lt 3 -or ($pythonMajor -eq 3 -and $pythonMinor -lt 10)) {
        Write-Host "ERROR: Python 3.10+ required. Current: $pythonVersion" -ForegroundColor Red
        Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "ERROR: Python not found. Please install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "`nChecking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "Found: $nodeVersion" -ForegroundColor Green
    $nodeMajor = (node --version).Substring(1).Split('.')[0]
    if ([int]$nodeMajor -lt 18) {
        Write-Host "WARNING: Node.js 18+ recommended. Current: $nodeVersion" -ForegroundColor Yellow
    }
} catch {
    Write-Host "ERROR: Node.js not found. Please install Node.js 18+ from nodejs.org" -ForegroundColor Red
    exit 1
}

# Check Git
Write-Host "`nChecking Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "Found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git not found. Please install Git from git-scm.com" -ForegroundColor Red
    exit 1
}

# Install bench
Write-Host "`nInstalling Frappe Bench CLI..." -ForegroundColor Yellow
pip install frappe-bench
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install frappe-bench" -ForegroundColor Red
    exit 1
}
Write-Host "Bench installed successfully!" -ForegroundColor Green

# Check bench installation
Write-Host "`nVerifying bench installation..." -ForegroundColor Yellow
try {
    $benchVersion = bench --version
    Write-Host "Found: $benchVersion" -ForegroundColor Green
} catch {
    Write-Host "WARNING: bench command not found. You may need to restart your terminal." -ForegroundColor Yellow
    Write-Host "Or add Python Scripts to PATH: %APPDATA%\Python\Python3XX\Scripts" -ForegroundColor Yellow
}

Write-Host "`n===========================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Navigate to your desired directory (e.g., D:\)" -ForegroundColor White
Write-Host "2. Run: bench init --frappe-branch version-16 frappe-bench" -ForegroundColor White
Write-Host "3. Run: cd frappe-bench" -ForegroundColor White
Write-Host "4. Run: bench get-app erpnext --branch version-16" -ForegroundColor White
Write-Host "5. Run: bench new-site your-site-name.local" -ForegroundColor White
Write-Host "6. Run: bench --site your-site-name.local install-app erpnext" -ForegroundColor White
Write-Host "7. Run: bench start" -ForegroundColor White
Write-Host "`nFor detailed instructions, see README.md" -ForegroundColor Cyan
