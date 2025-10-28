# EvalForge Troubleshooting Guide

Quick reference for common issues and their solutions.

---

## 🔴 Model 404 Error: "Publisher Model not found"

### Symptoms
```
404 NOT_FOUND. Publisher Model `projects/evalforge-1063529378/locations/us-central1/
publishers/google/models/gemini-1.5-flash` was not found
```

### Root Causes & Solutions

#### 1. Using Unversioned Model (Most Common)
**Problem:** Code or environment using `gemini-1.5-flash` instead of `gemini-1.5-flash-002`

**Check:**
```bash
# Cloud Run environment
gcloud run services describe evalforge-agents --region us-central1 \
  --format="value(spec.template.spec.containers[0].env)" | grep GENAI_MODEL

# Should show: name: GENAI_MODEL, value: gemini-1.5-flash-002
```

**Fix:**
```bash
gcloud run services update evalforge-agents \
  --region=us-central1 \
  --set-env-vars="GENAI_MODEL=gemini-1.5-flash-002"
```

#### 2. Traffic on Old Revision
**Problem:** Latest revision has correct config but traffic still goes to old revision

**Check:**
```bash
# View revisions and traffic split
gcloud run services describe evalforge-agents --region us-central1 \
  --format="yaml(status.traffic)"
```

**Fix:**
```bash
# Pin all traffic to latest revision
gcloud run services update-traffic evalforge-agents \
  --region=us-central1 \
  --to-latest
```

#### 3. Region Mismatch
**Problem:** `VERTEX_LOCATION` doesn't match actual Cloud Run region or model availability

**Check:**
```bash
# Verify region configuration
gcloud run services describe evalforge-agents --region us-central1 \
  --format="value(spec.template.spec.containers[0].env)" | grep VERTEX_LOCATION

# Check Model Garden for availability
# Visit: https://console.cloud.google.com/vertex-ai/model-garden
```

**Fix:**
Ensure `VERTEX_LOCATION` matches where model is available (usually `us-central1`)

---

## 🔴 403 Permission Denied Error

### Symptoms
```
403 PERMISSION_DENIED. Permission 'aiplatform.endpoints.predict' denied
```

### Root Causes & Solutions

#### 1. Missing IAM Role
**Problem:** Service account lacks Vertex AI User role

**Check:**
```bash
# Get service account email
SA_EMAIL=$(gcloud run services describe evalforge-agents \
  --region=us-central1 \
  --format='value(spec.template.spec.serviceAccountName)')

echo "Service Account: $SA_EMAIL"

# Check IAM roles
gcloud projects get-iam-policy evalforge-1063529378 \
  --flatten="bindings[].members" \
  --filter="bindings.members:$SA_EMAIL" \
  --format="table(bindings.role)"
```

**Fix:**
```bash
gcloud projects add-iam-policy-binding evalforge-1063529378 \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/aiplatform.user"
```

#### 2. Vertex AI API Not Enabled
**Problem:** Vertex AI API not enabled for project

**Check:**
```bash
gcloud services list --enabled --filter="name:aiplatform.googleapis.com"
```

**Fix:**
```bash
gcloud services enable aiplatform.googleapis.com
```

---

## 🔴 Local ADC Error: "Could not automatically determine credentials"

### Symptoms
```
DefaultCredentialsError: Could not automatically determine credentials.
Please set GOOGLE_APPLICATION_CREDENTIALS or explicitly create credentials
```

### Solutions

#### Option 1: Application Default Credentials (Recommended)
```bash
gcloud auth application-default login
```

#### Option 2: Explicit Credentials File
```bash
# Create service account key (development only!)
gcloud iam service-accounts keys create ~/key.json \
  --iam-account=YOUR_SA_EMAIL

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS=~/key.json  # Linux/Mac
$env:GOOGLE_APPLICATION_CREDENTIALS="$HOME\key.json"  # Windows PowerShell
```

#### Option 3: Switch to Plan B (Google AI API)
See `docs/PLAN_B_GOOGLE_AI_API.md` for using API key instead of ADC

---

## 🔴 "No agents found in current folder"

### Symptoms
Local server shows "No agents found" or "Failed to load agents"

### Solutions

#### 1. Wrong Directory Structure
**Problem:** Running `adk web` command incorrectly

**Fix:**
```bash
# Run from project root with current directory as argument
cd D:\EvalForge
adk web . --port 19000

# NOT: adk web arcade_app --port 19000
```

#### 2. Missing __init__.py
**Problem:** Agent directory missing `__init__.py` file

**Check:**
```bash
ls arcade_app/__init__.py  # Should exist
```

**Fix:**
```bash
touch arcade_app/__init__.py  # Create if missing
```

---

## 🔴 Tests Failing After Deployment

### Symptoms
CI smoke tests fail after deployment

### Troubleshooting Steps

#### 1. Check Service Health
```bash
BASE_URL=$(gcloud run services describe evalforge-agents \
  --region=us-central1 --format='value(status.url)')

# Test basic connectivity
curl -sf "$BASE_URL/list-apps?relative_path=arcade_app"

# Test session creation  
curl -sf -X POST -H "Content-Length: 0" \
  "$BASE_URL/apps/arcade_app/users/user/sessions"
```

#### 2. Check Logs for Errors
```bash
# Recent errors
gcloud logging read \
  'resource.type="cloud_run_revision"
   AND resource.labels.service_name="evalforge-agents"
   AND severity>=ERROR' \
  --limit=20 \
  --format='value(timestamp,textPayload)'

# Startup logs
gcloud logging read \
  'resource.type="cloud_run_revision"
   AND resource.labels.service_name="evalforge-agents"
   AND textPayload:"[startup]"' \
  --limit=5 \
  --format='value(textPayload)'
```

#### 3. Verify Environment Variables
```bash
gcloud run services describe evalforge-agents \
  --region=us-central1 \
  --format="yaml(spec.template.spec.containers[0].env)"
```

---

## 🔴 Model Regression (Reverted to Unversioned)

### Symptoms
After deployment, system uses `gemini-1.5-flash` instead of `-002`

### Investigation

#### 1. Check Code Defaults
```bash
# Verify code default
grep "gemini-1.5-flash" arcade_app/agent.py

# Should show: or "gemini-1.5-flash-002"
```

#### 2. Check Environment Variables
```bash
# Production
gcloud run services describe evalforge-agents --region us-central1 \
  --format="value(spec.template.spec.containers[0].env)" | grep GENAI_MODEL

# Local
echo $GENAI_MODEL  # Linux/Mac
echo $env:GENAI_MODEL  # Windows PowerShell
```

#### 3. Run Guardrail Test
```bash
cd D:\EvalForge
python tests/test_env_model.py

# Should output: ✅ Model correctly defaults to: gemini-1.5-flash-002
```

### Prevention
- ✅ Guardrail test runs in CI
- ✅ Deploy script locks environment variables
- ✅ Code defaults to versioned model

---

## 🟡 High Latency / Slow Responses

### Possible Causes

1. **Cold Start:** First request after idle takes longer
2. **Network Issues:** Check Cloud Run region vs. Vertex AI region
3. **Model Loading:** Initial model warmup

### Solutions

#### Minimize Cold Starts
```bash
# Set minimum instances (costs more, faster responses)
gcloud run services update evalforge-agents \
  --region=us-central1 \
  --min-instances=1
```

#### Check Response Times
```bash
# Time a request
time curl -X POST -H "Content-Length: 0" \
  "$BASE_URL/apps/arcade_app/users/user/sessions"
```

---

## 🟡 Rate Limiting / Quota Errors

### Symptoms
```
429 TOO_MANY_REQUESTS or RESOURCE_EXHAUSTED
```

### Solutions

1. **Check Vertex AI Quotas:**
   - Visit: https://console.cloud.google.com/iam-admin/quotas
   - Filter: "Vertex AI"
   - Look for: "Generate Content requests per minute"

2. **Implement Retry with Backoff** (already in code via tenacity)

3. **Consider Quota Increase:**
   ```bash
   # Request quota increase in Cloud Console
   # Or contact Google Cloud Support
   ```

4. **Switch to Plan B Temporarily:**
   See `docs/PLAN_B_GOOGLE_AI_API.md`

---

## 📋 Quick Diagnostic Commands

### Full Health Check
```bash
# Get service URL
BASE_URL=$(gcloud run services describe evalforge-agents \
  --region=us-central1 --format='value(status.url)')

# Check all endpoints
echo "=== List Apps ==="
curl -sf "$BASE_URL/list-apps?relative_path=arcade_app" || echo "FAILED"

echo "=== Create Session ==="
curl -sf -X POST -H "Content-Length: 0" \
  "$BASE_URL/apps/arcade_app/users/user/sessions" || echo "FAILED"

echo "=== Environment Check ==="
gcloud run services describe evalforge-agents --region=us-central1 \
  --format="yaml(spec.template.spec.containers[0].env)" | \
  grep -E "GENAI|VERTEX|GOOGLE_CLOUD_PROJECT"

echo "=== Recent Errors ==="
gcloud logging read \
  'resource.type="cloud_run_revision"
   AND resource.labels.service_name="evalforge-agents"
   AND severity>=ERROR' \
  --limit=5 --format='value(timestamp,textPayload)'
```

### Local Development Check
```powershell
# Windows PowerShell
$env:GENAI_PROVIDER="vertex"
$env:GOOGLE_CLOUD_PROJECT="evalforge-1063529378"
$env:VERTEX_LOCATION="us-central1"
$env:GENAI_MODEL="gemini-1.5-flash-002"

# Test ADC
gcloud auth application-default print-access-token

# Run server
cd D:\EvalForge
D:/EvalForge/.venv/Scripts/adk.exe web . --port 19000
```

---

## 🆘 Emergency Procedures

### System Down - Quick Restore

1. **Rollback to Previous Revision:**
   ```bash
   # List revisions
   gcloud run revisions list --service=evalforge-agents --region=us-central1
   
   # Rollback to previous
   gcloud run services update-traffic evalforge-agents \
     --region=us-central1 \
     --to-revisions=PREVIOUS_REVISION=100
   ```

2. **Switch to Plan B (Google AI API):**
   ```bash
   gcloud run services update evalforge-agents \
     --region=us-central1 \
     --set-env-vars="GENAI_PROVIDER=google,GENAI_MODEL=gemini-1.5-flash-002" \
     --set-secrets="GOOGLE_API_KEY=google-api-key:latest"
   ```

3. **Disable Service Temporarily:**
   ```bash
   gcloud run services update evalforge-agents \
     --region=us-central1 \
     --no-allow-unauthenticated
   ```

---

## 📞 Getting Help

1. **Check Logs:** Always check Cloud Run logs first
2. **Run Tests:** Execute `tests/test_env_model.py`
3. **Verify Config:** Check environment variables in Cloud Run
4. **Review Alerts:** Look for Cloud Logging alerts
5. **Check Status:** https://status.cloud.google.com/

### Useful Links
- Model Garden: https://console.cloud.google.com/vertex-ai/model-garden
- Cloud Run Console: https://console.cloud.google.com/run
- Vertex AI Docs: https://cloud.google.com/vertex-ai/docs
- ADK Documentation: (internal Google documentation)
