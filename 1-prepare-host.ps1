# DoganSystem Host Preparation Script
# Generates secrets, encrypts them, and prepares deployment package
# Run this on the Windows 11 Host machine

#Requires -Version 7.0

param(
    [string]$WorkingDir = "d:\DoganSystem",
    [switch]$SkipPackaging,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " DoganSystem - Host Preparation" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Change to working directory
Set-Location $WorkingDir

# Function to generate strong random password
function New-RandomPassword {
    param(
        [int]$Length = 32,
        [switch]$AlphaNumericOnly
    )

    if ($AlphaNumericOnly) {
        $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    } else {
        $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?'
    }

    $password = -join ((1..$Length) | ForEach-Object { $chars[(Get-Random -Maximum $chars.Length)] })
    return $password
}

# Function to encrypt string using DPAPI
function Protect-String {
    param([string]$PlainText)

    $bytes = [System.Text.Encoding]::UTF8.GetBytes($PlainText)
    $encrypted = [System.Security.Cryptography.ProtectedData]::Protect(
        $bytes,
        $null,
        [System.Security.Cryptography.DataProtectionScope]::CurrentUser
    )
    return [Convert]::ToBase64String($encrypted)
}

# Function to prompt for secret with validation
function Read-Secret {
    param(
        [string]$Prompt,
        [string]$ValidationPattern = ".*",
        [string]$ValidationMessage = "Invalid input",
        [switch]$Optional
    )

    do {
        $secret = Read-Host -Prompt $Prompt -AsSecureString
        $plainSecret = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
            [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
        )

        if ([string]::IsNullOrWhiteSpace($plainSecret) -and $Optional) {
            return ""
        }

        if ($plainSecret -match $ValidationPattern) {
            return $plainSecret
        } else {
            Write-Host "  $ValidationMessage" -ForegroundColor Red
        }
    } while ($true)
}

Write-Host "Step 1: Validating template file..." -ForegroundColor Yellow
$templatePath = ".\.env.production.template"
if (-not (Test-Path $templatePath)) {
    Write-Host "  ERROR: Template file not found: $templatePath" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Template found" -ForegroundColor Green

Write-Host ""
Write-Host "Step 2: Generating strong random passwords..." -ForegroundColor Yellow

$secrets = @{}

# Generate auto passwords
Write-Host "  Generating REDIS_PASSWORD..." -NoNewline
$secrets['REDIS_PASSWORD'] = New-RandomPassword -Length 32 -AlphaNumericOnly
Write-Host " ✓" -ForegroundColor Green

Write-Host "  Generating MYSQL_ROOT_PASSWORD..." -NoNewline
$secrets['MYSQL_ROOT_PASSWORD'] = New-RandomPassword -Length 32 -AlphaNumericOnly
Write-Host " ✓" -ForegroundColor Green

Write-Host "  Generating MYSQL_PASSWORD..." -NoNewline
$secrets['MYSQL_PASSWORD'] = New-RandomPassword -Length 32 -AlphaNumericOnly
Write-Host " ✓" -ForegroundColor Green

Write-Host "  Generating ERPNEXT_ADMIN_PASSWORD..." -NoNewline
$secrets['ERPNEXT_ADMIN_PASSWORD'] = New-RandomPassword -Length 16 -AlphaNumericOnly
Write-Host " ✓" -ForegroundColor Green

Write-Host "  Generating JWT_SECRET_KEY..." -NoNewline
$secrets['JWT_SECRET_KEY'] = New-RandomPassword -Length 64
Write-Host " ✓" -ForegroundColor Green

Write-Host "  Generating GRAFANA_PASSWORD..." -NoNewline
$secrets['GRAFANA_PASSWORD'] = New-RandomPassword -Length 16 -AlphaNumericOnly
Write-Host " ✓" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Please provide required credentials..." -ForegroundColor Yellow
Write-Host ""

# Claude API Key
Write-Host "  Claude API Key:" -ForegroundColor Cyan
Write-Host "    Get your API key from: https://console.anthropic.com/settings/keys" -ForegroundColor Gray
$secrets['CLAUDE_API_KEY'] = Read-Secret `
    -Prompt "    Enter Claude API Key" `
    -ValidationPattern "^sk-ant-api03-[A-Za-z0-9_-]+$" `
    -ValidationMessage "    Invalid Claude API key format. Should start with 'sk-ant-api03-'"

Write-Host "    ✓ Claude API key validated" -ForegroundColor Green
Write-Host ""

# SMTP Configuration
Write-Host "  SMTP Configuration:" -ForegroundColor Cyan
Write-Host "    For Gmail: Use app-specific password from https://myaccount.google.com/apppasswords" -ForegroundColor Gray
Write-Host ""

Write-Host "    SMTP Server (e.g., smtp.gmail.com):" -ForegroundColor White
$secrets['SMTP_SERVER'] = Read-Host "    "

Write-Host "    SMTP Port (default: 587):" -ForegroundColor White
$smtpPort = Read-Host "    "
$secrets['SMTP_PORT'] = if ([string]::IsNullOrWhiteSpace($smtpPort)) { "587" } else { $smtpPort }

Write-Host "    SMTP Username (email address):" -ForegroundColor White
$secrets['SMTP_USERNAME'] = Read-Host "    "

$secrets['SMTP_PASSWORD'] = Read-Secret `
    -Prompt "    Enter SMTP Password" `
    -ValidationPattern ".{8,}" `
    -ValidationMessage "    Password must be at least 8 characters"

Write-Host "    ✓ SMTP credentials saved" -ForegroundColor Green
Write-Host ""

# Optional: IMAP Configuration
Write-Host "  IMAP Configuration (for email processing):" -ForegroundColor Cyan
Write-Host "    Press Enter to skip IMAP setup or provide server name" -ForegroundColor Gray
$imapServer = Read-Host "    IMAP Server (default: imap.gmail.com)"
$secrets['IMAP_SERVER'] = if ([string]::IsNullOrWhiteSpace($imapServer)) { "imap.gmail.com" } else { $imapServer }

$imapPort = Read-Host "    IMAP Port (default: 993)"
$secrets['IMAP_PORT'] = if ([string]::IsNullOrWhiteSpace($imapPort)) { "993" } else { $imapPort }

Write-Host ""
Write-Host "Step 4: Adding deployment metadata..." -ForegroundColor Yellow
$secrets['DEPLOYED_AT'] = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
$secrets['DEPLOYED_BY'] = $env:USERNAME
$secrets['DEPLOYMENT_VERSION'] = "1.0.0-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Write-Host "  ✓ Metadata added" -ForegroundColor Green

Write-Host ""
Write-Host "Step 5: Creating .env.production file..." -ForegroundColor Yellow

# Read template
$envContent = Get-Content $templatePath -Raw

# Replace placeholders
foreach ($key in $secrets.Keys) {
    $envContent = $envContent -replace "__AUTO_GENERATED__", $secrets[$key], 1
    $envContent = $envContent -replace "__MANUAL_INPUT_REQUIRED__", $secrets[$key], 1
    $envContent = $envContent -replace "__AUTO_GENERATED_TIMESTAMP__", $secrets['DEPLOYED_AT']
    $envContent = $envContent -replace "__AUTO_GENERATED_USER__", $secrets['DEPLOYED_BY']
    $envContent = $envContent -replace "__AUTO_GENERATED_VERSION__", $secrets['DEPLOYMENT_VERSION']
}

# Save unencrypted version
$envPath = ".\.env.production"
$envContent | Out-File -FilePath $envPath -Encoding UTF8 -NoNewline
Write-Host "  ✓ Created: $envPath" -ForegroundColor Green

Write-Host ""
Write-Host "Step 6: Encrypting secrets using DPAPI..." -ForegroundColor Yellow
$encryptedContent = Protect-String -PlainText $envContent
$encryptedPath = ".\.env.production.encrypted"
$encryptedContent | Out-File -FilePath $encryptedPath -Encoding UTF8
Write-Host "  ✓ Created: $encryptedPath" -ForegroundColor Green
Write-Host "    (Encrypted with Windows Data Protection API - tied to your user account)" -ForegroundColor Gray

Write-Host ""
Write-Host "Step 7: Creating secrets reference file..." -ForegroundColor Yellow
$secretsRef = @"
DoganSystem Deployment Secrets Reference
Generated: $($secrets['DEPLOYED_AT'])
By: $($secrets['DEPLOYED_BY'])

CRITICAL SECRETS (Store securely):
===================================

Claude API Key: $($secrets['CLAUDE_API_KEY'])

SMTP Configuration:
  Server: $($secrets['SMTP_SERVER'])
  Port: $($secrets['SMTP_PORT'])
  Username: $($secrets['SMTP_USERNAME'])
  Password: $($secrets['SMTP_PASSWORD'])

IMAP Configuration:
  Server: $($secrets['IMAP_SERVER'])
  Port: $($secrets['IMAP_PORT'])

AUTO-GENERATED PASSWORDS:
===================================

Redis Password: $($secrets['REDIS_PASSWORD'])
MySQL Root Password: $($secrets['MYSQL_ROOT_PASSWORD'])
MySQL Password: $($secrets['MYSQL_PASSWORD'])
ERPNext Admin Password: $($secrets['ERPNEXT_ADMIN_PASSWORD'])
JWT Secret Key: $($secrets['JWT_SECRET_KEY'])
Grafana Password: $($secrets['GRAFANA_PASSWORD'])

IMPORTANT NOTES:
===================================
1. Store this file in a secure location (password manager, encrypted drive)
2. DO NOT commit this file to version control
3. Delete this file after securely storing the credentials
4. The .env.production.encrypted file can only be decrypted on this PC by this user account

ERPNext API Credentials:
===================================
After ERPNext is deployed and running, you'll need to:
1. Login to ERPNext at http://localhost:8000 (in the VM)
2. Create an API Key/Secret pair
3. Update these values in the .env file in the VM:
   - ERPNEXT_API_KEY
   - ERPNEXT_API_SECRET

Deployment Version: $($secrets['DEPLOYMENT_VERSION'])
"@

$secretsRefPath = ".\deployment-secrets.txt"
$secretsRef | Out-File -FilePath $secretsRefPath -Encoding UTF8
Write-Host "  ✓ Created: $secretsRefPath" -ForegroundColor Green
Write-Host "    WARNING: This file contains sensitive information!" -ForegroundColor Yellow
Write-Host "    Store it securely and delete after saving credentials elsewhere." -ForegroundColor Yellow

if (-not $SkipPackaging) {
    Write-Host ""
    Write-Host "Step 8: Creating deployment package..." -ForegroundColor Yellow

    $packagePath = ".\deployment-package.zip"
    if (Test-Path $packagePath) {
        if ($Force) {
            Remove-Item $packagePath -Force
            Write-Host "  Removed existing package" -ForegroundColor Gray
        } else {
            Write-Host "  Package already exists. Use -Force to overwrite." -ForegroundColor Yellow
            $packagePath = ".\deployment-package-$(Get-Date -Format 'yyyyMMdd-HHmmss').zip"
            Write-Host "  Creating new package: $packagePath" -ForegroundColor Gray
        }
    }

    # Files to include in package
    $filesToPackage = @(
        ".\.env.production.encrypted",
        ".\docker-compose.production.yml",
        ".\Dockerfile",
        ".\3-initialize-vm.ps1",
        ".\4-deploy-secrets.ps1",
        ".\5-deploy-with-docker.ps1",
        ".\6-configure-cloudflare-enhanced.ps1",
        ".\7-validate-deployment-enhanced.ps1",
        ".\8-setup-monitoring.ps1"
    )

    # Directories to include
    $dirsToPackage = @(
        ".\src",
        ".\agent-setup",
        ".\nginx",
        ".\cloudflare",
        ".\scripts"
    )

    # Create temporary directory for packaging
    $tempDir = New-Item -Path ".\temp-package" -ItemType Directory -Force

    # Copy files
    foreach ($file in $filesToPackage) {
        if (Test-Path $file) {
            Copy-Item $file -Destination $tempDir -Force
            Write-Host "    Packed: $file" -ForegroundColor Gray
        } else {
            Write-Host "    WARNING: File not found: $file" -ForegroundColor Yellow
        }
    }

    # Copy directories
    foreach ($dir in $dirsToPackage) {
        if (Test-Path $dir) {
            $dirName = Split-Path $dir -Leaf
            Copy-Item $dir -Destination (Join-Path $tempDir $dirName) -Recurse -Force
            Write-Host "    Packed: $dir" -ForegroundColor Gray
        } else {
            Write-Host "    WARNING: Directory not found: $dir" -ForegroundColor Yellow
        }
    }

    # Create zip
    Compress-Archive -Path "$tempDir\*" -DestinationPath $packagePath -Force

    # Cleanup
    Remove-Item $tempDir -Recurse -Force

    $packageSize = [math]::Round((Get-Item $packagePath).Length / 1MB, 2)
    Write-Host "  ✓ Package created: $packagePath ($packageSize MB)" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " ✓ Host Preparation Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Created files:" -ForegroundColor Cyan
Write-Host "  ✓ .env.production (unencrypted - for reference)" -ForegroundColor White
Write-Host "  ✓ .env.production.encrypted (DPAPI encrypted)" -ForegroundColor White
Write-Host "  ✓ deployment-secrets.txt (store securely!)" -ForegroundColor White
if (-not $SkipPackaging) {
    Write-Host "  ✓ deployment-package.zip (ready to copy to VM)" -ForegroundColor White
}
Write-Host ""

Write-Host "Generated Passwords:" -ForegroundColor Cyan
Write-Host "  Redis: $($secrets['REDIS_PASSWORD'].Substring(0, 8))..." -ForegroundColor White
Write-Host "  MySQL Root: $($secrets['MYSQL_ROOT_PASSWORD'].Substring(0, 8))..." -ForegroundColor White
Write-Host "  MySQL User: $($secrets['MYSQL_PASSWORD'].Substring(0, 8))..." -ForegroundColor White
Write-Host "  ERPNext Admin: $($secrets['ERPNEXT_ADMIN_PASSWORD'])" -ForegroundColor White
Write-Host "  JWT Secret: $($secrets['JWT_SECRET_KEY'].Substring(0, 16))..." -ForegroundColor White
Write-Host "  Grafana: $($secrets['GRAFANA_PASSWORD'])" -ForegroundColor White
Write-Host ""

Write-Host "IMPORTANT SECURITY REMINDERS:" -ForegroundColor Yellow
Write-Host "  1. Store deployment-secrets.txt in a password manager" -ForegroundColor White
Write-Host "  2. Delete deployment-secrets.txt after storing credentials" -ForegroundColor White
Write-Host "  3. DO NOT commit .env.production* files to version control" -ForegroundColor White
Write-Host "  4. The encrypted file can only be decrypted on THIS PC by THIS user" -ForegroundColor White
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Save the credentials from deployment-secrets.txt to a secure location" -ForegroundColor White
Write-Host "  2. Run: .\2-create-vm-enhanced.ps1" -ForegroundColor White
Write-Host "  3. After VM is created and Windows is installed:" -ForegroundColor White
Write-Host "     - Copy deployment-package.zip to the VM" -ForegroundColor White
Write-Host "     - Run the deployment scripts inside the VM" -ForegroundColor White
Write-Host ""
