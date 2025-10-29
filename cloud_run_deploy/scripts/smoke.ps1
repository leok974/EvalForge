# scripts/smoke.ps1 - Smoke tests for local and production
param(
    [ValidateSet("local", "prod")]
    [string]$Env = "local",
    [string]$Base = "https://evalforge-agents-291179078777.us-central1.run.app"
)

$ErrorActionPreference = "Stop"

$base = if ($Env -eq "local") { "http://127.0.0.1:19000" } else { $Base }

Write-Host "`n🧪 Running smoke tests - $Env" -ForegroundColor Cyan
Write-Host "Base URL: $base`n" -ForegroundColor Gray

# Test discovery
Write-Host "→ discovery" -ForegroundColor Cyan
$discoveryUrl = "$base/list-apps?relative_path=arcade_app"
Invoke-WebRequest -UseBasicParsing -Uri $discoveryUrl | Out-Null
Write-Host "✓ discovery passed" -ForegroundColor Green

# Test session creation
Write-Host "→ session" -ForegroundColor Cyan
$sessionUrl = "$base/apps/arcade_app/users/user/sessions"
Invoke-WebRequest -UseBasicParsing -Method POST -Uri $sessionUrl -Headers @{"Content-Length" = "0"} | Out-Null
Write-Host "✓ session passed" -ForegroundColor Green

Write-Host "`n✅ All smoke tests passed!`n" -ForegroundColor Green

