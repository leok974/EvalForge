# Manual Cloud Run Deployment Script
# Workaround for ADK Windows gcloud PATH issue

param(
    [string]$ProjectId = "evalforge",  # gcloud requires project ID
    [string]$ProjectNumber = "291179078777",  # Application needs project number (PROD)
    [string]$Region = "us-central1",
    [string]$ServiceName = "evalforge-agents"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Manual Cloud Run Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vertex AI configuration (gemini-2.5-flash in us-central1)
$env:VERTEX_PROJECT_NUMBER = $ProjectNumber
$env:VERTEX_REGION = "us-central1"
$env:VERTEX_MODEL_ID = "gemini-2.5-flash"

Write-Host "Vertex AI Configuration:" -ForegroundColor Cyan
Write-Host "  Project Number: $ProjectNumber" -ForegroundColor Gray
Write-Host "  Project ID (gcloud): $ProjectId" -ForegroundColor Gray
Write-Host "  Region: $env:VERTEX_REGION" -ForegroundColor Gray
Write-Host "  Model: $env:VERTEX_MODEL_ID" -ForegroundColor Gray
Write-Host "  Cloud Run Region: $Region" -ForegroundColor Gray
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
Write-Host "Project ID (gcloud):    $ProjectId" -ForegroundColor Yellow
Write-Host "Project Number (app):   $ProjectNumber" -ForegroundColor Yellow
Write-Host "Region:                 $Region" -ForegroundColor Yellow
Write-Host "Service:                $ServiceName" -ForegroundColor Yellow
Write-Host "Source:                 $deployFolder" -ForegroundColor Yellow
Write-Host ""

# Guard: Verify model is gemini-2.5-flash
Write-Host "Verifying model configuration..." -ForegroundColor Yellow
$agentFile = Join-Path $deployFolder "arcade_app\agent.py"
$agentContent = Get-Content $agentFile -Raw
if ($agentContent -notmatch 'gemini-2\.5-flash') {
    Write-Host "❌ ERROR: Model must be gemini-2.5-flash" -ForegroundColor Red
    Write-Host "Found configuration that doesn't include gemini-2.5-flash." -ForegroundColor Red
    Write-Host "This deployment would cause model regression." -ForegroundColor Red
    Write-Host ""
    Write-Host "Fix: Ensure arcade_app/agent.py defaults to 'gemini-2.5-flash'" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Model configuration verified (gemini-2.5-flash)" -ForegroundColor Green
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

# Vertex AI environment variables for gemini-2.5-flash
$envVars = @(
    "VERTEX_PROJECT_NUMBER=$ProjectNumber",
    "VERTEX_REGION=us-central1",
    "VERTEX_MODEL_ID=gemini-2.5-flash"
) -join ","

Write-Host "Locked Environment Variables:" -ForegroundColor Cyan
Write-Host "  VERTEX_PROJECT_NUMBER=$ProjectNumber" -ForegroundColor Gray
Write-Host "  VERTEX_REGION=us-central1" -ForegroundColor Gray
Write-Host "  VERTEX_MODEL_ID=gemini-2.5-flash" -ForegroundColor Gray
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
    
    # Configure IAM permissions for Vertex AI
    Write-Host "Configuring Vertex AI permissions..." -ForegroundColor Yellow
    Write-Host ""
    
    # Enable Vertex AI API
    Write-Host "Enabling Vertex AI API..." -ForegroundColor Cyan
    gcloud services enable aiplatform.googleapis.com --project=$ProjectId
    
    # Get the service account
    $serviceAccount = gcloud run services describe $ServiceName `
        --project=$ProjectId `
        --region=$Region `
        --format='value(spec.template.spec.serviceAccountName)'
    
    if (-not $serviceAccount) {
        $serviceAccount = "$ProjectNumber-compute@developer.gserviceaccount.com"
        Write-Host "Using default compute service account: $serviceAccount" -ForegroundColor Gray
    } else {
        Write-Host "Using service account: $serviceAccount" -ForegroundColor Gray
    }
    
    # Grant Vertex AI User role
    Write-Host "Granting roles/aiplatform.user..." -ForegroundColor Cyan
    gcloud projects add-iam-policy-binding $ProjectId `
        --member="serviceAccount:$serviceAccount" `
        --role="roles/aiplatform.user" `
        --condition=None 2>&1 | Out-Null
    
    # Grant Service Usage Consumer role
    Write-Host "Granting roles/serviceusage.serviceUsageConsumer..." -ForegroundColor Cyan
    gcloud projects add-iam-policy-binding $ProjectId `
        --member="serviceAccount:$serviceAccount" `
        --role="roles/serviceusage.serviceUsageConsumer" `
        --condition=None 2>&1 | Out-Null
    
    Write-Host "✓ IAM permissions configured" -ForegroundColor Green
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
