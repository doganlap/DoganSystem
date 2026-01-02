# Fix NuGet Restore - Update Package Versions Script
# This script updates all ABP package versions to the latest stable (8.3.4 or latest)

Write-Host "Fixing NuGet Package Versions..." -ForegroundColor Cyan
Write-Host ""

# Get all .csproj files
$csprojFiles = Get-ChildItem -Recurse -Filter "*.csproj"

$updatedCount = 0
foreach ($file in $csprojFiles) {
    $content = Get-Content $file.FullName -Raw
    $originalContent = $content
    
    # Update all ABP packages from 8.0.0 to 8.3.4 (latest stable)
    $content = $content -replace 'Version="8\.0\.0"', 'Version="8.3.4"'
    
    if ($content -ne $originalContent) {
        Set-Content $file.FullName -Value $content -NoNewline
        Write-Host "Updated: $($file.Name)" -ForegroundColor Green
        $updatedCount++
    }
}

Write-Host ""
Write-Host "Updated $updatedCount project files" -ForegroundColor Green
Write-Host ""
Write-Host "Now run: dotnet restore DoganSystem.sln" -ForegroundColor Yellow
