# DevDiag Proxy Troubleshooting Guide

Quick reference for common DevDiag proxy issues and fixes.

## Environment Setup

### Local Development

```bash
# .vscode/tasks.json or .env
DEVDIAG_BASE=http://127.0.0.1:8023
DEVDIAG_JWT=
```

### Production

```bash
# Set via environment or GitHub secrets
DEVDIAG_BASE=https://devdiag.example.com
DEVDIAG_JWT=eyJhbGciOiJIUzI1NiIs...
```

## Quick Verification

### 1. Start DevDiag Server (Local)

```powershell
# Windows
.\.venv\Scripts\python.exe -m mcp_devdiag serve `
  --config ops/devdiag.yaml `
  --host 127.0.0.1 `
  --port 8023 `
  --log-level info
```

```bash
# Linux/Mac
python -m mcp_devdiag serve \
  --config ops/devdiag.yaml \
  --host 127.0.0.1 \
  --port 8023 \
  --log-level info
```

### 2. Test Proxy Health

```bash
curl -s http://127.0.0.1:19010/api/ops/diag/health | jq
```

**Expected (DevDiag running):**
```json
{
  "ok": true,
  "message": "DevDiag server is healthy"
}
```

**Expected (DevDiag not running):**
```json
{
  "ok": false,
  "message": "Health check timed out"
}
```

### 3. Run Diagnostic via Proxy

```bash
curl -s -X POST http://127.0.0.1:19010/api/ops/diag \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"http://127.0.0.1:19010/healthz\",\"preset\":\"app\"}" | jq
```

**Expected (Success):**
```json
{
  "ok": true,
  "result": {
    "status": "pass",
    "checks": { ... }
  }
}
```

**Expected (DevDiag not configured):**
```json
{
  "detail": "DevDiag server not configured. Set DEVDIAG_BASE environment variable."
}
```

## Common Issues

### Issue: 401/403 Unauthorized

**Symptoms:**
- Health check returns 403
- Diagnostic requests return 401

**Diagnosis:**
```bash
# Check if DEVDIAG_JWT is required
curl -s http://127.0.0.1:8023/healthz
```

**Fix:**
1. For local dev: Leave `DEVDIAG_JWT` empty
2. Check `ops/devdiag.yaml` RBAC settings
3. If using `--disable-auth` flag, verify it's passed to DevDiag server
4. For production: Set valid JWT token in environment

### Issue: CORS Errors in DevDiag Logs

**Symptoms:**
```
CORS error: Origin 'http://127.0.0.1:19010' not allowed
```

**Fix:**
Edit `ops/devdiag.yaml`:
```yaml
allowlist:
  origins:
    - "http://127.0.0.1:19010"
    - "http://localhost:19010"
    - "https://evalforge.app"
    - "https://*.evalforge.app"
```

Restart DevDiag server after changes.

### Issue: 502/503 Bad Gateway via Proxy

**Symptoms:**
- Health check times out
- Diagnostic returns 503 with "Failed to connect"

**Diagnosis:**
```bash
# 1. Check DevDiag server is running
curl -s http://127.0.0.1:8023/healthz

# 2. Check port is correct in DEVDIAG_BASE
echo $DEVDIAG_BASE  # Should be http://127.0.0.1:8023

# 3. Check firewall (Windows)
Test-NetConnection -ComputerName 127.0.0.1 -Port 8023
```

**Fix:**
1. Start DevDiag server (see command above)
2. Verify port matches `DEVDIAG_BASE`
3. Check firewall rules allow local connections
4. Review DevDiag server logs for errors

### Issue: 400 Target URL Not Allowed (SSRF Protection)

**Symptoms:**
```json
{
  "detail": "Target URL not allowed. Permitted hosts: ..."
}
```

**Fix:**
Edit `apps/api/routes/devdiag_proxy.py`:
```python
ALLOWED_HOSTS = {
    "127.0.0.1",
    "localhost",
    "evalforge.app",
    "your-domain.com",  # Add your domain
}
```

### Issue: 504 Gateway Timeout

**Symptoms:**
- Diagnostic takes > 120 seconds
- Returns 504 timeout error

**Fix:**
1. Use simpler preset: `"chat"` instead of `"full"`
2. Check target URL responds quickly
3. Increase timeout in `devdiag_proxy.py`:
   ```python
   TIMEOUT = 180.0  # 3 minutes
   ```
4. Verify DevDiag server has adequate resources

### Issue: Metrics Not Recording

**Symptoms:**
- `/metrics` endpoint doesn't show `devdiag_*` metrics
- Warning: "Prometheus metrics not available"

**Fix:**
```bash
# Install prometheus_client
pip install prometheus-client

# Restart EvalForge server
```

## Verification Commands

### Check Metrics
```bash
curl -s http://127.0.0.1:19010/metrics | grep devdiag
```

Expected output:
```
devdiag_requests_total{status="success"} 5.0
devdiag_duration_seconds_bucket{le="5.0"} 3.0
devdiag_errors_total{reason="timeout"} 0.0
```

### Test SSRF Protection
```bash
# Should be BLOCKED (not in allowlist)
curl -s -X POST http://127.0.0.1:19010/api/ops/diag \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"http://evil.com\",\"preset\":\"app\"}"
```

Expected: `400 Bad Request` with "Target URL not allowed"

### Test Retry Logic
```bash
# Stop DevDiag server, then:
curl -s -X POST http://127.0.0.1:19010/api/ops/diag \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"http://127.0.0.1:19010\",\"preset\":\"app\"}"
```

Expected: Proxy retries 2 times with exponential backoff, then returns 503

## CI/CD Troubleshooting

### GitHub Actions: Secret Not Found

**Symptoms:**
```
Error: Context access might be invalid: DEVDIAG_BASE
```

**Fix:**
This is a linter warning, not a runtime error. Secrets resolve at runtime:
```bash
# Verify secrets are set
gh secret list

# Should show:
# DEVDIAG_BASE
# DEVDIAG_READER_JWT
# EVALFORGE_PREVIEW_URL
```

### Playwright Tests Failing

**Symptoms:**
- `devdiag-proxy.spec.ts` tests fail
- Health check returns unexpected status

**Fix:**
```bash
# Run tests locally with DEBUG
DEBUG=pw:api npm test -- devdiag-proxy.spec.ts

# Check BASE_URL
BASE_URL=http://127.0.0.1:19010 npm test
```

## Log Analysis

### Enable Debug Logging

```bash
# In .env or task environment
EVALFORGE_EVENT_LOG=1
```

### Search Logs for DevDiag Activity

```bash
# Check proxy logs
grep "DevDiag" logs/server.log

# Expected patterns:
# [DevDiag] Running diagnostic: target_url=...
# [DevDiag] Upstream response: status=200, duration=3.45s
# [DevDiag] Diagnostic completed successfully
```

### Common Log Messages

| Message | Meaning | Action |
|---------|---------|--------|
| "SSRF protection: rejected" | Target URL not in allowlist | Add host to ALLOWED_HOSTS |
| "Timeout, retrying in 1.23s" | Slow response, retrying | Check DevDiag server performance |
| "Upstream error 503, retrying" | DevDiag server busy | Wait or scale DevDiag resources |
| "JWT redacted" | Authentication in use | Normal (JWT hidden in logs) |

## Best Practices

1. **Local Dev:** Run DevDiag server locally for fastest iteration
2. **Production:** Use remote DevDiag service with JWT authentication
3. **Allowlist:** Only add trusted domains to ALLOWED_HOSTS
4. **Monitoring:** Check `/metrics` endpoint regularly
5. **Logging:** Keep EVALFORGE_EVENT_LOG=1 in dev, 0 in prod (unless debugging)
6. **Timeouts:** Start with 120s, adjust based on actual diagnostic duration
7. **Retries:** Keep MAX_RETRIES=2 to balance reliability and latency

## Quick Reference Commands

```bash
# Start everything (Windows)
.\.venv\Scripts\python.exe -m mcp_devdiag serve --config ops/devdiag.yaml --port 8023
D:/EvalForge/.venv/Scripts/python.exe -m uvicorn arcade_app.agent:app --port 19010 --reload

# Health check
curl http://127.0.0.1:19010/api/ops/diag/health

# Run diagnostic
curl -X POST http://127.0.0.1:19010/api/ops/diag \
  -H "Content-Type: application/json" \
  -d '{"url":"http://127.0.0.1:19010","preset":"app"}'

# Check metrics
curl http://127.0.0.1:19010/metrics | grep devdiag

# Playwright test
npm test -- devdiag-proxy.spec.ts
```
