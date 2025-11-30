# scripts/start_evalforge.ps1

Write-Host "🚀 Launching EvalForge (Live Mode)..." -ForegroundColor Cyan

# 1. Set Environment Variables explicitly
$env:GOOGLE_CLOUD_PROJECT = "291179078777"
$env:GOOGLE_CLOUD_LOCATION = "us-central1"
$env:EVALFORGE_PORT = "8092"
$env:EVALFORGE_MOCK_GRADING = "0"
$env:EVALFORGE_MODEL_VERSION = "gemini-2.5-flash"

# 2. Display Config
Write-Host "   Port:       $env:EVALFORGE_PORT"
Write-Host "   Model:      $env:EVALFORGE_MODEL_VERSION"
Write-Host "   Mock Mode:  OFF"
Write-Host "--------------------------------"

# 3. Run Server
# We use the env var for the port in the uvicorn command
python -m uvicorn arcade_app.agent:app --host 127.0.0.1 --port $env:EVALFORGE_PORT --reload
