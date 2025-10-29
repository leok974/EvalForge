#!/usr/bin/env pwsh
# Curl smoke tests for local and production endpoints

param(
    [ValidateSet("local", "prod")]
    [string]$Environment = "local"
)

$ErrorActionPreference = "Stop"

if ($Environment -eq "local") {
    $BASE = "http://127.0.0.1:19000"
} else {
    $BASE = "https://evalforge-agents-291179078777.us-central1.run.app"
}

Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🧪 Curl Smoke Test - $Environment" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "GET $BASE/list-apps?relative_path=arcade_app" -ForegroundColor Yellow
$disco = curl.exe -s "$BASE/list-apps?relative_path=arcade_app"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Discovery passed" -ForegroundColor Green
    $disco | Out-Host
} else {
    Write-Host "✗ Discovery failed" -ForegroundColor Red
    exit 1
}

Write-Host "`nPOST $BASE/apps/arcade_app/users/user/sessions" -ForegroundColor Yellow
$sess = curl.exe -s -X POST -H "Content-Length: 0" "$BASE/apps/arcade_app/users/user/sessions"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Session passed" -ForegroundColor Green
    $sess | Out-Host
} else {
    Write-Host "✗ Session failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ All smoke tests passed!" -ForegroundColor Green
