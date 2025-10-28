# Deploy Cloud Monitoring Alerts for EvalForge
# Creates log-based metrics and alert policies

param(
    [string]$ProjectId = "evalforge-1063529378",
    [switch]$DryRun
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EvalForge Alert Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No changes will be made" -ForegroundColor Cyan
    Write-Host ""
}

# Step 1: Create log-based metrics
Write-Host "Creating log-based metrics..." -ForegroundColor Yellow
Write-Host ""

# Vertex 404 errors metric
Write-Host "  Creating vertex_404_errors metric..." -ForegroundColor Gray
if (-not $DryRun) {
    gcloud logging metrics create vertex_404_errors `
        --project=$ProjectId `
        --description="Vertex AI 404 NOT_FOUND errors" `
        --log-filter='resource.type="cloud_run_revision"
    AND resource.labels.service_name="evalforge-agents"
    AND textPayload:"404 NOT_FOUND"
    AND textPayload:"aiplatform.googleapis.com"' 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✓ vertex_404_errors created" -ForegroundColor Green
    } else {
        Write-Host "    ⚠ metric may already exist" -ForegroundColor Yellow
    }
}

# Vertex 403 errors metric
Write-Host "  Creating vertex_403_errors metric..." -ForegroundColor Gray
if (-not $DryRun) {
    gcloud logging metrics create vertex_403_errors `
        --project=$ProjectId `
        --description="Vertex AI 403 PERMISSION_DENIED errors" `
        --log-filter='resource.type="cloud_run_revision"
    AND resource.labels.service_name="evalforge-agents"
    AND textPayload:"403 PERMISSION_DENIED"
    AND textPayload:"aiplatform.googleapis.com"' 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✓ vertex_403_errors created" -ForegroundColor Green
    } else {
        Write-Host "    ⚠ metric may already exist" -ForegroundColor Yellow
    }
}

Write-Host ""

# Step 2: Create alert policies (requires notification channels)
Write-Host "Checking for notification channels..." -ForegroundColor Yellow

$channels = gcloud alpha monitoring channels list `
    --project=$ProjectId `
    --format='value(name)' 2>&1

if ($channels -match "CHANNEL_ID") {
    Write-Host "  ✓ Notification channels found" -ForegroundColor Green
} else {
    Write-Host "  ⚠ No notification channels configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To create alerts, first create a notification channel:" -ForegroundColor Cyan
    Write-Host "  gcloud alpha monitoring channels create \" -ForegroundColor Gray
    Write-Host "    --display-name=`"EvalForge Alerts`" \" -ForegroundColor Gray
    Write-Host "    --type=email \" -ForegroundColor Gray
    Write-Host "    --channel-labels=email_address=YOUR_EMAIL@example.com" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Then update alert policy files with the channel ID." -ForegroundColor Yellow
    Write-Host ""
    
    if (-not $DryRun) {
        $createChannel = Read-Host "Would you like to create an email notification channel now? (y/N)"
        if ($createChannel -eq "y" -or $createChannel -eq "Y") {
            $email = Read-Host "Enter email address"
            
            gcloud alpha monitoring channels create `
                --project=$ProjectId `
                --display-name="EvalForge Alerts" `
                --type=email `
                --channel-labels="email_address=$email"
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✓ Notification channel created" -ForegroundColor Green
            }
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Log-based metrics created" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create alert policies (manual or via policy files):" -ForegroundColor Yellow
Write-Host "   See: analytics/alerts/*.json" -ForegroundColor Gray
Write-Host ""
Write-Host "2. View metrics in Cloud Console:" -ForegroundColor Yellow
Write-Host "   https://console.cloud.google.com/logs/metrics?project=$ProjectId" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Test alerts by triggering an error (optional):" -ForegroundColor Yellow
Write-Host "   Deploy with wrong model name temporarily" -ForegroundColor Gray
Write-Host ""
