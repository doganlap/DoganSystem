# PowerShell script to apply EF Core migration to database
# Run from solution root: .\apply-migration.ps1

Write-Host "Applying EF Core migration to database..." -ForegroundColor Green

$projectPath = "src\DoganSystem.EntityFrameworkCore"
$startupProject = "src\DoganSystem.Web.Mvc"
$context = "DoganSystemDbContext"

# Check connection string
Write-Host "Checking connection string..." -ForegroundColor Cyan
$appsettingsPath = Join-Path $startupProject "appsettings.json"
if (Test-Path $appsettingsPath) {
    $appsettings = Get-Content $appsettingsPath | ConvertFrom-Json
    $connString = $appsettings.ConnectionStrings.Default
    Write-Host "Connection: $connString" -ForegroundColor White
} else {
    Write-Host "Warning: appsettings.json not found" -ForegroundColor Yellow
}

# Build the project first
Write-Host "Building project..." -ForegroundColor Cyan
dotnet build $startupProject
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed. Please fix errors before applying migration." -ForegroundColor Red
    exit 1
}

# Apply migration
Write-Host "Applying migration to database..." -ForegroundColor Cyan
Write-Host "WARNING: This will modify your database!" -ForegroundColor Yellow
$response = Read-Host "Continue? (y/n)"
if ($response -ne "y") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

dotnet ef database update `
    --project $projectPath `
    --startup-project $startupProject `
    --context $context

if ($LASTEXITCODE -eq 0) {
    Write-Host "Migration applied successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Database is ready. You can now run the application." -ForegroundColor Green
} else {
    Write-Host "Migration application failed. Check errors above." -ForegroundColor Red
    exit 1
}
