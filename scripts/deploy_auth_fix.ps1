# Quick script to load .env.local and deploy auth fix
Write-Host "Loading credentials from .env.local..." -ForegroundColor Cyan

# Load .env.local
if (Test-Path ".env.local") {
    Get-Content .env.local | ForEach-Object {
        if ($_ -match "^([^=]+)=(.*)$") {
            $name = $matches[1]
            $value = $matches[2]
            Set-Item -Path "env:$name" -Value $value
        }
    }
}

# Load .env.prod (for SECRET_KEY if not in .env.local)
if (Test-Path ".env.prod") {
    Get-Content .env.prod | ForEach-Object {
        if ($_ -match "^([^=]+)=(.*)$") {
            $name = $matches[1]
            $value = $matches[2]
            # Don't override if already set
            if (-not (Test-Path "env:$name")) {
                Set-Item -Path "env:$name" -Value $value
            }
        }
    }
}

Write-Host ""
Write-Host "Checking credentials..." -ForegroundColor Yellow
$githubClientId = $env:GITHUB_CLIENT_ID
$githubClientSecret = $env:GITHUB_CLIENT_SECRET
$secretKey = $env:SECRET_KEY

if ($githubClientId) {
    $masked = "***" + $githubClientId.Substring([Math]::Max(0, $githubClientId.Length - 4))
    Write-Host "  ✓ GITHUB_CLIENT_ID = $masked" -ForegroundColor Green
} else {
    Write-Host "  ✗ GITHUB_CLIENT_ID = NOT SET" -ForegroundColor Red
}

if ($githubClientSecret) {
    Write-Host "  ✓ GITHUB_CLIENT_SECRET = ***" -ForegroundColor Green
} else {
    Write-Host "  ✗ GITHUB_CLIENT_SECRET = NOT SET" -ForegroundColor Red
}

if ($secretKey) {
    Write-Host "  ✓ SECRET_KEY = ***" -ForegroundColor Green
} else {
    Write-Host "  ✗ SECRET_KEY = NOT SET" -ForegroundColor Red
}

Write-Host ""

if (-not $githubClientId -or -not $githubClientSecret -or -not $secretKey) {
    Write-Host "ERROR: Missing required credentials!" -ForegroundColor Red
    exit 1
}

Write-Host "Updating Cloud Run service with auth secrets..." -ForegroundColor Cyan
Write-Host ""

gcloud run services update evalforge-agents `
  --project=evalforge `
  --region=us-central1 `
  --set-env-vars="GITHUB_CLIENT_ID=$githubClientId,GITHUB_CLIENT_SECRET=$githubClientSecret,SECRET_KEY=$secretKey,EVALFORGE_AUTH_MODE=github"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Successfully updated Cloud Run with auth secrets!" -ForegroundColor Green
    Write-Host ""
    Write-Host "The /api/auth/login endpoint should now work." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Failed to update Cloud Run" -ForegroundColor Red
    exit 1
}
