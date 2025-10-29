# Start ADK dev server in dedicated terminal
# Usage: pwsh scripts/dev.ps1

$env:GENAI_PROVIDER="vertex"
$env:GOOGLE_CLOUD_PROJECT="evalforge-1063529378"
$env:VERTEX_LOCATION="us-east5"
$env:GENAI_MODEL="gemini-1.5-flash-002"

Write-Host "🚀 Starting ADK dev server..." -ForegroundColor Cyan
Write-Host "   Port: 19000" -ForegroundColor White
Write-Host "   Vertex Region: us-east5 (Gemini-supported)" -ForegroundColor White
Write-Host "   UI: http://127.0.0.1:19000/dev-ui/" -ForegroundColor White
Write-Host ""

cd D:\EvalForge
Start-Process pwsh -ArgumentList "-NoExit","-Command","D:/EvalForge/.venv/Scripts/python.exe -m google.adk.cli web . --host 0.0.0.0 --port 19000"

Write-Host "✓ Server started in new terminal" -ForegroundColor Green
Write-Host "  Wait ~5 seconds then run: pwsh scripts/health.ps1" -ForegroundColor Yellow
