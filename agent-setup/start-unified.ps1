# Start Unified DoganSystem
# Multi-Tenant + Autonomous + Employee Agents + KSA Localization

Write-Host "===========================================" -ForegroundColor Green
Write-Host "Starting Unified DoganSystem" -ForegroundColor Green
Write-Host "Multi-Tenant + Autonomous + Employee Agents + KSA" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

# Activate virtual environment
if (Test-Path "venv") {
    .\venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "⚠ Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
}

# Check environment file
if (-not (Test-Path ".env")) {
    Write-Host "⚠ .env file not found. Copying from env.example..." -ForegroundColor Yellow
    Copy-Item env.example .env
    Write-Host "⚠ Please edit .env file with your configuration" -ForegroundColor Yellow
    exit 1
}

# Check Python dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
python -c "import requests, anthropic, fastapi, sqlite3" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Create directories
Write-Host "Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "tenant_databases" | Out-Null
New-Item -ItemType Directory -Force -Path ".cursor" | Out-Null

# Start unified system
Write-Host ""
Write-Host "Starting unified orchestrator..." -ForegroundColor Green
Write-Host "This will start:" -ForegroundColor Yellow
Write-Host "  - Multi-tenant system" -ForegroundColor Cyan
Write-Host "  - Autonomous workflows" -ForegroundColor Cyan
Write-Host "  - Employee agents" -ForegroundColor Cyan
Write-Host "  - KSA localization" -ForegroundColor Cyan
Write-Host "  - Self-healing system" -ForegroundColor Cyan
Write-Host "  - Email processing" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python unified-orchestrator.py
