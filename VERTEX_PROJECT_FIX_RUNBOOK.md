# Vertex AI Project Validation Fix - Complete Runbook

## Problem

The Vertex AI 404 errors were caused by using an invalid concatenated project identifier format (`evalforge-1063529378`) instead of a valid GCP project ID (`evalforge`) or project number (`1063529378`).

### Root Causes
1. **Invalid project format**: Used `evalforge-1063529378` which is neither a valid project ID nor project number
2. **GCP project ID rules**: Must be lowercase letters, digits, hyphens; starts with letter; 6–30 chars
3. **GCP project number rules**: Must be 6-20 digits only
4. **Concatenated format**: Invalid for Vertex AI resource paths

## Solution Overview

Added comprehensive project validation at startup with fail-fast behavior, rejecting invalid formats and providing helpful error messages.

## Changes Made

### 1. Code Patch: Project Validation (`arcade_app/agent.py`)

**Added helper functions:**
- `_is_project_id(v: str)`: Validates GCP project ID format
- `_is_project_number(v: str)`: Validates GCP project number format  
- `_looks_like_concat(v: str)`: Detects invalid concatenated format

**Validation logic:**
```python
if GENAI_PROVIDER == "vertex":
    # Reject concatenated format
    if not GOOGLE_CLOUD_PROJECT or _looks_like_concat(GOOGLE_CLOUD_PROJECT):
        raise RuntimeError(
            f"[startup] Invalid GOOGLE_CLOUD_PROJECT='{GOOGLE_CLOUD_PROJECT}'. "
            "Use the project ID (e.g. 'evalforge') OR the numeric project number (e.g. '1063529378'), not both."
        )
    
    # Validate format
    if not (_is_project_id(GOOGLE_CLOUD_PROJECT) or _is_project_number(GOOGLE_CLOUD_PROJECT)):
        raise RuntimeError(
            f"[startup] GOOGLE_CLOUD_PROJECT must be a valid project ID or number (got '{GOOGLE_CLOUD_PROJECT}')."
        )
```

**Result:** Server fails fast with helpful error message if project format is invalid.

### 2. Local Tasks: Use Project Number (`.vscode/tasks.json`)

**Changed:**
- `serve:local`: `$env:GOOGLE_CLOUD_PROJECT='1063529378'`
- `adk:dev`: `$env:GOOGLE_CLOUD_PROJECT='1063529378'`

**Alternative:** Can use project ID `'evalforge'` instead of number.

### 3. Cloud Run Deployment: Use Project Number (`manual_deploy.ps1`)

**Changed:**
```powershell
param(
    [string]$ProjectId = "1063529378",  # Was: "evalforge-1063529378"
    # ...
)

$env:GOOGLE_CLOUD_PROJECT = "1063529378"
```

**Environment variables passed to Cloud Run:**
- `GOOGLE_CLOUD_PROJECT=1063529378` (or `evalforge`)
- `VERTEX_LOCATION=us-east5`
- `GENAI_MODEL=gemini-1.5-flash-002`

### 4. E2E Tests: Project Validation (`tests/test_vertex_project_guard.py`)

**New comprehensive tests:**
- `test_rejects_concatenated_project()`: Verifies server fails with `evalforge-1063529378`
- `test_local_ok_with_project_number()`: Verifies server starts with `1063529378`
- `test_local_ok_with_project_id()`: Verifies server starts with `evalforge`

**Run tests:**
```powershell
D:/EvalForge/.venv/Scripts/python.exe tests/test_vertex_project_guard.py
```

### 5. Curl Smoke Tests (`scripts/curl_smoke.ps1`)

**New automated smoke test script:**
```powershell
# Test local only
pwsh scripts/curl_smoke.ps1 -Environment local

# Test production only
pwsh scripts/curl_smoke.ps1 -Environment prod

# Test both (default)
pwsh scripts/curl_smoke.ps1
```

**Tests performed:**
- Discovery endpoint (`/list-apps`)
- Session creation (`/apps/arcade_app/users/user/sessions`)

## Quick Start

### 1. Discover Your Project Values (One-time)

```powershell
# Get project ID
gcloud config get-value project
# Output: evalforge

# Get project number
gcloud projects describe $(gcloud config get-value project) --format="value(projectNumber)"
# Output: 1063529378
```

**Choose one consistently:**
- Project ID: `evalforge`
- Project Number: `1063529378`

### 2. Run Local Server

```powershell
# Option A: VS Code task
# Press Ctrl+Shift+P → "Tasks: Run Task" → "adk:dev"

# Option B: PowerShell script
pwsh scripts/dev.ps1

# Option C: Manual command
$env:GENAI_PROVIDER='vertex'
$env:GOOGLE_CLOUD_PROJECT='1063529378'  # or 'evalforge'
$env:VERTEX_LOCATION='us-east5'
$env:GENAI_MODEL='gemini-1.5-flash-002'
D:/EvalForge/.venv/Scripts/python.exe -m google.adk.cli web . --host 0.0.0.0 --port 19000
```

### 3. Verify Local Server

```powershell
# Quick curl tests
curl -s "http://127.0.0.1:19000/list-apps?relative_path=arcade_app"
curl -s -X POST -H "Content-Length: 0" "http://127.0.0.1:19000/apps/arcade_app/users/user/sessions"

# Or use automated smoke test
pwsh scripts/curl_smoke.ps1 -Environment local
```

**Expected output:**
- Discovery: JSON with `arcade_app` in response
- Session: JSON with `appName` and `id` fields

### 4. Run E2E Tests

```powershell
# Run all project validation tests
D:/EvalForge/.venv/Scripts/python.exe tests/test_vertex_project_guard.py

# Run all test suites
D:/EvalForge/.venv/Scripts/python.exe tests/test_vertex_config.py
D:/EvalForge/.venv/Scripts/python.exe tests/test_env_model.py
$env:PYTHONPATH="D:\EvalForge"; D:/EvalForge/.venv/Scripts/python.exe tests/test_agent_loads.py
```

### 5. Deploy to Production

```powershell
# Deploy with updated configuration
./manual_deploy.ps1

# Wait 5-10 minutes for deployment to complete
```

### 6. Verify Production

```powershell
# Quick curl tests
$BASE="https://evalforge-agents-uc7hnhrrkq-uc.a.run.app"
curl -s "$BASE/list-apps?relative_path=arcade_app"
curl -s -X POST -H "Content-Length: 0" "$BASE/apps/arcade_app/users/user/sessions"

# Or use automated smoke test
pwsh scripts/curl_smoke.ps1 -Environment prod

# Check Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=evalforge-agents" --limit=20 --format="table(timestamp,textPayload)" --freshness=10m --order=desc
```

## IAM & ADC Setup (Idempotent)

```powershell
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com --project evalforge

# Set up local ADC
gcloud auth application-default login
gcloud auth application-default set-quota-project evalforge

# Grant Cloud Run service account Vertex AI User role
$sa = (gcloud run services describe evalforge-agents --region us-central1 --format="value(spec.template.spec.serviceAccountName)")
gcloud projects add-iam-policy-binding evalforge --member "serviceAccount:$sa" --role roles/aiplatform.user
```

**Note:** IAM commands use project ID (`evalforge`), even if environment variables use project number.

## Verification Checklist

- [ ] Local server starts without errors
- [ ] Startup logs show: `[startup] provider=vertex project=1063529378 region=us-east5 model=gemini-1.5-flash-002`
- [ ] No "Invalid GOOGLE_CLOUD_PROJECT" errors
- [ ] Local curl tests pass (discovery + session)
- [ ] E2E tests pass (all 3 project validation tests)
- [ ] Production deployed successfully
- [ ] Production curl tests pass
- [ ] Cloud Run logs show correct project configuration
- [ ] Judge agent works end-to-end (test with debounce exercise)

## Troubleshooting

### Error: "Invalid GOOGLE_CLOUD_PROJECT='evalforge-1063529378'"

**Problem:** Using concatenated format  
**Solution:** Change to `1063529378` (number) or `evalforge` (ID)

### Error: "GOOGLE_CLOUD_PROJECT must be a valid project ID or number"

**Problem:** Invalid characters or format  
**Solution:** Use only lowercase letters, digits, hyphens (ID) or digits only (number)

### Error: Server starts but 404 errors from Vertex AI

**Problem:** Likely wrong region or model  
**Solution:** Verify:
- `VERTEX_LOCATION=us-east5` (not us-central1)
- `GENAI_MODEL=gemini-1.5-flash-002`

### Local tests pass but production fails

**Problem:** Environment variables not updated in Cloud Run  
**Solution:** 
1. Verify `manual_deploy.ps1` has correct project value
2. Redeploy: `./manual_deploy.ps1`
3. Check Cloud Run environment variables in console

## Reference Commands

### Check Current Configuration

```powershell
# View environment variables
gcloud run services describe evalforge-agents --region us-central1 --format="value(spec.template.spec.containers[0].env)"

# View service account
gcloud run services describe evalforge-agents --region us-central1 --format="value(spec.template.spec.serviceAccountName)"

# View IAM policy
gcloud projects get-iam-policy evalforge --flatten="bindings[].members" --filter="bindings.members:serviceAccount:*compute@*"
```

### Test Individual Endpoints

```powershell
# Local
curl http://127.0.0.1:19000/list-apps?relative_path=arcade_app | jq
curl -X POST http://127.0.0.1:19000/apps/arcade_app/users/user/sessions | jq

# Production
curl https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/list-apps?relative_path=arcade_app | jq
curl -X POST https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/apps/arcade_app/users/user/sessions | jq
```

## Files Changed

1. `arcade_app/agent.py` - Added project validation
2. `.vscode/tasks.json` - Updated project to `1063529378`
3. `manual_deploy.ps1` - Updated project to `1063529378`
4. `tests/test_vertex_project_guard.py` - New E2E tests
5. `scripts/curl_smoke.ps1` - New smoke test script
6. `VERTEX_PROJECT_FIX_RUNBOOK.md` - This document

## Summary

**Before:** `evalforge-1063529378` (invalid concatenated format)  
**After:** `1063529378` (valid project number) or `evalforge` (valid project ID)

**Result:** Server validates project format at startup, fails fast with helpful errors, and works correctly with both local and production Vertex AI endpoints.
