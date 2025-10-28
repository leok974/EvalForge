# 🚀 EvalForge Cloud Run Deployment Configuration

## ✅ Current Deployment Status

**Service Name:** `evalforge-agents`
**Project ID:** `evalforge-1063529378`
**Region:** `us-central1`
**Service URL:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app
**Web UI:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/dev-ui/

**Latest Revision:** `evalforge-agents-00004-nhv`
**Status:** ✅ Running with module mode and Vertex AI configuration

## 🔧 Configuration Details

### Dockerfile (Module Mode)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_GENAI_USE_VERTEXAI=True

# Expose port (Cloud Run will set PORT env var)
EXPOSE 8080

# Start ADK server in module mode - MUST bind to 0.0.0.0 for Cloud Run
# Use shell form to allow $PORT variable expansion
ENTRYPOINT python -m google.adk.cli web arcade_app --host 0.0.0.0 --port ${PORT:-8080}
```

**Key Changes from Previous Version:**
- ✅ Uses **module mode** (`arcade_app`) instead of scan mode (`.`)
- ✅ Binds to `0.0.0.0` instead of `127.0.0.1` (allows Cloud Run to connect)
- ✅ Uses `$PORT` environment variable (Cloud Run injects this)
- ✅ Sets `GOOGLE_GENAI_USE_VERTEXAI=True` for Vertex AI integration

### Environment Variables

```bash
GOOGLE_GENAI_USE_VERTEXAI=True        # Use Vertex AI instead of API key
GOOGLE_CLOUD_PROJECT=evalforge-1063529378
GOOGLE_CLOUD_LOCATION=us-central1
EVALFORGE_MODEL=gemini-1.5-flash      # Model to use for agent
```

### Cloud Run Service Settings

- **Memory:** 512 MiB
- **CPU:** 1
- **Timeout:** 300 seconds (5 minutes)
- **Concurrency:** 80 (default)
- **Min instances:** 0 (scales to zero)
- **Max instances:** 100 (default)
- **Authentication:** Allow unauthenticated (public access)

## 📊 Deployment Commands

### Quick Redeploy

```powershell
cd D:\EvalForge
.\manual_deploy.ps1
```

This script:
1. ✅ Creates clean deployment folder
2. ✅ Copies application files
3. ✅ Generates Dockerfile with correct configuration
4. ✅ Deploys to Cloud Run with environment variables
5. ✅ Returns service URL

### Manual Commands

#### Update Environment Variables Only

```powershell
gcloud run services update evalforge-agents `
  --region=us-central1 `
  --project=evalforge-1063529378 `
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_PROJECT=evalforge-1063529378,GOOGLE_CLOUD_LOCATION=us-central1,EVALFORGE_MODEL=gemini-1.5-flash"
```

#### Full Redeploy from Source

```powershell
cd D:\EvalForge\cloud_run_deploy

gcloud run deploy evalforge-agents `
  --source . `
  --project=evalforge-1063529378 `
  --region=us-central1 `
  --platform=managed `
  --allow-unauthenticated `
  --port=8080 `
  --memory=512Mi `
  --timeout=300 `
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_PROJECT=evalforge-1063529378,GOOGLE_CLOUD_LOCATION=us-central1,EVALFORGE_MODEL=gemini-1.5-flash"
```

#### Build and Deploy with Container Registry

```powershell
# Build and push to Container Registry
cd D:\EvalForge\cloud_run_deploy
gcloud builds submit --tag gcr.io/evalforge-1063529378/evalforge-agents:latest

# Deploy from image
gcloud run deploy evalforge-agents `
  --image gcr.io/evalforge-1063529378/evalforge-agents:latest `
  --region us-central1 `
  --project evalforge-1063529378 `
  --allow-unauthenticated `
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_PROJECT=evalforge-1063529378,GOOGLE_CLOUD_LOCATION=us-central1,EVALFORGE_MODEL=gemini-1.5-flash"
```

## 🔍 Monitoring & Debugging

### View Logs

```powershell
# Stream logs in real-time
gcloud run services logs tail evalforge-agents `
  --project=evalforge-1063529378 `
  --region=us-central1

# Read last 50 log entries
gcloud run services logs read evalforge-agents `
  --project=evalforge-1063529378 `
  --region=us-central1 `
  --limit=50
```

### Service Details

```powershell
# Get full service description
gcloud run services describe evalforge-agents `
  --project=evalforge-1063529378 `
  --region=us-central1

# Get just the URL
gcloud run services describe evalforge-agents `
  --project=evalforge-1063529378 `
  --region=us-central1 `
  --format='value(status.url)'

# Get environment variables
gcloud run services describe evalforge-agents `
  --project=evalforge-1063529378 `
  --region=us-central1 `
  --format="yaml(spec.template.spec.containers[0].env)"
```

### Test Endpoints

```powershell
$SERVICE_URL = "https://evalforge-agents-uc7hnhrrkq-uc.a.run.app"

# Test health
curl.exe $SERVICE_URL/

# Test agent listing
curl.exe $SERVICE_URL/list-apps?relative_path=arcade_app

# Open Web UI
Start-Process "$SERVICE_URL/dev-ui/"
```

## 🎯 Module Mode vs Scan Mode

### Module Mode (Current - ✅ Recommended)

```bash
python -m google.adk.cli web arcade_app --host 0.0.0.0 --port 8080
```

**Advantages:**
- ✅ Explicitly loads the `arcade_app` module
- ✅ Faster startup (no filesystem scanning)
- ✅ More reliable (no dependency on file discovery)
- ✅ Works with `arcade_app/__init__.py` exporting `root_agent`

### Scan Mode (Previous)

```bash
python -m google.adk.cli web . --host 0.0.0.0 --port 8080
```

**Disadvantages:**
- ⚠️ Scans current directory for Python files with `root_agent`
- ⚠️ Slower startup
- ⚠️ May not find `arcade.py` if filesystem structure is different in container

## 🔐 Service Account (Optional)

To use a custom service account with specific permissions:

```powershell
# Create service account
gcloud iam service-accounts create evalforge-runner `
  --display-name="EvalForge Agent Runner" `
  --project=evalforge-1063529378

# Grant Vertex AI permissions
gcloud projects add-iam-policy-binding evalforge-1063529378 `
  --member="serviceAccount:evalforge-runner@evalforge-1063529378.iam.gserviceaccount.com" `
  --role="roles/aiplatform.user"

# Update Cloud Run service to use it
gcloud run services update evalforge-agents `
  --region=us-central1 `
  --project=evalforge-1063529378 `
  --service-account="evalforge-runner@evalforge-1063529378.iam.gserviceaccount.com"
```

## 📝 Deployment History

| Revision | Date | Changes |
|----------|------|---------|
| `evalforge-agents-00001-h7h` | 2025-10-14 | Initial deployment - Failed (localhost binding) |
| `evalforge-agents-00002-7bq` | 2025-10-14 | Fixed host binding to 0.0.0.0 - Working |
| `evalforge-agents-00003-d9h` | 2025-10-14 | Added Vertex AI env vars |
| `evalforge-agents-00004-nhv` | 2025-10-14 | ✅ Module mode + Vertex AI (Current) |

## 🐛 Common Issues

### Issue: Container fails to start

**Symptoms:** Deployment succeeds but service shows unhealthy
**Cause:** Server binding to `127.0.0.1` instead of `0.0.0.0`
**Fix:** Ensure Dockerfile uses `--host 0.0.0.0`

### Issue: Agent not found in UI

**Symptoms:** Web UI loads but agent dropdown is empty
**Cause:** Using scan mode (`.`) instead of module mode
**Fix:** Use `web arcade_app` instead of `web .`

### Issue: Vertex AI authentication errors

**Symptoms:** Agent fails when making LLM calls
**Cause:** Missing environment variables or IAM permissions
**Fix:** 
1. Set `GOOGLE_GENAI_USE_VERTEXAI=True`
2. Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`
3. Ensure service account has `roles/aiplatform.user`

### Issue: Deployment takes too long

**Symptoms:** Build step is slow (>5 minutes)
**Cause:** Rebuilding Python dependencies from scratch
**Fix:** Use Container Registry caching:
```powershell
gcloud builds submit --tag gcr.io/evalforge-1063529378/evalforge-agents:latest
```

## 💰 Cost Optimization

Current configuration scales to zero when not in use. Typical costs:

- **Free tier:** 2M requests/month, 360k GB-seconds memory, 180k vCPU-seconds
- **Light usage:** ~$0-5/month (within free tier)
- **Medium usage:** ~$10-20/month

### Reduce Costs

```powershell
# Set min instances to 0 (already default)
gcloud run services update evalforge-agents `
  --region=us-central1 `
  --min-instances=0

# Reduce memory if not needed
gcloud run services update evalforge-agents `
  --region=us-central1 `
  --memory=256Mi
```

## 🔄 Update Workflow

1. **Make code changes** in `D:\EvalForge`
2. **Test locally:**
   ```powershell
   cd D:\EvalForge
   .\.venv\Scripts\Activate.ps1
   adk web arcade_app --host 0.0.0.0 --port 19000
   ```
3. **Deploy to Cloud Run:**
   ```powershell
   .\manual_deploy.ps1
   ```
4. **Test in production:**
   - Open Web UI: https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/dev-ui/
   - Check logs: `gcloud run services logs tail evalforge-agents ...`

## 🎉 Success Criteria

✅ Service is deployed and healthy
✅ Web UI loads at `/dev-ui/`
✅ Agent appears in dropdown (ArcadeOrchestrator)
✅ Can send messages and get responses
✅ Vertex AI integration working (no API key needed)
✅ Costs within free tier

---

**Last Updated:** October 14, 2025
**Deployed By:** manual_deploy.ps1
**Status:** ✅ Production Ready
