# PowerShell script to create EF Core migration
# Run from solution root: .\create-migration.ps1

Write-Host "Creating EF Core migration..." -ForegroundColor Green

$projectPath = "src\DoganSystem.EntityFrameworkCore"
$startupProject = "src\DoganSystem.Web.Mvc"
$context = "DoganSystemDbContext"
$migrationName = "Initial"

# Check if migration already exists
$migrationsPath = Join-Path $projectPath "Migrations"
if (Test-Path $migrationsPath) {
    $existingMigrations = Get-ChildItem -Path $migrationsPath -Filter "*_*.cs" -Exclude "*ModelSnapshot.cs"
    if ($existingMigrations.Count -gt 0) {
        Write-Host "Warning: Existing migrations found. Use a different name or remove existing migrations first." -ForegroundColor Yellow
        Write-Host "Existing migrations:" -ForegroundColor Yellow
        $existingMigrations | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Yellow }
        $response = Read-Host "Continue anyway? (y/n)"
        if ($response -ne "y") {
            exit
        }
    }
}

# Build the project first
Write-Host "Building project..." -ForegroundColor Cyan
dotnet build $startupProject
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed. Please fix errors before creating migration." -ForegroundColor Red
    exit 1
}

# Create migration
Write-Host "Creating migration '$migrationName'..." -ForegroundColor Cyan
dotnet ef migrations add $migrationName `
    --project $projectPath `
    --startup-project $startupProject `
    --context $context

if ($LASTEXITCODE -eq 0) {
    Write-Host "Migration created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Review the migration file in: $migrationsPath" -ForegroundColor White
    Write-Host "2. Apply migration: dotnet ef database update --project $projectPath --startup-project $startupProject --context $context" -ForegroundColor White
} else {
    Write-Host "Migration creation failed. Check errors above." -ForegroundColor Red
    exit 1
}
