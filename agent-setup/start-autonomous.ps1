# Start Autonomous Workplace System
# Zero Human Intervention Mode

Write-Host "===========================================" -ForegroundColor Green
Write-Host "Starting DoganSystem Autonomous Workplace" -ForegroundColor Green
Write-Host "Zero Human Intervention Mode" -ForegroundColor Green
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
python -c "import requests, anthropic, fastapi" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Start autonomous system
Write-Host ""
Write-Host "Starting autonomous orchestrator..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python autonomous-orchestrator.py
