# PowerShell script to run the DoganSystem application
# Run from solution root: .\run-app.ps1

Write-Host "Starting DoganSystem Application..." -ForegroundColor Green

$projectPath = "src\DoganSystem.Web.Mvc"

# Check if database exists
Write-Host "Checking database connection..." -ForegroundColor Cyan
$appsettingsPath = Join-Path $projectPath "appsettings.json"
if (Test-Path $appsettingsPath) {
    $appsettings = Get-Content $appsettingsPath | ConvertFrom-Json
    $connString = $appsettings.ConnectionStrings.Default
    Write-Host "Connection: $connString" -ForegroundColor White
}

# Build the project
Write-Host "Building project..." -ForegroundColor Cyan
dotnet build $projectPath --configuration Release
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed. Please fix errors before running." -ForegroundColor Red
    exit 1
}

# Run the application
Write-Host ""
Write-Host "Starting application..." -ForegroundColor Green
Write-Host "Application will be available at:" -ForegroundColor Yellow
Write-Host "  - HTTP:  http://localhost:5000" -ForegroundColor White
Write-Host "  - HTTPS: https://localhost:5001" -ForegroundColor White
Write-Host "  - Swagger: https://localhost:5001/swagger" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

cd $projectPath
dotnet run --configuration Release
