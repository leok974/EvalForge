# MCP DevDiag Integration

Automated UI diagnostics for EvalForge using [MCP DevDiag](https://github.com/modelcontextprotocol/devdiag).

## Overview

DevDiag provides automated detection and diagnosis of common web UI issues:
- **CSP violations**: Inline scripts, missing nonces, blocked resources
- **Embed compatibility**: iframe sandboxing, CORS, postMessage issues  
- **Chat streaming**: SSE connection problems, event parsing errors
- **Performance**: Slow renders, bundle size, resource loading

## Architecture

```
┌─────────────────┐       ┌──────────────────┐       ┌─────────────────┐
│   GitHub CI     │──────▶│  DevDiag Server  │◀──────│    Dev UI       │
│  (PR checks)    │  JWT  │  (localhost:8023)│  JWT  │ (/ops/diag btn) │
└─────────────────┘       └──────────────────┘       └─────────────────┘
        │                          │                           │
        │                          ▼                           │
        │                   ┌─────────────┐                   │
        │                   │  Playwright  │                   │
        │                   │  Diagnostics │                   │
        │                   └─────────────┘                   │
        │                          │                           │
        ▼                          ▼                           ▼
  ┌──────────────────────────────────────────────────────────────┐
  │              EvalForge FastAPI Backend                       │
  │  ┌────────────────────────────────────────────────────┐     │
  │  │  arcade_app/routers/ops_diag.py                    │     │
  │  │  - POST /ops/diag (run diagnostics)                │     │
  │  │  - GET  /ops/health (router status)                │     │
  │  └────────────────────────────────────────────────────┘     │
  │  ┌────────────────────────────────────────────────────┐     │
  │  │  arcade_app/devdiag_client.py                      │     │
  │  │  - devdiag_quickcheck(url, preset, tenant)         │     │
  │  │  - devdiag_remediation(problem, fix, confidence)   │     │
  │  └────────────────────────────────────────────────────┘     │
  └──────────────────────────────────────────────────────────────┘
```

## Files

### Configuration
- **`ops/devdiag.yaml`** - DevDiag server config (RBAC, allowlist, presets, learning, export)

### Backend
- **`arcade_app/devdiag_client.py`** - Async HTTP client for DevDiag API
- **`arcade_app/routers/ops_diag.py`** - FastAPI operations router
- **`arcade_app/agent.py`** - Mounts ops router at `/ops`

### Frontend  
- **`apps/web/src/pages/DevUI.tsx`** - "Run DevDiag" button in dev interface

### CI/CD
- **`.github/workflows/devdiag-quickcheck.yml`** - PR diagnostic checks
- **`.github/workflows/devdiag-canary.yml`** - Hourly production monitoring

### Documentation
- **`docs/devdiag-secrets.md`** - GitHub secrets setup guide (you are here)

## Quick Start

### 1. Install DevDiag Package

```bash
pip install "mcp-devdiag[playwright,export]==0.2.1"
```

Or add to `requirements.txt`:
```
mcp-devdiag[playwright,export]==0.2.1
```

### 2. Start DevDiag Server (Local Development)

```bash
# Using config file
devdiag serve --config ops/devdiag.yaml

# Or with inline config
devdiag serve --port 8023 --disable-auth
```

Server will start at `http://localhost:8023`

### 3. Configure GitHub Secrets (CI Only)

See [`docs/devdiag-secrets.md`](./devdiag-secrets.md) for detailed setup:

- `DEVDIAG_BASE` - Server URL
- `DEVDIAG_READER_JWT` - Read token for diagnostics
- `DEVDIAG_OPERATOR_JWT` - Write token for learning
- `EVALFORGE_PREVIEW_URL` - PR preview URL pattern
- `EVALFORGE_CANARY_URL` - Production healthz endpoint

### 4. Test Integration

```bash
# Start EvalForge server (existing VS Code task)
# Server runs at http://127.0.0.1:19010

# Open Dev UI
open http://127.0.0.1:19010/

# Click "Run DevDiag" button in header
# Should show toast notification with results
```

## Usage

### Manual Diagnostics (Dev UI)

1. Open http://127.0.0.1:19010/
2. Click **"Run DevDiag"** button in header toolbar
3. View results in:
   - Toast notification (success/error)
   - Event log panel (detailed output)
   - Browser console (full response)

### Programmatic API

```python
from arcade_app.devdiag_client import devdiag_quickcheck

# Run diagnostics
result = await devdiag_quickcheck(
    url="https://evalforge.app",
    preset="app",  # or "embed", "chat", "full"
    tenant="evalforge"
)

# Check result
if result["status"] == "ok":
    print("✅ All checks passed")
else:
    print(f"❌ Issues found: {result['issues']}")
```

### CI/CD Workflows

**PR Quickchecks** (`devdiag-quickcheck.yml`)
- Triggers on PR open/update
- Runs diagnostics on preview URL
- Posts results as PR comment
- Fails CI if issues found

**Hourly Canary** (`devdiag-canary.yml`)
- Runs every hour at :07
- Monitors production health
- Creates GitHub issue on failure
- Auto-closes issue when fixed

## Presets

Configured in `ops/devdiag.yaml`:

| Preset | Checks | Use Case |
|--------|--------|----------|
| `app` | CSP, bundle size, accessibility | General app health |
| `embed` | iframe sandbox, CORS, postMessage | Embed compatibility |
| `chat` | SSE streaming, event parsing | Chat functionality |
| `full` | All of the above | Comprehensive audit |

## Learning Mode

DevDiag can learn from successful remediations:

```python
from arcade_app.devdiag_client import devdiag_remediation

# After fixing a CSP issue
await devdiag_remediation(
    problem_code="CSP_INLINE_BLOCKED",
    fix_code="FIX_CSP_NONCE",
    confidence=0.9
)
```

Requires:
- PostgreSQL database (configured in `ops/devdiag.yaml`)
- `DEVDIAG_OPERATOR_JWT` with write permissions
- Tenant identifier for multi-tenant deployments

## Troubleshooting

### "Connection refused" errors

DevDiag server not running. Start with:
```bash
devdiag serve --config ops/devdiag.yaml
```

### "401 Unauthorized" in CI

GitHub secrets not configured. See [`docs/devdiag-secrets.md`](./devdiag-secrets.md).

### DevDiag button missing

Rebuild UI:
```bash
npm --prefix apps/web run build
```

### No results in event log

1. Open browser console (F12)
2. Check network tab for `/ops/diag` request
3. Verify DevDiag server is reachable
4. Check server logs for errors

## Configuration

### RBAC (Role-Based Access Control)

`ops/devdiag.yaml`:
```yaml
rbac:
  jwks_url: "https://auth.example.com/.well-known/jwks.json"  # Optional
  required_claims:
    tenant: "evalforge"
```

For local dev, comment out `rbac` section to disable authentication.

### Allowlist

Only URLs matching these patterns can be diagnosed:
```yaml
allowlist:
  - "evalforge.app"
  - "evalforge.int"
  - "localhost:19010"
  - "localhost:5173"
```

### Export to S3

Save screenshots and HAR files:
```yaml
export:
  s3_bucket: "mcp-devdiag-artifacts"
  s3_region: "us-east-1"
```

Requires AWS credentials in environment.

## Development

### Running Tests

```bash
# Backend tests
pytest arcade_app/tests/test_devdiag.py

# Smoke test ops router
curl -X POST http://127.0.0.1:19010/ops/diag \
  -H "Content-Type: application/json" \
  -d '{"target_url": "http://127.0.0.1:19010", "preset": "app"}'

# Health check
curl http://127.0.0.1:19010/ops/health
```

### Adding New Presets

Edit `ops/devdiag.yaml`:
```yaml
diag:
  presets:
    my_custom_preset:
      checks:
        - csp_policy
        - bundle_size
        - my_custom_check
      thresholds:
        bundle_size_kb: 500
```

Then use in API:
```python
result = await devdiag_quickcheck(url, preset="my_custom_preset")
```

## Security

- **JWT tokens**: Store in GitHub secrets, never commit
- **Allowlist**: Restricts diagnostic targets to known domains
- **RBAC**: Separate read (quickcheck) vs write (remediation) permissions
- **Audit logs**: All diagnostic runs logged to PostgreSQL (if configured)

## References

- [MCP DevDiag GitHub](https://github.com/modelcontextprotocol/devdiag)
- [GitHub Secrets Setup](./devdiag-secrets.md)
- [FastAPI Router Pattern](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Playwright Documentation](https://playwright.dev/)

## Support

Issues with DevDiag integration? Check:
1. Server logs: `devdiag serve --debug`
2. FastAPI logs: `EVALFORGE_EVENT_LOG=1 uvicorn ...`
3. Browser console: F12 → Network tab
4. GitHub Actions logs: Failed workflow runs

For DevDiag server issues, see upstream docs.
