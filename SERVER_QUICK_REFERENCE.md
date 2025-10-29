# Server Management Quick Reference

## VS Code Tasks (Recommended)

Access via: **Terminal → Run Task** or `Ctrl+Shift+P` → "Tasks: Run Task"

### Server Tasks
- **`adk:dev`** - Start local ADK dev server (dedicated terminal, port 19000)
  - Opens in persistent terminal
  - UI available at: http://127.0.0.1:19000/dev-ui/

### Health Check Tasks
- **`health:local`** - Check local server endpoints
  - Tests discovery and session creation
  - Reports status with ✓/✗

- **`health:prod`** - Check production Cloud Run endpoints
  - Tests production deployment
  - Reports status with ✓/✗

- **`logs:cloudrun`** - Fetch recent Cloud Run logs
  - Last 20 entries
  - 10-minute freshness window

### Quick Workflows

**Start & Verify:**
1. Run Task: `adk:dev`
2. Wait ~5 seconds for startup
3. Run Task: `health:local`
4. Run Task: `health:prod`

**Check Logs:**
- Run Task: `logs:cloudrun`

---

## PowerShell Scripts (Alternative)

### Start Server
```powershell
pwsh scripts/dev.ps1
```
- Launches ADK server in dedicated terminal
- Port 19000, all interfaces (0.0.0.0)

### Health Checks
```powershell
pwsh scripts/health.ps1
```
- Checks both local and production endpoints
- Shows ✓/✗ status for each check

---

## Manual Commands

### Start Server (Manual)
```powershell
$env:GENAI_PROVIDER="vertex"
$env:GOOGLE_CLOUD_PROJECT="evalforge-1063529378"
$env:VERTEX_LOCATION="us-central1"
$env:GENAI_MODEL="gemini-1.5-flash-002"
D:/EvalForge/.venv/Scripts/python.exe -m google.adk.cli web . --host 0.0.0.0 --port 19000
```

### Local Checks (Manual)
```powershell
# Discovery
curl -sf "http://127.0.0.1:19000/list-apps?relative_path=arcade_app"

# Session
Invoke-WebRequest -Uri "http://127.0.0.1:19000/apps/arcade_app/users/user/sessions" -Method POST
```

### Production Checks (Manual)
```powershell
# Discovery
curl -sf "https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/list-apps?relative_path=arcade_app"

# Session
Invoke-WebRequest -Uri "https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/apps/arcade_app/users/user/sessions" -Method POST
```

### Cloud Run Logs (Manual)
```powershell
gcloud logging read `
  'resource.type="cloud_run_revision" AND resource.labels.service_name="evalforge-agents"' `
  --limit=20 `
  --format='table(timestamp,textPayload)' `
  --freshness=10m `
  --order=desc
```

---

## URLs

### Local Development
- **Dev UI:** http://127.0.0.1:19000/dev-ui/
- **API Base:** http://127.0.0.1:19000
- **Discovery:** http://127.0.0.1:19000/list-apps?relative_path=arcade_app
- **Sessions:** http://127.0.0.1:19000/apps/arcade_app/users/user/sessions

### Production (Cloud Run)
- **Dev UI:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/dev-ui/
- **API Base:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app
- **Discovery:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/list-apps?relative_path=arcade_app
- **Sessions:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/apps/arcade_app/users/user/sessions

---

## Environment Variables

Required for local server:
```powershell
GENAI_PROVIDER=vertex
GOOGLE_CLOUD_PROJECT=evalforge-1063529378
VERTEX_LOCATION=us-central1
GENAI_MODEL=gemini-1.5-flash-002
```

---

## Troubleshooting

### Server won't start
```powershell
# Check if port 19000 is in use
Get-NetTCPConnection -LocalPort 19000 -ErrorAction SilentlyContinue

# Kill process if needed
Stop-Process -Id (Get-NetTCPConnection -LocalPort 19000).OwningProcess -Force
```

### Health checks fail
```powershell
# Verify server is running
curl -sf "http://127.0.0.1:19000/health" 2>&1

# Check server logs in the adk:dev terminal
```

### Production issues
```powershell
# Check Cloud Run service status
gcloud run services describe evalforge-agents --region=us-central1

# View recent logs
pwsh scripts/health.ps1  # Will show prod status
```

---

## Related Files

- `.vscode/tasks.json` - VS Code task definitions
- `scripts/dev.ps1` - Server startup script
- `scripts/health.ps1` - Health check script
- `manual_deploy.ps1` - Production deployment
- `fast_rollback.ps1` - Emergency rollback

---

**Last Updated:** October 28, 2025  
**Server Port:** 19000  
**Production URL:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app
