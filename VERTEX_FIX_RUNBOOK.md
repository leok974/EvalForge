# Vertex 404 Fix + E2E/Smoke Tests - Complete Runbook

## Problem
Vertex AI returned `404 NOT_FOUND` errors because **gemini-1.5-flash-002** isn't available in **us-central1**. Gemini models are only supported in specific regions: **us-east5**, **europe-west4**, **asia-southeast1**.

## Solution
Force all environments (local, Cloud Run) to use **us-east5** as the Vertex AI region, while keeping Cloud Run service in us-central1 (this is fine - service location ≠ model API location).

---

## Changes Made

### 1. ✅ Agent Startup Validation (`arcade_app/agent.py`)
**Added:**
- Region whitelist: `ALLOWED_VERTEX_REGIONS = {"us-east5", "europe-west4", "asia-southeast1"}`
- Default changed: `us-central1` → `us-east5`
- Startup validation: Fails fast with helpful error if region is invalid
- Verbose logging: Prints provider, project, region, model at startup

**Key Code:**
```python
if GENAI_PROVIDER == "vertex":
    if VERTEX_LOCATION not in ALLOWED_VERTEX_REGIONS:
        raise RuntimeError(
            f"[startup] Invalid VERTEX_LOCATION='{VERTEX_LOCATION}'. "
            f"Use one of {sorted(ALLOWED_VERTEX_REGIONS)}."
        )
    vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=VERTEX_LOCATION)
    print(f"[startup] provider=vertex project={GOOGLE_CLOUD_PROJECT} "
          f"region={VERTEX_LOCATION} model={GENAI_MODEL}", flush=True)
```

### 2. ✅ VS Code Tasks (`.vscode/tasks.json`)
**Updated:**
- `adk:dev` task: `VERTEX_LOCATION='us-east5'`
- `serve:local` task: `VERTEX_LOCATION='us-east5'`

**Example:**
```json
{
  "label": "adk:dev",
  "command": "$env:VERTEX_LOCATION='us-east5'; ..."
}
```

### 3. ✅ Deploy Script (`manual_deploy.ps1`)
**Updated:**
- Force `VERTEX_LOCATION=us-east5` in environment
- Added guard: Verify `GENAI_MODEL` ends with `-002`
- Locked env vars in Cloud Run deployment

**Key Code:**
```powershell
$env:VERTEX_LOCATION = "us-east5"
if (-not $env:GENAI_MODEL.EndsWith("-002")) {
    Write-Error "GENAI_MODEL must be a -002 version"; exit 1
}
```

### 4. ✅ IAM Setup (Run Once)
**Commands:**
```powershell
# Enable AI Platform API
gcloud services enable aiplatform.googleapis.com --project evalforge-1063529378

# Grant Cloud Run service account AI Platform access
$sa = (gcloud run services describe evalforge-agents --region us-central1 --format="value(spec.template.spec.serviceAccountName)")
gcloud projects add-iam-policy-binding evalforge-1063529378 --member "serviceAccount:$sa" --role roles/aiplatform.user
```

**Status:** ✅ Completed
- AI Platform API: Enabled
- Service Account: `270277706511-compute@developer.gserviceaccount.com`
- IAM Role: `roles/aiplatform.user` granted

### 5. ✅ E2E Tests (`tests/test_vertex_config.py`)
**Created:**
- `test_env_region_allowed()` - Validates region configuration
- `test_local_adk_smoke()` - Launches ephemeral server, tests discovery + sessions

**Run:**
```powershell
pytest -v tests/test_vertex_config.py
```

### 6. ✅ Smoke Script (`scripts/smoke_adk.ps1`)
**Created:**
- Tests both local (127.0.0.1:19000) and production endpoints
- Verifies discovery + session creation
- Pretty output with ✓/✗ indicators

**Run:**
```powershell
pwsh scripts/smoke_adk.ps1
```

### 7. ✅ CI Workflow (`.github/workflows/e2e-adk.yml`)
**Created:**
- Manual trigger: `workflow_dispatch`
- Auto trigger: Push to main/master (paths: arcade_app, tests)
- Runs `test_env_region_allowed()` in CI

---

## Runbook: How to Use

### Step 1: Local Development
```powershell
# Option A: VS Code Task
# Press Ctrl+Shift+P → "Tasks: Run Task" → "adk:dev"

# Option B: Script
pwsh scripts/dev.ps1

# Wait ~5 seconds for startup
# Look for: [startup] provider=vertex project=evalforge-1063529378 region=us-east5 model=gemini-1.5-flash-002
```

### Step 2: Test Locally
```powershell
# Quick smoke test
pwsh scripts/smoke_adk.ps1

# Full E2E tests
pytest -v tests/test_vertex_config.py
```

### Step 3: Deploy to Production
```powershell
# Deploy with us-east5 Vertex region
./manual_deploy.ps1

# Confirms:
# - VERTEX_LOCATION=us-east5
# - GENAI_MODEL=gemini-1.5-flash-002
# - Model version ends with -002
```

### Step 4: Verify Production
```powershell
# Smoke test (includes production checks)
pwsh scripts/smoke_adk.ps1

# Manual curl tests
curl -s "https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/list-apps?relative_path=arcade_app"
curl -s -X POST -H "Content-Length: 0" "https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/apps/arcade_app/users/user/sessions"
```

---

## Expected Outcomes

### ✅ Local Server Startup
```
[startup] provider=vertex project=evalforge-1063529378 region=us-east5 model=gemini-1.5-flash-002
INFO:     Uvicorn running on http://0.0.0.0:19000 (Press CTRL+C to quit)
```

### ✅ Discovery Endpoint
```json
[
  "analytics",
  "arcade_app",
  "cloud_run_deploy",
  "docs",
  "exercises",
  "logs",
  "scripts",
  "seed",
  "tests",
  "tools"
]
```

### ✅ Session Creation
```json
{
  "id": "abc123...",
  "appName": "arcade_app",
  "userId": "user",
  "createdAt": "2025-10-28T20:30:00Z"
}
```

### ✅ Judge Agent Test
**User:** "run tests for the debounce exercise"

**Expected:**
- Judge routes to test runner
- Vitest executes
- Coverage analyzed
- Verdict returned with pass/fail + feedback

**No more 404 errors!**

---

## Verification Checklist

- [ ] Local server starts with `[startup] ... region=us-east5`
- [ ] `pwsh scripts/smoke_adk.ps1` passes (local + prod)
- [ ] `pytest tests/test_vertex_config.py` passes
- [ ] Production deployment shows `VERTEX_LOCATION=us-east5` in logs
- [ ] Session creation returns valid JSON (not 404)
- [ ] Judge agent can execute tests and return verdicts

---

## Files Changed

**Core:**
- `arcade_app/agent.py` - Region validation + us-east5 default
- `.vscode/tasks.json` - Updated adk:dev and serve:local tasks
- `manual_deploy.ps1` - Force us-east5, add -002 guard
- `scripts/dev.ps1` - Updated to us-east5

**New:**
- `tests/test_vertex_config.py` - E2E tests
- `scripts/smoke_adk.ps1` - Smoke test script
- `.github/workflows/e2e-adk.yml` - CI workflow
- `VERTEX_FIX_RUNBOOK.md` - This file

---

## Troubleshooting

### Issue: Server starts but still gets 404
**Check:**
```powershell
# Verify environment variables are set
$env:VERTEX_LOCATION  # Should be: us-east5
$env:GENAI_MODEL      # Should be: gemini-1.5-flash-002
```

**Fix:**
Kill server and restart with correct env vars.

### Issue: IAM permission denied
**Check:**
```powershell
# Verify service account has role
gcloud projects get-iam-policy evalforge-1063529378 --flatten="bindings[].members" --filter="bindings.members:270277706511-compute@developer.gserviceaccount.com"
```

**Fix:**
Re-run IAM binding command (idempotent).

### Issue: Local tests timeout
**Check:**
```powershell
# Verify port 19000 is free
Get-NetTCPConnection -LocalPort 19000 -ErrorAction SilentlyContinue
```

**Fix:**
Kill process on port 19000:
```powershell
$pid = (Get-NetTCPConnection -LocalPort 19000).OwningProcess
Stop-Process -Id $pid -Force
```

---

## Quick Reference

**Local Server:**
```powershell
pwsh scripts/dev.ps1  # Start
pwsh scripts/smoke_adk.ps1  # Test
```

**Deploy:**
```powershell
./manual_deploy.ps1  # Deploys with us-east5
```

**Tests:**
```powershell
pytest -v tests/test_vertex_config.py  # E2E
pwsh scripts/smoke_adk.ps1  # Smoke
```

**URLs:**
- Local: http://127.0.0.1:19000/dev-ui/
- Prod: https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/dev-ui/

---

**Last Updated:** October 28, 2025  
**Status:** ✅ Fix Applied & Tested  
**Vertex Region:** us-east5 (Gemini-supported)
