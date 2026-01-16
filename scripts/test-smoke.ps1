# Run EvalForge Smoke Tests
# Tests core API functionality without starting the full server

Write-Host "🧪 Running EvalForge Smoke Tests..." -ForegroundColor Cyan

# Set environment variables
$env:DATABASE_URL = "postgresql+asyncpg://evalforge_app:evalforge_dev@127.0.0.1:5435/evalforge"
$env:PYTHONPATH = "D:\EvalForge"
$env:ENV = "test"

Write-Host "📍 DATABASE_URL: $env:DATABASE_URL" -ForegroundColor Gray
Write-Host "" -ForegroundColor Gray

# Run smoke tests
python -m pytest tests/smoke/ -v --tb=short --maxfail=3

if ($LASTEXITCODE -eq 0) {
    Write-Host "" -ForegroundColor Gray
    Write-Host "✅ All smoke tests passed!" -ForegroundColor Green
} else {
    Write-Host "" -ForegroundColor Gray
    Write-Host "❌ Some smoke tests failed" -ForegroundColor Red
    Write-Host "   Check the output above for details" -ForegroundColor Yellow
    exit 1
}
