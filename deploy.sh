#!/bin/bash
# Deploy EvalForge to Google Cloud Run
# Usage: ./deploy.sh

set -e  # Exit on error

# ========================================
# Configuration - UPDATE THESE VALUES
# ========================================
PROJECT_ID=""  # e.g., "my-project-123456"
REGION="us-central1"  # e.g., "us-central1", "us-east1", "europe-west1"
SERVICE_NAME="evalforge-agents"
APP_NAME="evalforge"
SA_EMAIL=""  # Optional: Service account email (leave empty to use default)

# ========================================
# Validation
# ========================================
if [ -z "$PROJECT_ID" ]; then
    echo "❌ ERROR: PROJECT_ID is not set. Please edit deploy.sh and set your Google Cloud Project ID."
    exit 1
fi

echo "========================================"
echo "EvalForge Cloud Run Deployment"
echo "========================================"
echo "Project ID:     $PROJECT_ID"
echo "Region:         $REGION"
echo "Service Name:   $SERVICE_NAME"
echo "App Name:       $APP_NAME"
if [ -n "$SA_EMAIL" ]; then
    echo "Service Acct:   $SA_EMAIL"
fi
echo "========================================"
echo ""

# ========================================
# Activate Virtual Environment
# ========================================
echo "Activating virtual environment..."
if [ ! -d ".venv" ]; then
    echo "❌ ERROR: Virtual environment not found. Run: python3 -m venv .venv"
    exit 1
fi
source .venv/bin/activate

# ========================================
# Verify ADK Installation
# ========================================
echo "Verifying google-adk installation..."
if ! python -c "import google.adk" 2>/dev/null; then
    echo "❌ ERROR: google-adk is not installed. Run: pip install google-adk"
    exit 1
fi
ADK_VERSION=$(python -c "import google.adk; print(google.adk.__version__)")
echo "✓ google-adk version: $ADK_VERSION"
echo ""

# ========================================
# Check gcloud CLI
# ========================================
echo "Checking gcloud CLI..."
if ! command -v gcloud &> /dev/null; then
    echo "⚠️  WARNING: gcloud CLI not found. Install from: https://cloud.google.com/sdk/docs/install"
    echo "You can still try the deployment, but it may fail."
    echo ""
else
    GCLOUD_VERSION=$(gcloud version --format="value(version)" 2>/dev/null || echo "unknown")
    echo "✓ gcloud CLI version: $GCLOUD_VERSION"
    
    # Check authentication
    CURRENT_ACCOUNT=$(gcloud config get-value account 2>/dev/null || echo "")
    if [ -z "$CURRENT_ACCOUNT" ]; then
        echo "⚠️  WARNING: Not authenticated with gcloud. Run: gcloud auth login"
    else
        echo "✓ Authenticated as: $CURRENT_ACCOUNT"
    fi
    echo ""
fi

# ========================================
# Build Deploy Command
# ========================================
DEPLOY_CMD="adk deploy cloud_run --project=\"$PROJECT_ID\" --region=\"$REGION\" --service_name=\"$SERVICE_NAME\" --app_name=\"$APP_NAME\" --with_ui"

if [ -n "$SA_EMAIL" ]; then
    DEPLOY_CMD="$DEPLOY_CMD --service_account=\"$SA_EMAIL\""
fi

DEPLOY_CMD="$DEPLOY_CMD ."

# ========================================
# Confirmation
# ========================================
echo "About to run:"
echo "$DEPLOY_CMD"
echo ""
read -p "Continue with deployment? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo "========================================"
echo "Starting Deployment..."
echo "========================================"
echo ""

# ========================================
# Deploy
# ========================================
eval $DEPLOY_CMD

# ========================================
# Result
# ========================================
echo ""
echo "========================================"
echo "✓ Deployment Successful!"
echo "========================================"
echo ""
echo "Your service should be available at:"
echo "https://$SERVICE_NAME-<hash>-$REGION.a.run.app"
echo ""
echo "To view your service:"
echo "gcloud run services describe $SERVICE_NAME --project=$PROJECT_ID --region=$REGION"
