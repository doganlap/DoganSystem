# Quick Push to GitHub
# Run: .\push-to-github.ps1

Write-Host "Pushing to GitHub..." -ForegroundColor Green
Write-Host ""

# Disable pager
$env:GIT_PAGER = "cat"

# Push
git push -u origin main

Write-Host ""
Write-Host "Done! Check: https://github.com/doganlap/DoganSystem" -ForegroundColor Green
