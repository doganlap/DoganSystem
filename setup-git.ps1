# Git Setup Script for DoganSystem
# Run: .\setup-git.ps1

Write-Host "===========================================" -ForegroundColor Green
Write-Host "DoganSystem Git Setup" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

# Check if git is installed
Write-Host "Checking Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✓ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git not found. Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Initialize git repository
Write-Host "Initializing Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
} else {
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

Write-Host ""

# Add all files
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added" -ForegroundColor Green

Write-Host ""

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "Creating initial commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: Complete DoganSystem implementation

- ABP MVC Application Shell with Entity Framework
- Tenant Management Module
- ERPNext Management Module
- Multi-Agent Orchestrator Module
- Subscription Management Module
- Python Services Integration
- Complete REST API endpoints
- Web Dashboard UI
- Full documentation"
    Write-Host "✓ Initial commit created" -ForegroundColor Green
} else {
    Write-Host "No changes to commit" -ForegroundColor Yellow
}

Write-Host ""

# Check if remote exists
Write-Host "Checking remote repository..." -ForegroundColor Yellow
$remote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Remote already configured: $remote" -ForegroundColor Green
    $updateRemote = Read-Host "Update remote? (y/n)"
    if ($updateRemote -eq "y") {
        git remote remove origin
        git remote add origin https://github.com/doganlap/DoganSystem.git
        Write-Host "✓ Remote updated" -ForegroundColor Green
    }
} else {
    Write-Host "Adding remote repository..." -ForegroundColor Yellow
    git remote add origin https://github.com/doganlap/DoganSystem.git
    Write-Host "✓ Remote added: https://github.com/doganlap/DoganSystem.git" -ForegroundColor Green
}

Write-Host ""

# Rename branch to main
Write-Host "Setting branch to main..." -ForegroundColor Yellow
git branch -M main
Write-Host "✓ Branch set to main" -ForegroundColor Green

Write-Host ""
Write-Host "===========================================" -ForegroundColor Green
Write-Host "Ready to Push!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Push to GitHub:" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "2. If authentication is required:" -ForegroundColor Cyan
Write-Host "   - Use Personal Access Token (not password)" -ForegroundColor White
Write-Host "   - Generate at: https://github.com/settings/tokens" -ForegroundColor White
Write-Host ""
Write-Host "3. Or use SSH:" -ForegroundColor Cyan
Write-Host "   git remote set-url origin git@github.com:doganlap/DoganSystem.git" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
