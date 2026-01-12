# Set Authentication Secrets for EvalForge Deployment
# Run this script BEFORE running manual_deploy.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EvalForge Authentication Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env.prod exists
if (Test-Path ".env.prod") {
    Write-Host "Loading secrets from .env.prod..." -ForegroundColor Yellow
    Get-Content .env.prod | ForEach-Object {
        if ($_ -match "^([^=]+)=(.*)$") {
            $name = $matches[1]
            $value = $matches[2]
            Set-Item -Path "env:$name" -Value $value
            Write-Host "  ✓ Set $name" -ForegroundColor Green
        }
    }
    Write-Host ""
} else {
    Write-Host "No .env.prod file found. Please set variables manually." -ForegroundColor Yellow
    Write-Host ""
}

# Validate required variables
$required = @("GITHUB_CLIENT_ID", "GITHUB_CLIENT_SECRET", "SECRET_KEY")
$missing = @()

foreach ($var in $required) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ($value) {
        $masked = if ($value.Length -gt 4) { "***" + $value.Substring($value.Length - 4) } else { "***" }
        Write-Host "  $var = $masked" -ForegroundColor Green
    } else {
        Write-Host "  $var = NOT SET" -ForegroundColor Red
        $missing += $var
    }
}

Write-Host ""

if ($missing.Count -gt 0) {
    Write-Host "Missing variables: $($missing -join ', ')" -ForegroundColor Red
    Write-Host ""
    Write-Host "To set them manually, run:" -ForegroundColor Yellow
    Write-Host '  $env:GITHUB_CLIENT_ID = "your_github_oauth_client_id"' -ForegroundColor Gray
    Write-Host '  $env:GITHUB_CLIENT_SECRET = "your_github_oauth_client_secret"' -ForegroundColor Gray
    Write-Host '  $env:SECRET_KEY = "your_random_secret_key"' -ForegroundColor Gray
    Write-Host ""
    Write-Host "Or create a .env.prod file with these values." -ForegroundColor Gray
    exit 1
} else {
    Write-Host "✓ All authentication secrets are set!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run: ./manual_deploy.ps1" -ForegroundColor Cyan
}
