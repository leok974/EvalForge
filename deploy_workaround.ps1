# Workaround script to deploy with gcloud in PATH
# This ensures Python subprocess can find gcloud

# Get the gcloud bin directory
$gcloudCmd = Get-Command gcloud -ErrorAction Stop
$gcloudBinDir = Split-Path $gcloudCmd.Source

# Add to both user PATH and current session
$env:PATH = "$gcloudBinDir;$env:PATH"

# Also set CLOUDSDK_PYTHON to ensure gcloud uses correct Python
$cloudsdkPython = Get-Command python -ErrorAction SilentlyContinue
if ($cloudsdkPython) {
    $env:CLOUDSDK_PYTHON = $cloudsdkPython.Source
}

Write-Host "✓ gcloud bin added to PATH: $gcloudBinDir" -ForegroundColor Green
Write-Host "✓ Current PATH (first 200 chars): $($env:PATH.Substring(0, [Math]::Min(200, $env:PATH.Length)))..." -ForegroundColor Cyan
Write-Host ""

# Now run the deployment
Write-Host "Running ADK deployment..." -ForegroundColor Yellow
adk deploy cloud_run --project="evalforge-1063529378" --region="us-central1" --service_name="evalforge-agents" --app_name="evalforge" --with_ui .
