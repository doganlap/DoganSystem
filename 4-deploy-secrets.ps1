# DoganSystem Secrets Deployment Script
# Decrypts and deploys secrets inside the VM
# Run this INSIDE the VM after copying the deployment package

#Requires -Version 7.0

param(
    [string]$WorkingDir = "C:\DoganSystem",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " DoganSystem - Secrets Deployment" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Ensure we're in the right directory
if (-not (Test-Path $WorkingDir)) {
    Write-Host "ERROR: Working directory not found: $WorkingDir" -ForegroundColor Red
    Write-Host "Please extract deployment-package.zip first" -ForegroundColor Yellow
    exit 1
}

Set-Location $WorkingDir

# Function to decrypt string using DPAPI
function Unprotect-String {
    param([string]$EncryptedText)

    try {
        $bytes = [Convert]::FromBase64String($EncryptedText)
        $decrypted = [System.Security.Cryptography.ProtectedData]::Unprotect(
            $bytes,
            $null,
            [System.Security.Cryptography.DataProtectionScope]::CurrentUser
        )
        return [System.Text.Encoding]::UTF8.GetString($decrypted)
    } catch {
        Write-Host "ERROR: Failed to decrypt data" -ForegroundColor Red
        Write-Host "This file can only be decrypted on the PC where it was created" -ForegroundColor Yellow
        throw
    }
}

Write-Host "Step 1: Checking for encrypted secrets file..." -ForegroundColor Yellow
$encryptedPath = ".\.env.production.encrypted"

if (-not (Test-Path $encryptedPath)) {
    Write-Host "  ERROR: Encrypted file not found: $encryptedPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Please ensure deployment-package.zip was copied and extracted" -ForegroundColor Yellow
    exit 1
}
Write-Host "  ✓ Found encrypted secrets file" -ForegroundColor Green

Write-Host ""
Write-Host "Step 2: Decrypting secrets..." -ForegroundColor Yellow
Write-Host "  (This uses Windows Data Protection API)" -ForegroundColor Gray

try {
    $encryptedContent = Get-Content $encryptedPath -Raw
    $decryptedContent = Unprotect-String -EncryptedText $encryptedContent
    Write-Host "  ✓ Secrets decrypted successfully" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Decryption failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "  This usually means:" -ForegroundColor Yellow
    Write-Host "  1. The file was encrypted on a different computer" -ForegroundColor White
    Write-Host "  2. The file was encrypted by a different user account" -ForegroundColor White
    Write-Host "  3. The file is corrupted" -ForegroundColor White
    Write-Host ""
    Write-Host "  Solution: Re-run 1-prepare-host.ps1 on the host machine" -ForegroundColor Cyan
    exit 1
}

Write-Host ""
Write-Host "Step 3: Validating decrypted content..." -ForegroundColor Yellow

# Check for required variables
$requiredVars = @(
    "CLAUDE_API_KEY",
    "REDIS_PASSWORD",
    "MYSQL_ROOT_PASSWORD",
    "MYSQL_PASSWORD",
    "JWT_SECRET_KEY",
    "SMTP_SERVER",
    "SMTP_USERNAME",
    "SMTP_PASSWORD"
)

$missingVars = @()
foreach ($var in $requiredVars) {
    if ($decryptedContent -notmatch "$var=.+") {
        $missingVars += $var
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "  ERROR: Missing required variables:" -ForegroundColor Red
    foreach ($var in $missingVars) {
        Write-Host "    - $var" -ForegroundColor Yellow
    }
    exit 1
}

Write-Host "  ✓ All required variables present" -ForegroundColor Green

# Check if .env already exists
$envPath = ".\.env"
if (Test-Path $envPath) {
    if ($Force) {
        Write-Host ""
        Write-Host "  Existing .env file will be replaced" -ForegroundColor Yellow
        # Backup existing
        $backupPath = ".\.env.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item $envPath $backupPath
        Write-Host "  Backup created: $backupPath" -ForegroundColor Gray
    } else {
        Write-Host ""
        Write-Host "  WARNING: .env file already exists!" -ForegroundColor Yellow
        $response = Read-Host "  Replace it? (y/N)"
        if ($response -ne 'y' -and $response -ne 'Y') {
            Write-Host "  Aborted by user" -ForegroundColor Yellow
            exit 0
        }
        # Backup existing
        $backupPath = ".\.env.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item $envPath $backupPath
        Write-Host "  Backup created: $backupPath" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Step 4: Creating .env file..." -ForegroundColor Yellow
$decryptedContent | Out-File -FilePath $envPath -Encoding UTF8 -NoNewline
Write-Host "  ✓ Created: $envPath" -ForegroundColor Green

Write-Host ""
Write-Host "Step 5: Setting file permissions..." -ForegroundColor Yellow
Write-Host "  Restricting access to SYSTEM and Administrators only" -ForegroundColor Gray

try {
    # Get current ACL
    $acl = Get-Acl $envPath

    # Disable inheritance
    $acl.SetAccessRuleProtection($true, $false)

    # Remove all existing rules
    $acl.Access | ForEach-Object { $acl.RemoveAccessRule($_) | Out-Null }

    # Add SYSTEM full control
    $systemRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
        "SYSTEM",
        "FullControl",
        "Allow"
    )
    $acl.AddAccessRule($systemRule)

    # Add Administrators full control
    $adminRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
        "Administrators",
        "FullControl",
        "Allow"
    )
    $acl.AddAccessRule($adminRule)

    # Add current user read access
    $currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    $userRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
        $currentUser,
        "Read",
        "Allow"
    )
    $acl.AddAccessRule($userRule)

    # Apply ACL
    Set-Acl -Path $envPath -AclObject $acl

    Write-Host "  ✓ File permissions secured" -ForegroundColor Green
} catch {
    Write-Host "  WARNING: Could not set restrictive permissions" -ForegroundColor Yellow
    Write-Host "  File is still readable by all users on this system" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Step 6: Creating encrypted backup..." -ForegroundColor Yellow
$backupDir = ".\backups"
if (-not (Test-Path $backupDir)) {
    New-Item -Path $backupDir -ItemType Directory -Force | Out-Null
}

$backupEncPath = Join-Path $backupDir ".env.encrypted.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item $encryptedPath $backupEncPath
Write-Host "  ✓ Backup created: $backupEncPath" -ForegroundColor Green

Write-Host ""
Write-Host "Step 7: Extracting key information..." -ForegroundColor Yellow

# Parse some key values for display
$claudeKey = if ($decryptedContent -match "CLAUDE_API_KEY=(.+)") {
    $matches[1].Trim()
} else {
    "Not found"
}

$smtpServer = if ($decryptedContent -match "SMTP_SERVER=(.+)") {
    $matches[1].Trim()
} else {
    "Not found"
}

$domainName = if ($decryptedContent -match "DOMAIN_NAME=(.+)") {
    $matches[1].Trim()
} else {
    "doganconsult.com"
}

Write-Host "  Claude API Key: $($claudeKey.Substring(0, [Math]::Min(20, $claudeKey.Length)))..." -ForegroundColor White
Write-Host "  SMTP Server: $smtpServer" -ForegroundColor White
Write-Host "  Domain: $domainName" -ForegroundColor White

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " ✓ Secrets Deployed Successfully!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Files Created:" -ForegroundColor Cyan
Write-Host "  ✓ .env (with restricted permissions)" -ForegroundColor White
Write-Host "  ✓ Encrypted backup in backups/" -ForegroundColor White
Write-Host ""

Write-Host "Security:" -ForegroundColor Cyan
Write-Host "  • File permissions: SYSTEM, Administrators, and $currentUser (read) only" -ForegroundColor White
Write-Host "  • Original encrypted file preserved" -ForegroundColor White
Write-Host "  • Backup created for disaster recovery" -ForegroundColor White
Write-Host ""

Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "  • The .env file contains sensitive credentials" -ForegroundColor White
Write-Host "  • Do NOT copy this file to unsecured locations" -ForegroundColor White
Write-Host "  • Do NOT commit this file to version control" -ForegroundColor White
Write-Host "  • Keep the encrypted backup for disaster recovery" -ForegroundColor White
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Verify .env file: cat .env | Select-String 'CLAUDE_API_KEY'" -ForegroundColor White
Write-Host "  2. Run: .\5-deploy-with-docker.ps1 (deploy all services)" -ForegroundColor White
Write-Host ""

Write-Host "If you need to update secrets later:" -ForegroundColor Cyan
Write-Host "  1. Edit .env file directly: notepad .env" -ForegroundColor White
Write-Host "  2. Restart services: docker-compose -f docker-compose.production.yml restart" -ForegroundColor White
Write-Host ""
