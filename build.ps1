# DoganSystem Build Script for Windows
# Usage: .\build.ps1 [Release|Debug]

param(
    [string]$Configuration = "Release"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DoganSystem Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check .NET SDK
Write-Host "Checking .NET SDK..." -ForegroundColor Yellow
$dotnetVersion = dotnet --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: .NET SDK not found. Please install .NET 8.0 SDK." -ForegroundColor Red
    exit 1
}
Write-Host "✓ .NET SDK $dotnetVersion found" -ForegroundColor Green
Write-Host ""

# Restore packages
Write-Host "Restoring NuGet packages..." -ForegroundColor Yellow
dotnet restore DoganSystem.sln
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Package restore failed." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Packages restored" -ForegroundColor Green
Write-Host ""

# Build solution
Write-Host "Building solution ($Configuration)..." -ForegroundColor Yellow
dotnet build DoganSystem.sln --configuration $Configuration --no-restore
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Build successful" -ForegroundColor Green
Write-Host ""

# Publish web application
Write-Host "Publishing web application..." -ForegroundColor Yellow
$publishPath = "src\DoganSystem.Web.Mvc\publish"
if (Test-Path $publishPath) {
    Remove-Item $publishPath -Recurse -Force
}
dotnet publish "src\DoganSystem.Web.Mvc\DoganSystem.Web.Mvc.csproj" `
    --configuration $Configuration `
    --output $publishPath `
    --no-build
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Publish failed." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Published to: $publishPath" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update connection string in appsettings.json" -ForegroundColor White
Write-Host "2. Run database migrations:" -ForegroundColor White
Write-Host "   cd src\DoganSystem.EntityFrameworkCore" -ForegroundColor Gray
Write-Host "   dotnet ef migrations add Initial --startup-project ..\DoganSystem.Web.Mvc" -ForegroundColor Gray
Write-Host "   dotnet ef database update --startup-project ..\DoganSystem.Web.Mvc" -ForegroundColor Gray
Write-Host "3. Run the application:" -ForegroundColor White
Write-Host "   cd src\DoganSystem.Web.Mvc" -ForegroundColor Gray
Write-Host "   dotnet run" -ForegroundColor Gray
Write-Host ""
