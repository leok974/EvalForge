# Vertex AI Quick Runbook

**Use this runbook only in EvalForge workspace**

## 🚀 Quick Start (Local Development)

### 1. Start Local Server
```powershell
# Run the adk:dev VS Code task (Ctrl+Shift+P → "Tasks: Run Task" → "adk:dev")
# OR manually:
$env:GENAI_PROVIDER='vertex'
$env:GOOGLE_CLOUD_PROJECT='evalforge'  # or '291179078777'
$env:VERTEX_LOCATION='us-east5'
$env:GENAI_MODEL='gemini-1.5-flash-002'
python -m google.adk.cli web . --host 0.0.0.0 --port 19000
```

### 2. Verify Local Works
```powershell
pwsh scripts/smoke.ps1 -Env local
# Expected output:
# ✓ discovery passed
# ✓ session passed
```

## 🔧 Troubleshooting Local 404/403

**If Dev UI shows 404/403 popup:**

❌ **DO NOT** change code first!

✅ **DO THIS** instead:

```powershell
# 1. Set ADC quota project to match your configuration
gcloud auth application-default set-quota-project evalforge

# 2. Test again
pwsh scripts/smoke.ps1 -Env local

# 3. If still failing, verify ADC is logged in
gcloud auth application-default login
gcloud auth application-default set-quota-project evalforge
```

### Common Causes
- **ADC pointing to wrong project**: Your local ADC credentials reference a different project than `GOOGLE_CLOUD_PROJECT` env var
- **Vertex API not enabled**: Enable with `gcloud services enable aiplatform.googleapis.com --project=evalforge`

## ☁️ Production Verification

```powershell
pwsh scripts/smoke.ps1 -Env prod -Base https://evalforge-agents-291179078777.us-central1.run.app
# Expected output:
# ✓ discovery passed
# ✓ session passed
```

## 🔧 Troubleshooting Production 403

**If production returns 403 CONSUMER_INVALID:**

```powershell
# 1. Get the service account
$sa = (gcloud run services describe evalforge-agents --region us-central1 --format="value(spec.template.spec.serviceAccountName)")

# 2. Grant Vertex AI permissions
gcloud projects add-iam-policy-binding evalforge `
  --member="serviceAccount:$sa" `
  --role="roles/aiplatform.user"

# 3. Grant service usage permissions
gcloud projects add-iam-policy-binding evalforge `
  --member="serviceAccount:$sa" `
  --role="roles/serviceusage.serviceUsageConsumer"

# 4. Test again
pwsh scripts/smoke.ps1 -Env prod -Base https://evalforge-agents-291179078777.us-central1.run.app
```

## 📋 Valid Configuration Values

### Project
- ✅ `evalforge` (project ID)
- ✅ `291179078777` (project number)
- ❌ `evalforge-1063529378` (REJECTED - concatenated format)

### Region (Vertex Location)
- ✅ `us-east5` (Gemini models available)
- ✅ `europe-west4` (Gemini models available)
- ✅ `asia-southeast1` (Gemini models available)
- ❌ `us-central1` (Gemini NOT available)

### Model
- ✅ `gemini-1.5-flash-002` (versioned, stable)
- ⚠️ `gemini-1.5-flash` (unversioned, may change)

## 🧪 Testing Stack

```powershell
# Local smoke test
pwsh scripts/smoke.ps1 -Env local

# Production smoke test
pwsh scripts/smoke.ps1 -Env prod -Base <cloud-run-url>

# E2E test (launches ephemeral server)
python tests/test_vertex_e2e.py

# Project validation tests
python tests/test_vertex_project_guard.py
```

## 🚢 Deployment

```powershell
# Deploy with automatic IAM configuration
./manual_deploy.ps1

# This will:
# 1. Build and deploy to Cloud Run
# 2. Enable aiplatform.googleapis.com API
# 3. Grant roles/aiplatform.user to service account
# 4. Grant roles/serviceusage.serviceUsageConsumer
```

## 📊 Configuration Files

| File | Purpose |
|------|---------|
| `arcade_app/agent.py` | Single source of truth, validation logic |
| `.vscode/tasks.json` | Local dev server configuration |
| `manual_deploy.ps1` | Production deployment with IAM setup |
| `scripts/smoke.ps1` | Unified smoke tests (local + prod) |
| `tests/test_vertex_e2e.py` | End-to-end integration tests |

## 🎯 Quick Reference

**Start local server:**
```powershell
# Via VS Code task
Ctrl+Shift+P → "Tasks: Run Task" → "adk:dev"
```

**Test local:**
```powershell
pwsh scripts/smoke.ps1 -Env local
```

**Test prod:**
```powershell
pwsh scripts/smoke.ps1 -Env prod -Base https://evalforge-agents-291179078777.us-central1.run.app
```

**Fix local ADC:**
```powershell
gcloud auth application-default set-quota-project evalforge
```

**Fix prod IAM:**
```powershell
$sa = (gcloud run services describe evalforge-agents --region us-central1 --format="value(spec.template.spec.serviceAccountName)")
gcloud projects add-iam-policy-binding evalforge --member="serviceAccount:$sa" --role="roles/aiplatform.user"
```

---

**Last Updated:** October 28, 2025  
**Status:** ✅ Both local and production verified working
