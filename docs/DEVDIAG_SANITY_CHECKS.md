# DevDiag Proxy - Quick Sanity Checks

Fast verification commands for local development and production deployments.

## Local Development

### Prerequisites

- EvalForge backend running on `http://127.0.0.1:19010`
- Optional: DevDiag server running on port 8023 (gracefully degrades if missing)

### Health Check

```powershell
# PowerShell
curl -s http://127.0.0.1:19010/api/ops/diag/health
```

**Expected Responses:**

**DevDiag Configured (DEVDIAG_BASE set):**
```json
{
  "ok": true,
  "message": "DevDiag proxy healthy"
}
```

**DevDiag Not Configured (graceful degradation):**
```json
{
  "ok": false,
  "message": "DEVDIAG_BASE not configured"
}
```

Both responses are valid - `ok: false` indicates graceful degradation.

### Full Diagnostic Run

```powershell
# PowerShell
curl -s -X POST http://127.0.0.1:19010/api/ops/diag `
  -H "content-type: application/json" `
  -d '{"url":"http://127.0.0.1:19010","preset":"app"}' | jq
```

**Expected Response (Success):**
```json
{
  "ok": true,
  "result": {
    "diagnostics": { ... },
    "summary": { ... }
  },
  "playwright_report_url": "https://devdiag.example.com/reports/abc123/index.html",
  "export_tar_url": "https://devdiag.example.com/exports/abc123.tar.gz"
}
```

**Expected Response (No DevDiag Server):**
```json
{
  "detail": "DevDiag server not configured. Set DEVDIAG_BASE environment variable."
}
```
HTTP Status: `503 Service Unavailable`

**Expected Response (Rate Limited):**
```json
{
  "detail": "Rate limit exceeded. Please wait at least 15 seconds between requests (max 6/minute)."
}
```
HTTP Status: `429 Too Many Requests`

---

## Production Deployment

### Prerequisites

- EvalForge deployed to Cloud Run or similar
- GitHub Secrets configured:
  - `DEVDIAG_BASE`: DevDiag server URL
  - `DEVDIAG_JWT`: Authentication token

### Health Check

```bash
# Replace with your production URL
curl -s https://evalforge.app/api/ops/diag/health
```

### Full Diagnostic Run

```bash
curl -s -X POST https://evalforge.app/api/ops/diag \
  -H "Content-Type: application/json" \
  -d '{"url":"https://evalforge.app","preset":"app"}' | jq
```

---

## What You Just Shipped ✅

### Security Hardening
- **SSRF allowlist locked** to `{127.0.0.1, localhost, evalforge.app, evalforge.int}`
- **Timeouts hardened**: `connect=5s, read=90s` (production-ready)
- **Rate limiting**: 6 requests/min per IP/session + 15s cooldown
  - Returns `429 Too Many Requests` with metrics

### Observability
- **Prometheus metrics**: `devdiag_requests_total`, `devdiag_duration_seconds`, `devdiag_errors_total`
- **Dashboard queries documented**: P95 latency, error rate, rate-limited share
- **Alert recipes**: >20% error rate (10m), P95 >8s (10m), canary failures

### UI/UX
- **Dev UI button**: Spinner, disabled state during run
- **Artifact URLs**: Displays `playwright_report_url`, `export_tar_url` in results
- **Toast notifications**: Success/error feedback with artifact links

### CI/CD
- **Playwright spec** added to `ci-smoke-tests.yml` (runs on Linux + Windows)
- **E2E tests**: Health check, diagnostics, validation, degradation scenarios

### Documentation
- **Troubleshooting guide**: [DEVDIAG_TROUBLESHOOTING.md](./DEVDIAG_TROUBLESHOOTING.md)
- **Proxy summary**: [DEVDIAG_PROXY_SUMMARY.md](./DEVDIAG_PROXY_SUMMARY.md)
- **Integration docs**: [devdiag.md](./devdiag.md)
- **README cross-links**: DevDiag section with verification steps

---

## Rollout Steps (Production)

### 1. Configure Secrets

Add to GitHub Actions secrets (Settings → Secrets and variables → Actions):

```bash
# DevDiag server base URL
DEVDIAG_BASE=https://devdiag.example.com

# JWT token for authentication
DEVDIAG_JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Verify secrets are set:
```bash
gh secret list
```

### 2. Deploy EvalForge

Use your normal deployment process:

```powershell
# Windows
.\manual_deploy.ps1

# Or via gcloud
gcloud run services update evalforge-agents \
  --region us-central1 \
  --update-env-vars DEVDIAG_BASE=https://devdiag.example.com \
  --update-env-vars DEVDIAG_JWT=YOUR_JWT_TOKEN
```

### 3. Test in Production

1. Open Dev UI: `https://evalforge.app/dev-ui/`
2. Click **Run DevDiag** button
3. Check for artifact links in Log/toast notifications
4. Verify artifacts are accessible (Playwright reports, export archives)

### 4. Set Up Dashboards

Add panels to Grafana using documented queries:

**Error Rate (5m window):**
```promql
(sum(rate(devdiag_errors_total[5m])) / sum(rate(devdiag_requests_total[5m]))) * 100
```

**P95 Latency (5m window):**
```promql
histogram_quantile(0.95, sum by (le) (rate(devdiag_duration_seconds_bucket[5m])))
```

**Rate-Limited Share:**
```promql
sum(rate(devdiag_requests_total{status="rate_limited"}[5m])) / sum(rate(devdiag_requests_total[5m]))
```

### 5. Create Alerts

Configure alerts in Grafana/Prometheus:

- **High error rate**: >20% for 10 minutes
- **High latency**: P95 >8s for 10 minutes
- **Service down**: No requests for 15 minutes
- **Excessive rate limiting**: >30% requests rate-limited for 10 minutes
- **SSRF attacks**: >1 blocked request/sec for 5 minutes

See [devdiag.md](./devdiag.md#alert-rules) for complete alert configurations.

---

## Fast Grafana Checks (Copy/Paste)

### Error Rate (5m)
```promql
(sum(rate(devdiag_errors_total[5m])) / sum(rate(devdiag_requests_total[5m]))) * 100
```

### P95 Latency (5m)
```promql
histogram_quantile(0.95, sum by (le) (rate(devdiag_duration_seconds_bucket[5m])))
```

### Rate-Limited Share
```promql
sum(rate(devdiag_requests_total{status="rate_limited"}[5m])) / sum(rate(devdiag_requests_total[5m]))
```

### Requests by Status (Breakdown)
```promql
sum by (status) (rate(devdiag_requests_total[5m]))
```

### Errors by Reason (Breakdown)
```promql
sum by (reason) (rate(devdiag_errors_total[5m]))
```

---

## Nice Follow-Ups (Tiny Improvements)

### 1. Env-Driven Allowlist
Move hardcoded host set to environment variable for blue/green deploys:

```python
# Instead of hardcoded:
ALLOWED_HOSTS = {"127.0.0.1", "localhost", "evalforge.app", "evalforge.int"}

# Use env var:
ALLOWED_HOSTS = set(os.getenv("DEVDIAG_ALLOWED_HOSTS", "127.0.0.1,localhost").split(","))
```

**Benefits:**
- Stage-specific allowlists (staging vs production)
- No code changes for new domains
- Easier blue/green deployments

### 2. Per-Tenant Metrics
Add tenant label for multi-brand support:

```python
DEVDIAG_REQUESTS_TOTAL.labels(status="ok", tenant="evalforge").inc()
```

**Benefits:**
- Isolate metrics per brand
- Track usage by tenant
- Better cost allocation

### 3. UI Toast "Open Report" Button
Already plumbed—ensure artifact URLs are clickable:

```typescript
// In DevUI.tsx, enhance artifact message display
if (result.playwright_report_url) {
  push({ 
    kind: "success", 
    title: "DevDiag completed",
    text: "View report",
    action: {
      label: "Open Report",
      onClick: () => window.open(result.playwright_report_url, "_blank")
    }
  });
}
```

**Benefits:**
- One-click access to reports
- Better UX for developers
- Faster debugging workflow

---

## Troubleshooting Common Issues

### Health Check Returns 503
**Cause**: `DEVDIAG_BASE` not configured  
**Fix**: Set environment variable:
```bash
export DEVDIAG_BASE=https://devdiag.example.com
```

### Diagnostic Returns 429
**Cause**: Rate limit exceeded (>6 requests/min or <15s since last request)  
**Fix**: Wait at least 15 seconds between requests

### No Artifact URLs in Response
**Cause**: DevDiag server doesn't return artifact URLs  
**Fix**: 
1. Verify DevDiag version supports `playwright_report_url`/`export_tar_url`
2. Check DevDiag server configuration for artifact storage
3. Review server logs for artifact generation errors

### SSRF Protection Blocks Valid Request
**Cause**: Target host not in allowlist  
**Fix**: Add host to `ALLOWED_HOSTS` in `devdiag_proxy.py` or use env var approach

For detailed troubleshooting, see [DEVDIAG_TROUBLESHOOTING.md](./DEVDIAG_TROUBLESHOOTING.md).

---

## Quick Reference

| Check | Local | Production |
|-------|-------|------------|
| **Health** | `curl -s http://127.0.0.1:19010/api/ops/diag/health` | `curl -s https://evalforge.app/api/ops/diag/health` |
| **Diagnostic** | `curl -s -X POST http://127.0.0.1:19010/api/ops/diag -H "content-type: application/json" -d '{"url":"http://127.0.0.1:19010","preset":"app"}'` | `curl -s -X POST https://evalforge.app/api/ops/diag -H "Content-Type: application/json" -d '{"url":"https://evalforge.app","preset":"app"}'` |
| **Metrics** | `curl -s http://127.0.0.1:19010/metrics \| grep devdiag` | `curl -s https://evalforge.app/metrics \| grep devdiag` |

**Rate Limits:**
- 6 requests per minute per IP/session
- Minimum 15 seconds between requests
- Returns `429 Too Many Requests` when exceeded

**Timeouts:**
- Connect: 5 seconds
- Read: 90 seconds
- Write: 5 seconds
- Pool: 5 seconds

**SSRF Protection:**
- Allowlist: `127.0.0.1`, `localhost`, `evalforge.app`, `evalforge.int`
- Returns `400 Bad Request` for blocked hosts
