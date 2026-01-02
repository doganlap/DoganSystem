# DoganSystem Deployment Script for Windows
# Usage: .\deploy.ps1 [local|iis|docker]

param(
    [string]$Target = "local",
    [string]$Configuration = "Release"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DoganSystem Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Build first
Write-Host "Building application..." -ForegroundColor Yellow
& .\build.ps1 -Configuration $Configuration
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed. Cannot deploy." -ForegroundColor Red
    exit 1
}
Write-Host ""

switch ($Target.ToLower()) {
    "local" {
        Write-Host "Deploying locally..." -ForegroundColor Yellow
        Write-Host "Starting application..." -ForegroundColor Green
        cd src\DoganSystem.Web.Mvc
        dotnet run
    }
    "iis" {
        Write-Host "Deploying to IIS..." -ForegroundColor Yellow
        $iisPath = "C:\inetpub\wwwroot\DoganSystem"
        $publishPath = "src\DoganSystem.Web.Mvc\publish"
        
        if (-not (Test-Path "C:\inetpub\wwwroot")) {
            Write-Host "ERROR: IIS not installed or wwwroot not found." -ForegroundColor Red
            exit 1
        }
        
        Write-Host "Copying files to IIS directory..." -ForegroundColor Yellow
        if (Test-Path $iisPath) {
            Remove-Item $iisPath -Recurse -Force
        }
        Copy-Item -Path "$publishPath\*" -Destination $iisPath -Recurse -Force
        Write-Host "✓ Files copied to $iisPath" -ForegroundColor Green
        Write-Host ""
        Write-Host "IMPORTANT: Configure IIS Application Pool and Website manually." -ForegroundColor Yellow
        Write-Host "1. Create Application Pool: DoganSystemAppPool (No Managed Code)" -ForegroundColor White
        Write-Host "2. Create Website pointing to: $iisPath" -ForegroundColor White
        Write-Host "3. Update connection string in web.config" -ForegroundColor White
    }
    "docker" {
        Write-Host "Building Docker image..." -ForegroundColor Yellow
        docker build -t dogansystem:latest .
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: Docker build failed." -ForegroundColor Red
            exit 1
        }
        Write-Host "✓ Docker image built" -ForegroundColor Green
        Write-Host ""
        Write-Host "To run container:" -ForegroundColor Yellow
        Write-Host "docker run -d -p 8080:80 -e ConnectionStrings__Default='your-connection-string' --name dogansystem dogansystem:latest" -ForegroundColor White
    }
    default {
        Write-Host "ERROR: Unknown deployment target: $Target" -ForegroundColor Red
        Write-Host "Valid targets: local, iis, docker" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
