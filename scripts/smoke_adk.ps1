# Smoke test script for ADK endpoints
# Tests both local and production servers

param(
    [string]$BASE_LOCAL = "http://127.0.0.1:19000",
    [string]$BASE_PROD  = "https://evalforge-agents-uc7hnhrrkq-uc.a.run.app"
)

Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "ADK Smoke Tests" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan

# Local tests
Write-Host "`n📍 LOCAL ($BASE_LOCAL)" -ForegroundColor Yellow
Write-Host "Testing discovery..." -ForegroundColor Gray

try {
    $discovery = curl -sf "$BASE_LOCAL/list-apps?relative_path=arcade_app" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ discovery" -ForegroundColor Green
    } else {
        Write-Host "  ✗ discovery failed" -ForegroundColor Red
        throw "Discovery failed"
    }
} catch {
    Write-Host "  ✗ discovery error: $_" -ForegroundColor Red
    Write-Host "`n⚠️  Is local server running? Run: pwsh scripts/dev.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "Testing session creation..." -ForegroundColor Gray
try {
    $session = curl -sf -X POST -H "Content-Length: 0" "$BASE_LOCAL/apps/arcade_app/users/user/sessions" 2>&1
    if ($LASTEXITCODE -eq 0) {
        $sessionData = $session | ConvertFrom-Json
        Write-Host "  ✓ session (id: $($sessionData.id.Substring(0,8))...)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ session failed" -ForegroundColor Red
        throw "Session creation failed"
    }
} catch {
    Write-Host "  ✗ session error: $_" -ForegroundColor Red
    exit 1
}

# Production tests
Write-Host "`n📍 PRODUCTION ($BASE_PROD)" -ForegroundColor Yellow
Write-Host "Testing discovery..." -ForegroundColor Gray

try {
    $discovery = curl -sf "$BASE_PROD/list-apps?relative_path=arcade_app" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ discovery" -ForegroundColor Green
    } else {
        Write-Host "  ✗ discovery failed" -ForegroundColor Red
        throw "Discovery failed"
    }
} catch {
    Write-Host "  ✗ discovery error: $_" -ForegroundColor Red
    exit 1
}

Write-Host "Testing session creation..." -ForegroundColor Gray
try {
    $session = curl -sf -X POST -H "Content-Length: 0" "$BASE_PROD/apps/arcade_app/users/user/sessions" 2>&1
    if ($LASTEXITCODE -eq 0) {
        $sessionData = $session | ConvertFrom-Json
        Write-Host "  ✓ session (id: $($sessionData.id.Substring(0,8))...)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ session failed" -ForegroundColor Red
        throw "Session creation failed"
    }
} catch {
    Write-Host "  ✗ session error: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ All smoke tests passed!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
