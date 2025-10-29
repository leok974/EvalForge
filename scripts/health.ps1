# Health check script for local and production endpoints
# Usage: pwsh scripts/health.ps1

Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔍 Running Health Checks" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`n📍 LOCAL SERVER (http://127.0.0.1:19000)" -ForegroundColor Yellow

# Local discovery
try {
    curl -sf "http://127.0.0.1:19000/list-apps?relative_path=arcade_app" | Out-Null
    Write-Host "  ✓ discovery (local)" -ForegroundColor Green
} catch {
    Write-Host "  ✗ discovery failed - is server running?" -ForegroundColor Red
}

# Local session
try {
    $r = Invoke-WebRequest -Uri "http://127.0.0.1:19000/apps/arcade_app/users/user/sessions" -Method POST -UseBasicParsing
    Write-Host ("  ✓ session (local) - Status: {0}" -f $r.StatusCode) -ForegroundColor Green
} catch {
    Write-Host "  ✗ session failed" -ForegroundColor Red
}

Write-Host "`n📍 PRODUCTION SERVER (Cloud Run)" -ForegroundColor Yellow

# Prod discovery
try {
    curl -sf "https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/list-apps?relative_path=arcade_app" | Out-Null
    Write-Host "  ✓ discovery (prod)" -ForegroundColor Green
} catch {
    Write-Host "  ✗ discovery failed" -ForegroundColor Red
}

# Prod session
try {
    $r = Invoke-WebRequest -Uri "https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/apps/arcade_app/users/user/sessions" -Method POST -UseBasicParsing
    Write-Host ("  ✓ session (prod) - Status: {0}" -f $r.StatusCode) -ForegroundColor Green
} catch {
    Write-Host "  ✗ session failed" -ForegroundColor Red
}

Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ Health checks complete" -ForegroundColor Green
Write-Host ""
