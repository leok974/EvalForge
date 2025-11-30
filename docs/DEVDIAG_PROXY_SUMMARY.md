# DevDiag Proxy Implementation Summary

## Completed Tasks

### 1. Environment Configuration ✅
- Updated `.vscode/tasks.json` with:
  - `DEVDIAG_BASE=http://127.0.0.1:8023`
  - `DEVDIAG_JWT=` (empty for local dev)

### 2. E2E Testing ✅
- Created `apps/web/tests/e2e/devdiag-proxy.spec.ts`
- Tests cover:
  - Health check (graceful degradation)
  - Diagnostic endpoint (200 or 503)
  - Request validation (422 for invalid requests)
  - Invalid JSON handling

### 3. Proxy Hardening ✅

**SSRF Protection:**
```python
ALLOWED_HOSTS = {
    "127.0.0.1",
    "localhost",
    "evalforge.app",
    "evalforge.int",
    "evalforge-agents-uc7hnhrrkq-uc.a.run.app",
}
```
- Validates target URLs against allowlist
- Returns 400 for disallowed hosts

**Retry Logic:**
- Max 2 retries for 502/503/504 errors
- Exponential backoff with jitter: `(2^attempt) + random(0,1)`
- Immediate retry for timeouts and connection errors

**Improved Logging:**
- Redacts JWT in logs: `Bearer ********...`
- Logs target URL, preset, duration, attempt count
- Logs upstream response status and errors

### 4. Metrics ✅

Added to `arcade_app/metrics.py`:
```python
DEVDIAG_REQUESTS_TOTAL = Counter(
    "devdiag_requests_total",
    ["status"]  # success|timeout|upstream_5xx|bad_request|ssrf_blocked
)

DEVDIAG_DURATION_SECONDS = Histogram(
    "devdiag_duration_seconds",
    buckets=[1.0, 5.0, 10.0, 30.0, 60.0, 120.0]
)

DEVDIAG_ERRORS_TOTAL = Counter(
    "devdiag_errors_total",
    ["reason"]  # timeout|upstream_5xx|bad_request|ssrf_blocked|connection_error
)
```

Integrated into `apps/api/routes/devdiag_proxy.py`:
- Records all request outcomes
- Tracks duration for successful diagnostics
- Categorizes errors by type

### 5. UI Integration ✅

Updated `apps/web/src/pages/DevUI.tsx`:
- Imports `runDevDiag` from `lib/devdiag.ts`
- Uses standardized client utility
- Consistent error handling with toast notifications

## Files Modified

1. `.vscode/tasks.json` - Added DevDiag environment variables
2. `apps/api/routes/devdiag_proxy.py` - Added hardening (allowlist, retries, metrics, logging)
3. `arcade_app/metrics.py` - Added DevDiag metrics
4. `apps/web/src/pages/DevUI.tsx` - Integrated DevDiag client utility
5. `apps/web/tests/e2e/devdiag-proxy.spec.ts` - Created E2E tests

## Files Created

1. `docs/DEVDIAG_TROUBLESHOOTING.md` - Comprehensive troubleshooting guide
2. `scripts/verify-devdiag-proxy.ps1` - Quick verification script

## Quick Start

### 1. Start DevDiag Server (Local)

```powershell
.\.venv\Scripts\python.exe -m mcp_devdiag serve `
  --config ops/devdiag.yaml `
  --host 127.0.0.1 `
  --port 8023 `
  --log-level info
```

### 2. Start EvalForge Backend

Use the VS Code task: "EvalForge: Dev Server (Judge/Coach/Greeter + MCP)"

Or manually:
```powershell
D:/EvalForge/.venv/Scripts/python.exe -m uvicorn arcade_app.agent:app --port 19010 --reload
```

### 3. Verify Setup

```powershell
# Health check
curl http://127.0.0.1:19010/api/ops/diag/health

# Run diagnostic
curl -X POST http://127.0.0.1:19010/api/ops/diag `
  -H "Content-Type: application/json" `
  -d '{"url":"http://127.0.0.1:19010/healthz","preset":"app"}'

# Or run automated verification
.\scripts\verify-devdiag-proxy.ps1
```

### 4. Test via UI

1. Open http://127.0.0.1:19010
2. Click "Run DevDiag" button in header
3. Check toast notifications and log output

## Security Features

1. **JWT Server-Side Only:** Tokens never exposed to frontend
2. **SSRF Protection:** Target URLs validated against allowlist
3. **JWT Redaction:** Authentication tokens redacted in logs
4. **Rate Limiting:** Proxies 429 responses from DevDiag server
5. **Timeout Protection:** 120s timeout prevents long-running requests

## Resilience Features

1. **Graceful Degradation:** Returns 503 when DevDiag not configured
2. **Retry Logic:** Automatically retries transient failures (502/503/504)
3. **Circuit Breaking:** Stops after MAX_RETRIES attempts
4. **Error Propagation:** Preserves upstream error codes and messages
5. **Health Checks:** Separate endpoint for monitoring

## Observability

### Logs
```bash
# Enable debug logging
EVALFORGE_EVENT_LOG=1

# Search logs
grep "DevDiag" logs/server.log
```

### Metrics
```bash
# Check Prometheus metrics
curl http://127.0.0.1:19010/metrics | grep devdiag
```

Example output:
```
devdiag_requests_total{status="success"} 5.0
devdiag_requests_total{status="ssrf_blocked"} 1.0
devdiag_duration_seconds_bucket{le="5.0"} 3.0
devdiag_errors_total{reason="timeout"} 0.0
```

## Testing

### Unit Tests (Playwright)
```bash
npm test -- devdiag-proxy.spec.ts
```

### Smoke Tests
```bash
# Automated verification
.\scripts\verify-devdiag-proxy.ps1

# Manual smoke test (from docs/devdiag-smoke.sh)
bash scripts/devdiag-smoke.sh
```

## Production Deployment

### Environment Variables
```bash
DEVDIAG_BASE=https://devdiag.example.com  # Required
DEVDIAG_JWT=eyJhbGci...                   # Optional
```

### GitHub Secrets
```bash
gh secret set DEVDIAG_BASE --body "https://devdiag.example.com"
gh secret set DEVDIAG_READER_JWT --body "eyJhbGci..."
gh secret set DEVDIAG_OPERATOR_JWT --body "eyJhbGci..."
```

### Allowlist Configuration

Add production domains to `apps/api/routes/devdiag_proxy.py`:
```python
ALLOWED_HOSTS = {
    "127.0.0.1",
    "localhost",
    "evalforge.app",
    "your-production-domain.com",  # Add here
}
```

## Monitoring

### Health Check
```bash
curl https://evalforge.app/api/ops/diag/health
```

### Metrics Endpoint
```bash
curl https://evalforge.app/metrics | grep devdiag
```

### CI/CD Integration

- **PR Checks:** `.github/workflows/devdiag-quickcheck.yml`
- **Hourly Canary:** `.github/workflows/devdiag-canary.yml`

Both workflows updated to use new `/api/ops/diag` endpoint.

## Troubleshooting

See `docs/DEVDIAG_TROUBLESHOOTING.md` for comprehensive guide.

Quick fixes:
- **401/403:** Check JWT or use `--disable-auth` for local dev
- **CORS:** Add origin to `ops/devdiag.yaml` allowlist
- **502/503:** Verify DevDiag server is running on correct port
- **400 SSRF:** Add target host to `ALLOWED_HOSTS`
- **504:** Use simpler preset or increase timeout

## Next Steps

1. ✅ Environment configured
2. ✅ Proxy hardened with security features
3. ✅ Metrics and logging integrated
4. ✅ E2E tests created
5. ✅ UI button wired
6. ⏳ Run verification script
7. ⏳ Test with live DevDiag server
8. ⏳ Deploy to production

## References

- `docs/devdiag.md` - Main integration documentation
- `docs/DEVDIAG_TROUBLESHOOTING.md` - Troubleshooting guide
- `docs/AGENT_ENGINE_VERIFICATION.md` - Agent Engine setup
- `apps/web/src/lib/devdiag.ts` - Frontend client utility
- `apps/api/routes/devdiag_proxy.py` - Backend proxy implementation
