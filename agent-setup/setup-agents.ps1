# ERPNext Multi-Agent System Setup for Windows
# Run in PowerShell

Write-Host "===========================================" -ForegroundColor Green
Write-Host "ERPNext Multi-Agent System Setup" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python is required" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "Please edit .env file with your configuration" -ForegroundColor Yellow
}

# Create directories
New-Item -ItemType Directory -Force -Path logs | Out-Null
New-Item -ItemType Directory -Force -Path data | Out-Null

Write-Host ""
Write-Host "===========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your ERPNext and Claude API credentials" -ForegroundColor White
Write-Host "2. Generate ERPNext API key:" -ForegroundColor White
Write-Host "   - Login to ERPNext" -ForegroundColor White
Write-Host "   - Go to Settings > Integrations > API Keys" -ForegroundColor White
Write-Host "   - Create new API key" -ForegroundColor White
Write-Host "3. Start the API server:" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   python api-server.py" -ForegroundColor White
Write-Host ""
