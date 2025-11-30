# DevDiag Integration

Automated UI diagnostics for EvalForge using DevDiag over HTTP.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Local Development](#local-development)
- [Production Setup](#production-setup)
- [Usage](#usage)
- [Security](#security)
- [Monitoring and Observability](#monitoring-and-observability)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

**Quick Links:**
- 🚀 **[DEVDIAG_SANITY_CHECKS.md](./DEVDIAG_SANITY_CHECKS.md)**: Quick verification commands, rollout steps, Grafana queries
- 🔧 **[DEVDIAG_TROUBLESHOOTING.md](./DEVDIAG_TROUBLESHOOTING.md)**: Detailed troubleshooting and error resolutions
- 📋 **[DEVDIAG_PROXY_SUMMARY.md](./DEVDIAG_PROXY_SUMMARY.md)**: Implementation details and verification steps

## Overview

DevDiag provides automated UI diagnostics to detect common web application issues:
- CSP (Content Security Policy) violations
- Embed compatibility problems
- API endpoint availability
- Performance degradation
- Console errors and warnings

EvalForge integrates DevDiag via HTTP proxy architecture, keeping authentication tokens server-side for security.

## Architecture

```
Frontend (Browser)
    |
    | POST /api/ops/diag { url, preset }
    v
Backend Proxy (FastAPI)
    |
    | POST /diag/run (with JWT)
    v
DevDiag HTTP Server
    |
    | Puppeteer/Playwright diagnostics
    v
Result { ok, result/error }
```

**Key Components:**

1. **Backend Proxy** (`apps/api/routes/devdiag_proxy.py`)
   - FastAPI router at `/api/ops/diag`
   - Adds JWT authentication server-side
   - Handles timeouts, rate limiting, error propagation
   - Health check at `/api/ops/diag/health`

2. **Frontend Client** (`apps/web/src/lib/devdiag.ts`)
   - Thin client utility: `runDevDiag(url, preset)`
   - No JWT handling (tokens stay server-side)
   - Graceful error handling

3. **DevDiag HTTP Server** (External Service)
   - Runs Puppeteer/Playwright diagnostics
   - Requires `DEVDIAG_BASE` URL
   - Optional JWT authentication via `DEVDIAG_JWT`

## Local Development

### Prerequisites

- EvalForge backend running (FastAPI on port 19010)
- DevDiag HTTP server (optional for local dev)

### Environment Configuration

Add to `.env`:

```bash
# DevDiag HTTP server base URL (leave empty to disable)
DEVDIAG_BASE=http://127.0.0.1:8080

# DevDiag JWT token (optional, only if server requires auth)
DEVDIAG_JWT=
```

### Running Without DevDiag Server

EvalForge gracefully handles missing DevDiag server:
- Health check returns `ok: false` with message
- Diagnostic requests return `503 Service Unavailable`
- Frontend UI shows appropriate error messages

This allows development without running a separate DevDiag instance.

### Running With Local DevDiag Server

If you have access to a DevDiag HTTP server:

1. Start DevDiag HTTP server (check DevDiag docs for instructions)
2. Set `DEVDIAG_BASE=http://127.0.0.1:8080` (or your server URL)
3. Set `DEVDIAG_JWT` if authentication is required
4. Restart EvalForge backend

Test health check:
```bash
curl http://127.0.0.1:19010/api/ops/diag/health
```

## Production Setup

### Environment Variables

Set in your deployment environment:

```bash
# Required: DevDiag HTTP server URL
DEVDIAG_BASE=https://devdiag.example.com

# Optional: JWT token for authentication
DEVDIAG_JWT=eyJhbGciOiJIUzI1NiIs...
```

### GitHub Secrets

For CI/CD workflows, configure these secrets:

```bash
gh secret set DEVDIAG_BASE --body "https://devdiag.example.com"
gh secret set DEVDIAG_READER_JWT --body "eyJhbGci..."
gh secret set DEVDIAG_OPERATOR_JWT --body "eyJhbGci..."
gh secret set EVALFORGE_PREVIEW_URL --body "https://preview.evalforge.app"
gh secret set EVALFORGE_CANARY_URL --body "https://evalforge.app/healthz"
```

- `DEVDIAG_BASE`: DevDiag HTTP server URL
- `DEVDIAG_READER_JWT`: Read-only token for PR checks
- `DEVDIAG_OPERATOR_JWT`: Full-access token for remediation
- `EVALFORGE_PREVIEW_URL`: PR preview deployment URL
- `EVALFORGE_CANARY_URL`: Production health check URL

## Usage

### Frontend (TypeScript/React)

```typescript
import { runDevDiag, checkDevDiagHealth } from '@/lib/devdiag';

// Check if DevDiag is available
const health = await checkDevDiagHealth();
if (!health.ok) {
  console.warn("DevDiag unavailable:", health.message);
}

// Run diagnostics
try {
  const result = await runDevDiag("https://evalforge.app", "app");
  
  if (result.ok) {
    console.log("✅ Diagnostics passed:", result.result);
  } else {
    console.error("❌ Diagnostics failed:", result.error);
  }
} catch (error) {
  console.error("Request error:", error);
}
```

**Presets:**
- `"chat"`: Chat interface checks (CSP, embed, console errors)
- `"embed"`: Embed compatibility checks
- `"app"`: Full application diagnostics (recommended)
- `"full"`: Extended diagnostics with performance analysis

### Backend (Python/FastAPI)

```python
import httpx
from apps.api.routes.devdiag_proxy import router

# Router is automatically mounted at /api/ops by agent.py
# No manual integration needed

# For custom diagnostic calls:
async with httpx.AsyncClient(timeout=120.0) as client:
    response = await client.post(
        "http://127.0.0.1:19010/api/ops/diag",
        json={"url": "https://evalforge.app", "preset": "app"}
    )
    result = response.json()
    print(result)
```

### CLI (curl)

```bash
# Health check
curl http://127.0.0.1:19010/api/ops/diag/health

# Run diagnostics
curl -X POST http://127.0.0.1:19010/api/ops/diag \
  -H "Content-Type: application/json" \
  -d '{"url": "https://evalforge.app", "preset": "app"}'
```

## Security

### JWT Token Handling

**CRITICAL**: JWT tokens are ONLY handled server-side:
- ✅ Backend reads `DEVDIAG_JWT` from environment
- ✅ Backend adds `Authorization: Bearer $TOKEN` to DevDiag requests
- ❌ Frontend NEVER sees or handles JWT tokens
- ❌ Tokens are NEVER exposed in API responses or logs

### Authentication Flow

```
1. Frontend: POST /api/ops/diag { url, preset }
2. Backend: Adds "Authorization: Bearer $DEVDIAG_JWT"
3. Backend: Proxies to $DEVDIAG_BASE/diag/run
4. DevDiag: Validates JWT, runs diagnostics
5. Backend: Returns { ok, result/error }
6. Frontend: Displays result
```

### Rate Limiting

Backend enforces rate limits:
- 1 request per second per session
- Burst capacity: 5 requests
- Returns `429 Too Many Requests` on rate limit

### Error Handling

Proper error propagation:
- `503`: DevDiag not configured (`DEVDIAG_BASE` not set)
- `504`: Diagnostic timeout (120s exceeded)
- `429`: Rate limit exceeded
- `4xx`/`5xx`: Propagated from DevDiag server

## CI/CD Integration

### PR Quickchecks (`.github/workflows/devdiag-quickcheck.yml`)

Runs on every PR:
- Calls `POST /diag/run` with PR preview URL
- Uses `DEVDIAG_READER_JWT` for read-only access
- Comments results on PR
- Fails PR if diagnostics fail

### Hourly Canary (`.github/workflows/devdiag-canary.yml`)

Runs every hour:
- Monitors production health
- Creates GitHub issue on failure
- Auto-closes issue when canary passes
- Uses `DEVDIAG_READER_JWT` for monitoring

## Monitoring and Observability

### Metrics

The DevDiag proxy exports the following Prometheus metrics:

- **`devdiag_requests_total{status}`**: Counter of all diagnostic requests by status (`ok`, `error`, `rate_limited`)
- **`devdiag_duration_seconds`**: Histogram of diagnostic request durations in seconds
- **`devdiag_errors_total{reason}`**: Counter of errors by reason (`not_configured`, `ssrf_blocked`, `timeout`, `upstream_error`, `rate_limited`)

### Prometheus Query Examples

**Dashboard Panels:**

```promql
# Total request rate (requests per second)
rate(devdiag_requests_total[5m])

# Request rate by status
sum by (status) (rate(devdiag_requests_total[5m]))

# Error rate percentage
100 * (
  sum(rate(devdiag_requests_total{status="error"}[5m])) /
  sum(rate(devdiag_requests_total[5m]))
)

# P95 latency
histogram_quantile(0.95, rate(devdiag_duration_seconds_bucket[5m]))

# P99 latency
histogram_quantile(0.99, rate(devdiag_duration_seconds_bucket[5m]))

# Success rate over time (200-299 responses)
sum(rate(devdiag_requests_total{status="ok"}[5m])) / 
sum(rate(devdiag_requests_total[5m]))

# Errors by reason
sum by (reason) (rate(devdiag_errors_total[5m]))

# Rate limiting impact
rate(devdiag_requests_total{status="rate_limited"}[5m])
```

### Alert Rules

**Example Grafana/Prometheus Alert Rules:**

```yaml
groups:
  - name: devdiag_proxy
    interval: 60s
    rules:
      # High error rate
      - alert: DevDiagHighErrorRate
        expr: |
          100 * (
            sum(rate(devdiag_requests_total{status="error"}[10m])) /
            sum(rate(devdiag_requests_total[10m]))
          ) > 20
        for: 10m
        labels:
          severity: warning
          component: devdiag_proxy
        annotations:
          summary: "DevDiag error rate above 20%"
          description: "DevDiag proxy error rate is {{ $value | humanizePercentage }} (threshold: 20%)"

      # High latency
      - alert: DevDiagHighLatency
        expr: |
          histogram_quantile(0.95, rate(devdiag_duration_seconds_bucket[10m])) > 8
        for: 10m
        labels:
          severity: warning
          component: devdiag_proxy
        annotations:
          summary: "DevDiag P95 latency above 8s"
          description: "DevDiag proxy P95 latency is {{ $value | humanizeDuration }} (threshold: 8s)"

      # Service unavailable
      - alert: DevDiagServiceDown
        expr: |
          sum(rate(devdiag_requests_total[5m])) == 0
        for: 15m
        labels:
          severity: critical
          component: devdiag_proxy
        annotations:
          summary: "DevDiag proxy receiving no requests"
          description: "DevDiag proxy has received no requests for 15 minutes"

      # Excessive rate limiting
      - alert: DevDiagExcessiveRateLimiting
        expr: |
          100 * (
            sum(rate(devdiag_requests_total{status="rate_limited"}[10m])) /
            sum(rate(devdiag_requests_total[10m]))
          ) > 30
        for: 10m
        labels:
          severity: info
          component: devdiag_proxy
        annotations:
          summary: "DevDiag rate limiting >30% of requests"
          description: "{{ $value | humanizePercentage }} of requests are rate limited (threshold: 30%)"

      # SSRF protection triggered frequently
      - alert: DevDiagSSRFBlocked
        expr: |
          rate(devdiag_errors_total{reason="ssrf_blocked"}[10m]) > 1
        for: 5m
        labels:
          severity: warning
          component: devdiag_proxy
        annotations:
          summary: "DevDiag SSRF protection triggered"
          description: "SSRF protection blocking {{ $value | humanize }} requests/sec"
```

**Recommended Dashboard Layout:**

1. **Overview Panel**: Total request rate, success rate, P95 latency
2. **Status Breakdown**: Pie chart of requests by status (ok, error, rate_limited)
3. **Latency Panel**: P50, P95, P99 latencies over time
4. **Error Analysis**: Errors by reason (stacked area chart)
5. **Rate Limiting**: Rate-limited requests over time, percentage rate-limited
6. **Uptime Panel**: Service availability percentage (SLA tracking)

---

## Troubleshooting

For comprehensive troubleshooting guidance, see **[DEVDIAG_TROUBLESHOOTING.md](./DEVDIAG_TROUBLESHOOTING.md)**.

Common issues:

### "DevDiag server not configured"

**Symptom**: `503 Service Unavailable` with message about `DEVDIAG_BASE`

**Fix**: Set `DEVDIAG_BASE` environment variable to your DevDiag HTTP server URL:
```bash
export DEVDIAG_BASE=https://devdiag.example.com
```

### "DevDiag diagnostic timed out"

**Symptom**: `504 Gateway Timeout` after 90 seconds

**Fixes**:
- Use simpler preset: try `"chat"` instead of `"full"`
- Check target URL responds quickly
- Verify DevDiag server has adequate resources

### "Rate limit exceeded"

**Symptom**: `429 Too Many Requests`

**Fix**: Wait at least 15 seconds between requests. Maximum 6 requests per minute per IP/session.

See [DEVDIAG_TROUBLESHOOTING.md](./DEVDIAG_TROUBLESHOOTING.md) for more detailed diagnostics.

## Additional Resources

- [DevDiag MCP Server](https://github.com/evalstate/mcp-devdiag) - Original MCP implementation
- [EvalForge Architecture](./architecture.md) - Overall system design
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) - Managing CI secrets
