# Deploy EvalForge to Google Cloud Run
# Usage: .\deploy.ps1

# ========================================
# Configuration
# ========================================
$PROJECT_ID = "evalforge-1063529378"
$REGION = "us-central1"
$SERVICE_NAME = "evalforge-agents"
$APP_NAME = "evalforge"

# ========================================
# Activations
# ========================================
Write-Host "Activating virtual environment..." -ForegroundColor Green
if (Test-Path .\.venv\Scripts\Activate.ps1) {
    .\.venv\Scripts\Activate.ps1
} else {
    Write-Warning "Virtual environment not found at .\.venv\Scripts\Activate.ps1"
}

# ========================================
# Check Checks
# ========================================
Write-Host "Verifying google-adk..." -ForegroundColor Green
try {
    python -c "import google.adk; print(google.adk.__version__)" 2>$null
} catch {
    Write-Warning "Failed to check adk version."
}

# ========================================
# Deploy Command
# ========================================
$deployCmd = "adk deploy cloud_run --project=`"$PROJECT_ID`" --region=`"$REGION`" --service_name=`"$SERVICE_NAME`" --app_name=`"$APP_NAME`" --with_ui ."

Write-Host "Starting Deployment..." -ForegroundColor Cyan
Write-Host "Running: $deployCmd" -ForegroundColor White

# Run directly
try {
    Invoke-Expression $deployCmd
} catch {
    Write-Error "Deployment failed: $_"
    exit 1
}

Write-Host "Deployment command finished." -ForegroundColor Green
exit 0
