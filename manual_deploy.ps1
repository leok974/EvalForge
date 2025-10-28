# Manual Cloud Run Deployment Script
# Workaround for ADK Windows gcloud PATH issue

param(
    [string]$ProjectId = "evalforge-1063529378",
    [string]$Region = "us-central1",
    [string]$ServiceName = "evalforge-agents"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Manual Cloud Run Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create deployment directory
$deployFolder = "D:\EvalForge\cloud_run_deploy"
if (Test-Path $deployFolder) {
    Write-Host "Cleaning existing deployment folder..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $deployFolder
}
New-Item -ItemType Directory -Path $deployFolder | Out-Null
Write-Host "✓ Created: $deployFolder" -ForegroundColor Green
Write-Host ""

# Step 2: Copy application files
Write-Host "Copying application files..." -ForegroundColor Yellow
$filesToCopy = @(
    "arcade_app",
    "exercises",
    "scripts",
    "seed",
    "requirements.txt"
)

foreach ($item in $filesToCopy) {
    $source = Join-Path "D:\EvalForge" $item
    if (Test-Path $source) {
        Copy-Item -Recurse $source $deployFolder
        Write-Host "  ✓ Copied: $item" -ForegroundColor Green
    } else {
        Write-Warning "  ⚠ Not found: $item"
    }
}
Write-Host ""

# Step 3: Create Dockerfile
Write-Host "Creating Dockerfile..." -ForegroundColor Yellow
$dockerfile = @'
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port (Cloud Run will set PORT env var)
EXPOSE 8080

# Start ADK server in scan mode from WORKDIR (/app) which contains arcade_app/
CMD ["sh", "-c", "python -m google.adk.cli web . --host 0.0.0.0 --port ${PORT:-8080}"]
'@

$dockerfilePath = Join-Path $deployFolder "Dockerfile"
$dockerfile | Out-File -Encoding UTF8 -NoNewline $dockerfilePath
Write-Host "✓ Created: Dockerfile" -ForegroundColor Green
Write-Host ""

# Step 4: Create .dockerignore
Write-Host "Creating .dockerignore..." -ForegroundColor Yellow
$dockerignore = @'
.venv
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.git
.gitignore
.vscode
*.md
logs
.env
'@

$dockerignorePath = Join-Path $deployFolder ".dockerignore"
$dockerignore | Out-File -Encoding UTF8 -NoNewline $dockerignorePath
Write-Host "✓ Created: .dockerignore" -ForegroundColor Green
Write-Host ""

# Step 5: Deploy with gcloud
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploying to Cloud Run" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project:      $ProjectId" -ForegroundColor Yellow
Write-Host "Region:       $Region" -ForegroundColor Yellow
Write-Host "Service:      $ServiceName" -ForegroundColor Yellow
Write-Host "Source:       $deployFolder" -ForegroundColor Yellow
Write-Host ""

# Guard: Verify model version ends with -002 (prevent env drift)
Write-Host "Verifying model configuration..." -ForegroundColor Yellow
$agentFile = Join-Path $deployFolder "arcade_app\agent.py"
$agentContent = Get-Content $agentFile -Raw
if ($agentContent -notmatch 'gemini-1\.5-flash-002') {
    Write-Host "❌ ERROR: Model default must be gemini-1.5-flash-002" -ForegroundColor Red
    Write-Host "Found configuration that doesn't include versioned model." -ForegroundColor Red
    Write-Host "This deployment would cause model regression." -ForegroundColor Red
    Write-Host ""
    Write-Host "Fix: Ensure arcade_app/agent.py defaults to 'gemini-1.5-flash-002'" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Model version guard passed (gemini-1.5-flash-002)" -ForegroundColor Green
Write-Host ""

$confirm = Read-Host "Continue with deployment? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Deployment cancelled." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "Deploying... (this may take 5-10 minutes)" -ForegroundColor Cyan
Write-Host ""

# Run gcloud deploy with locked environment variables
cd $deployFolder

# HARDENED: Lock all Vertex AI configuration to prevent regression
$envVars = @(
    "GENAI_PROVIDER=vertex",
    "GOOGLE_CLOUD_PROJECT=$ProjectId",
    "VERTEX_LOCATION=$Region",
    "GENAI_MODEL=gemini-1.5-flash-002",
    "GOOGLE_GENAI_USE_VERTEXAI=true",
    "GOOGLE_CLOUD_LOCATION=$Region"
) -join ","

Write-Host "Locked Environment Variables:" -ForegroundColor Cyan
Write-Host "  GENAI_PROVIDER=vertex" -ForegroundColor Gray
Write-Host "  GOOGLE_CLOUD_PROJECT=$ProjectId" -ForegroundColor Gray
Write-Host "  VERTEX_LOCATION=$Region" -ForegroundColor Gray
Write-Host "  GENAI_MODEL=gemini-1.5-flash-002" -ForegroundColor Gray
Write-Host ""

gcloud run deploy $ServiceName `
    --source . `
    --project=$ProjectId `
    --region=$Region `
    --platform=managed `
    --allow-unauthenticated `
    --port=8080 `
    --memory=512Mi `
    --timeout=300 `
    --set-env-vars=$envVars

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Deployment Successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    # Pin traffic to latest revision (avoid stale envs)
    Write-Host "Pinning traffic to latest revision..." -ForegroundColor Yellow
    $latestRevision = gcloud run services describe $ServiceName `
        --project=$ProjectId `
        --region=$Region `
        --format='value(status.latestCreatedRevisionName)'
    
    gcloud run services update-traffic $ServiceName `
        --project=$ProjectId `
        --region=$Region `
        --to-latest
    
    Write-Host "✓ Traffic pinned to revision: $latestRevision" -ForegroundColor Green
    Write-Host ""
    
    # Get the service URL
    $serviceUrl = gcloud run services describe $ServiceName `
        --project=$ProjectId `
        --region=$Region `
        --format='value(status.url)'
    
    Write-Host "Service URL:" -ForegroundColor Yellow
    Write-Host $serviceUrl -ForegroundColor White
    Write-Host ""
    Write-Host "Web UI:" -ForegroundColor Yellow
    Write-Host "$serviceUrl/dev-ui/" -ForegroundColor White
    Write-Host ""
    Write-Host "Test the agent:" -ForegroundColor Yellow
    Write-Host "curl $serviceUrl/" -ForegroundColor Gray
    Write-Host ""
    
    # Plan B reminder: Keep Google AI API secret ready but disabled
    Write-Host "Plan B Status:" -ForegroundColor Cyan
    $secretExists = gcloud secrets describe google-api-key `
        --project=$ProjectId 2>&1 | Select-String "name:"
    
    if ($secretExists) {
        Write-Host "  ✓ google-api-key secret exists (Plan B ready)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ google-api-key secret not found" -ForegroundColor Yellow
        Write-Host "  To enable Plan B fallback, create secret:" -ForegroundColor Gray
        Write-Host "    echo -n `"YOUR_API_KEY`" | gcloud secrets create google-api-key --data-file=-" -ForegroundColor Gray
    }
    Write-Host ""
    
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "✗ Deployment Failed" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the error messages above." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Not authenticated: Run 'gcloud auth login'" -ForegroundColor White
    Write-Host "2. APIs not enabled: Run the commands in DEPLOYMENT.md" -ForegroundColor White
    Write-Host "3. Billing not enabled: Check Cloud Console" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Return to original directory
cd D:\EvalForge
