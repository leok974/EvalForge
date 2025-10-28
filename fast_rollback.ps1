# Fast Rollback Script for EvalForge
# Rolls back to the previous healthy Cloud Run revision

param(
    [string]$ServiceName = "evalforge-agents",
    [string]$Region = "us-central1",
    [switch]$DryRun
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "EvalForge Fast Rollback" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get current revision
$currentRevision = gcloud run services describe $ServiceName `
    --region=$Region `
    --format='value(status.latestCreatedRevisionName)'

Write-Host "Current revision: $currentRevision" -ForegroundColor Yellow

# Get all revisions
$allRevisions = gcloud run revisions list `
    --service=$ServiceName `
    --region=$Region `
    --format='value(name)' | Select-Object -First 5

Write-Host ""
Write-Host "Recent revisions:" -ForegroundColor Cyan
$allRevisions | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
Write-Host ""

# Get previous revision (second in list)
$previousRevision = $allRevisions | Select-Object -Skip 1 -First 1

if (-not $previousRevision) {
    Write-Host "❌ ERROR: No previous revision found" -ForegroundColor Red
    exit 1
}

Write-Host "Will rollback to: $previousRevision" -ForegroundColor Yellow
Write-Host ""

# Check environment variables of target revision
Write-Host "Checking target revision configuration..." -ForegroundColor Yellow
$targetConfig = gcloud run revisions describe $previousRevision `
    --region=$Region `
    --format='yaml(spec.containers[0].env)' | Select-String -Pattern "GENAI_MODEL"

Write-Host $targetConfig -ForegroundColor Gray
Write-Host ""

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No changes will be made" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Would execute:" -ForegroundColor Yellow
    Write-Host "  gcloud run services update-traffic $ServiceName \" -ForegroundColor Gray
    Write-Host "    --region=$Region \" -ForegroundColor Gray
    Write-Host "    --to-revisions=$previousRevision=100" -ForegroundColor Gray
    exit 0
}

$confirm = Read-Host "Proceed with rollback? (yes/N)"
if ($confirm -ne "yes") {
    Write-Host "Rollback cancelled." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "Rolling back..." -ForegroundColor Cyan

# Execute rollback
gcloud run services update-traffic $ServiceName `
    --region=$Region `
    --to-revisions="$previousRevision=100"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Rollback Successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Traffic now routing to: $previousRevision" -ForegroundColor Green
    Write-Host ""
    
    # Get service URL
    $serviceUrl = gcloud run services describe $ServiceName `
        --region=$Region `
        --format='value(status.url)'
    
    Write-Host "Service URL: $serviceUrl" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Verify rollback:" -ForegroundColor Cyan
    Write-Host "  curl -sf `"$serviceUrl/list-apps?relative_path=arcade_app`"" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Monitor logs:" -ForegroundColor Cyan
    Write-Host "  gcloud logging tail `"resource.type=cloud_run_revision AND resource.labels.service_name=$ServiceName`"" -ForegroundColor Gray
    Write-Host ""
    
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "✗ Rollback Failed" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the error messages above." -ForegroundColor Yellow
    Write-Host "You may need to manually set traffic in Cloud Console." -ForegroundColor Yellow
    exit 1
}
