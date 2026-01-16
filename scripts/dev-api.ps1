# EvalForge Backend Dev Server
# Starts uvicorn with proper environment variables

Write-Host "🚀 Starting EvalForge Backend..." -ForegroundColor Cyan

# Set environment variables
$env:DATABASE_URL = "postgresql+asyncpg://evalforge_app:evalforge_dev@127.0.0.1:5435/evalforge"
$env:REDIS_URL = "redis://127.0.0.1:6379/0"
$env:PYTHONPATH = "D:\EvalForge"
$env:ENV = "development"
$env:AUTO_INIT_DB = "0"  # Set to 1 if you want auto-init on startup

Write-Host "📍 DATABASE_URL: $env:DATABASE_URL" -ForegroundColor Gray
Write-Host "📍 REDIS_URL: $env:REDIS_URL" -ForegroundColor Gray
Write-Host "" -ForegroundColor Gray

# Start uvicorn with reload
python -m uvicorn arcade_app.agent:app --reload --host 127.0.0.1 --port 8092
