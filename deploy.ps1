# Deploy EvalForge to Google Cloud Run
# Usage: .\deploy.ps1

# ========================================
# Configuration - UPDATE THESE VALUES
# ========================================
$PROJECT_ID = "evalforge-1063529378"  # e.g., "my-project-123456"
$REGION = "us-central1"  # e.g., "us-central1", "us-east1", "europe-west1"
$SERVICE_NAME = "evalforge-agents"
$APP_NAME = "evalforge"
$SA_EMAIL = ""  # Optional: Service account email (leave empty to use default)

# ========================================
# Validation
# ========================================
if ([string]::IsNullOrWhiteSpace($PROJECT_ID)) {
    Write-Error "ERROR: PROJECT_ID is not set. Please edit deploy.ps1 and set your Google Cloud Project ID."
    exit 1
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EvalForge Cloud Run Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Project ID:     $PROJECT_ID" -ForegroundColor Yellow
Write-Host "Region:         $REGION" -ForegroundColor Yellow
Write-Host "Service Name:   $SERVICE_NAME" -ForegroundColor Yellow
Write-Host "App Name:       $APP_NAME" -ForegroundColor Yellow
if (![string]::IsNullOrWhiteSpace($SA_EMAIL)) {
    Write-Host "Service Acct:   $SA_EMAIL" -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ========================================
# Activate Virtual Environment
# ========================================
Write-Host "Activating virtual environment..." -ForegroundColor Green
.\.venv\Scripts\Activate.ps1

# ========================================
# Verify ADK Installation
# ========================================
Write-Host "Verifying google-adk installation..." -ForegroundColor Green
$adkVersion = python -c "import google.adk; print(google.adk.__version__)" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "ERROR: google-adk is not installed. Run: pip install google-adk"
    exit 1
}
Write-Host "✓ google-adk version: $adkVersion" -ForegroundColor Green
Write-Host ""

# ========================================
# Check gcloud CLI
# ========================================
Write-Host "Checking gcloud CLI..." -ForegroundColor Green
$gcloudInstalled = Get-Command gcloud -ErrorAction SilentlyContinue
if (!$gcloudInstalled) {
    Write-Warning "WARNING: gcloud CLI not found. Install from: https://cloud.google.com/sdk/docs/install"
    Write-Host "You can still try the deployment, but it may fail." -ForegroundColor Yellow
    Write-Host ""
} else {
    $gcloudVersion = gcloud version --format="value(version)" 2>$null
    Write-Host "✓ gcloud CLI version: $gcloudVersion" -ForegroundColor Green
    
    # Add gcloud bin directory to PATH for subprocess calls (needed by ADK)
    $gcloudBinDir = Split-Path $gcloudInstalled.Source
    if ($gcloudBinDir -and (Test-Path $gcloudBinDir)) {
        # Ensure gcloud.cmd is in PATH for Python subprocess
        if ($env:PATH -notlike "*$gcloudBinDir*") {
            $env:PATH = "$gcloudBinDir;$env:PATH"
            Write-Host "✓ Added gcloud bin to PATH: $gcloudBinDir" -ForegroundColor Green
        }
        
        # Verify gcloud.cmd exists
        $gcloudCmd = Join-Path $gcloudBinDir "gcloud.cmd"
        if (Test-Path $gcloudCmd) {
            Write-Host "✓ Found gcloud.cmd: $gcloudCmd" -ForegroundColor Green
        } else {
            Write-Warning "WARNING: gcloud.cmd not found at $gcloudCmd"
        }
    }
    
    # Check authentication
    $currentAccount = gcloud config get-value account 2>$null
    if ([string]::IsNullOrWhiteSpace($currentAccount)) {
        Write-Warning "WARNING: Not authenticated with gcloud. Run: gcloud auth login"
    } else {
        Write-Host "✓ Authenticated as: $currentAccount" -ForegroundColor Green
    }
    Write-Host ""
}

# ========================================
# Build Deploy Command
# ========================================
$deployCmd = "adk deploy cloud_run --project=`"$PROJECT_ID`" --region=`"$REGION`" --service_name=`"$SERVICE_NAME`" --app_name=`"$APP_NAME`" --with_ui"

if (![string]::IsNullOrWhiteSpace($SA_EMAIL)) {
    $deployCmd += " --service_account=`"$SA_EMAIL`""
}

$deployCmd += " ."

# ========================================
# Confirmation
# ========================================
Write-Host "About to run:" -ForegroundColor Yellow
Write-Host $deployCmd -ForegroundColor White
Write-Host ""
$confirm = Read-Host "Continue with deployment? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Deployment cancelled." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Deployment..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ========================================
# Deploy
# ========================================
Write-Host "Running: $deployCmd" -ForegroundColor Cyan
Write-Host ""

# Capture output and check for errors
$deployOutput = Invoke-Expression $deployCmd 2>&1 | Tee-Object -Variable deployResult
$deployExitCode = $LASTEXITCODE

# ========================================
# Result
# ========================================
if ($deployExitCode -eq 0 -and $deployOutput -notlike "*Deploy failed*") {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Deployment Successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your service should be available at:" -ForegroundColor Yellow
    Write-Host "https://$SERVICE_NAME-<hash>-$REGION.a.run.app" -ForegroundColor White
    Write-Host ""
    Write-Host "To view your service:" -ForegroundColor Yellow
    Write-Host "gcloud run services describe $SERVICE_NAME --project=$PROJECT_ID --region=$REGION" -ForegroundColor White
    Write-Host ""
    Write-Host "Get the exact URL:" -ForegroundColor Yellow
    Write-Host "gcloud run services describe $SERVICE_NAME --project=$PROJECT_ID --region=$REGION --format='value(status.url)'" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "✗ Deployment Failed" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    
    if ($deployOutput -like "*The system cannot find the file specified*") {
        Write-Host "ERROR: gcloud CLI not found in PATH" -ForegroundColor Red
        Write-Host ""
        Write-Host "Solutions:" -ForegroundColor Yellow
        Write-Host "1. Restart PowerShell to refresh PATH environment variable" -ForegroundColor White
        Write-Host "2. Manually add gcloud to PATH:" -ForegroundColor White
        Write-Host '   $env:PATH = "C:\Users\pierr\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin;$env:PATH"' -ForegroundColor Gray
        Write-Host "3. Verify gcloud works: gcloud version" -ForegroundColor White
    } elseif ($deployOutput -like "*not authenticated*" -or $deployOutput -like "*credentials*") {
        Write-Host "ERROR: Not authenticated with Google Cloud" -ForegroundColor Red
        Write-Host ""
        Write-Host "Run: gcloud auth login" -ForegroundColor White
        Write-Host "Then: gcloud auth application-default login" -ForegroundColor White
    } else {
        Write-Host "Check the error messages above for details." -ForegroundColor Yellow
    }
    Write-Host ""
    exit 1
}
