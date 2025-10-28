# 🚀 Deploying EvalForge to Google Cloud Run

This guide walks you through deploying your AI Trainer Arcade agents to Google Cloud Run.

## 📋 Prerequisites

### 1. Google Cloud Project
- [ ] Have a Google Cloud Project created
- [ ] Billing enabled on the project
- [ ] Note your Project ID (e.g., `my-project-123456`)

### 2. gcloud CLI Installed
```powershell
# Windows: Download from https://cloud.google.com/sdk/docs/install
# Or use the installer

# Verify installation
gcloud version
```

### 3. Authenticate with Google Cloud
```powershell
# Login to your Google account
gcloud auth login

# Set your project
gcloud config set project YOUR-PROJECT-ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 4. Python Virtual Environment
```powershell
# Already set up in this repo
.\.venv\Scripts\Activate.ps1

# Verify google-adk is installed
pip list | Select-String google-adk
```

## 🔧 Configuration

### Option 1: Edit deploy.ps1 (Recommended)

1. Open `deploy.ps1` in your editor
2. Update these variables at the top:

```powershell
$PROJECT_ID = "your-project-id-here"  # REQUIRED
$REGION = "us-central1"                # Choose your region
$SERVICE_NAME = "evalforge-agents"     # Your service name
$APP_NAME = "evalforge"                # Your app name
$SA_EMAIL = ""                         # Optional: service account email
```

3. Save the file

### Option 2: Manual Command

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Deploy directly
adk deploy cloud_run `
  --project="YOUR-PROJECT-ID" `
  --region="us-central1" `
  --service_name=evalforge-agents `
  --app_name=evalforge `
  --with_ui `
  .
```

## 🚀 Deployment

### Using the Script (Recommended)

```powershell
# Make sure you're in the repo root
cd D:\EvalForge

# Run the deployment script
.\deploy.ps1
```

The script will:
1. ✅ Validate your configuration
2. ✅ Check google-adk installation
3. ✅ Verify gcloud CLI
4. ✅ Show you what will be deployed
5. ✅ Ask for confirmation
6. ✅ Deploy to Cloud Run
7. ✅ Show you the service URL

### Manual Deployment

```powershell
cd D:\EvalForge
.\.venv\Scripts\Activate.ps1

adk deploy cloud_run `
  --project="my-project-123456" `
  --region="us-central1" `
  --service_name=evalforge-agents `
  --app_name=evalforge `
  --with_ui `
  .
```

## 🌐 Available Regions

Choose a region close to your users:

| Region | Location |
|--------|----------|
| `us-central1` | Iowa, USA |
| `us-east1` | South Carolina, USA |
| `us-west1` | Oregon, USA |
| `europe-west1` | Belgium |
| `asia-southeast1` | Singapore |

[Full list of regions](https://cloud.google.com/run/docs/locations)

## 🔐 Service Account (Optional)

If you want to use a custom service account:

```powershell
# Create a service account
gcloud iam service-accounts create evalforge-runner `
  --display-name="EvalForge Agent Runner"

# Get the email
$SA_EMAIL = gcloud iam service-accounts list `
  --filter="displayName:EvalForge Agent Runner" `
  --format="value(email)"

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR-PROJECT-ID `
  --member="serviceAccount:$SA_EMAIL" `
  --role="roles/run.invoker"
```

Then add the email to `deploy.ps1`:
```powershell
$SA_EMAIL = "evalforge-runner@your-project.iam.gserviceaccount.com"
```

## 📊 Post-Deployment

### View Your Service

```powershell
# Get service details
gcloud run services describe evalforge-agents `
  --project=YOUR-PROJECT-ID `
  --region=us-central1

# Get the service URL
gcloud run services describe evalforge-agents `
  --project=YOUR-PROJECT-ID `
  --region=us-central1 `
  --format="value(status.url)"
```

### Access the UI

Your service will be available at:
```
https://evalforge-agents-<hash>-us-central1.a.run.app
```

The UI will be at:
```
https://evalforge-agents-<hash>-us-central1.a.run.app/dev-ui/
```

### View Logs

```powershell
# Stream logs in real-time
gcloud run services logs tail evalforge-agents `
  --project=YOUR-PROJECT-ID `
  --region=us-central1
```

Or view in Cloud Console:
```
https://console.cloud.google.com/run/detail/us-central1/evalforge-agents/logs
```

## 🐛 Troubleshooting

### Error: "Permission denied"

**Solution:** Ensure you're authenticated and have proper permissions:
```powershell
gcloud auth login
gcloud auth application-default login
```

### Error: "API not enabled"

**Solution:** Enable required APIs:
```powershell
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Error: "Billing account not found"

**Solution:** Enable billing in Cloud Console:
1. Go to https://console.cloud.google.com/billing
2. Link a billing account to your project

### Error: "gcloud command not found"

**Solution:** Install gcloud CLI:
- Windows: https://cloud.google.com/sdk/docs/install-sdk#windows
- After install, restart PowerShell

### Deployment is slow

**First deployment:** Can take 5-10 minutes (building container, pushing to registry)
**Subsequent deployments:** Usually 2-3 minutes

### Service returns 404 or errors

**Check logs:**
```powershell
gcloud run services logs tail evalforge-agents --project=YOUR-PROJECT-ID --region=us-central1
```

**Common issues:**
- Missing dependencies in requirements.txt
- Import errors in agent code
- Incorrect file paths

## 🔄 Updating Your Deployment

After making changes to your code:

```powershell
# Just run deploy again
.\deploy.ps1

# Or manually
adk deploy cloud_run --project=YOUR-PROJECT-ID --region=us-central1 --service_name=evalforge-agents --app_name=evalforge --with_ui .
```

Cloud Run will:
1. Build a new container image
2. Push it to Container Registry
3. Deploy the new version
4. Route traffic to the new version
5. Keep the old version for rollback

## 💰 Cost Estimation

Cloud Run charges for:
- CPU and memory while handling requests
- Number of requests
- Data transfer

**Free tier includes:**
- 2 million requests/month
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds

**Typical costs for this app:**
- Light usage (< 1000 req/day): **$0-5/month**
- Medium usage (10,000 req/day): **$10-30/month**

[Cloud Run Pricing Calculator](https://cloud.google.com/products/calculator)

## 🎯 What Gets Deployed

The `adk deploy cloud_run` command will package and deploy:

```
✅ arcade_app/          # Your agent code
✅ exercises/           # Quest exercises
✅ seed/                # Quest configurations
✅ scripts/             # Helper scripts
✅ requirements.txt     # Python dependencies
✅ Web UI               # Interactive testing UI (--with_ui flag)
```

## 🔒 Security Notes

1. **Authentication:** By default, Cloud Run requires authentication. Anyone with the URL and Google account permissions can access it.

2. **Make it public (optional):**
```powershell
gcloud run services add-iam-policy-binding evalforge-agents `
  --region=us-central1 `
  --member="allUsers" `
  --role="roles/run.invoker"
```

3. **Environment variables:** Add secrets via:
```powershell
gcloud run services update evalforge-agents `
  --region=us-central1 `
  --set-env-vars="GEMINI_API_KEY=your-key-here"
```

## 📚 Next Steps

- [ ] Deploy your service
- [ ] Test in the Cloud Run UI
- [ ] Set up CI/CD with GitHub Actions
- [ ] Configure custom domain
- [ ] Set up monitoring and alerts
- [ ] Add authentication for production use

## 🆘 Need Help?

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [ADK Documentation](https://github.com/google/adk)
- [Cloud Run Quickstart](https://cloud.google.com/run/docs/quickstarts)

---

**Ready to deploy?** Edit `deploy.ps1` with your Project ID and run it! 🚀
