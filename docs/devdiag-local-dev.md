# DevDiag Local Development Notes

## What is MCP DevDiag?

`mcp-devdiag` is a **Model Context Protocol (MCP) server** that provides diagnostic capabilities for web applications. It runs as an STDIO-based server (not HTTP), designed to be called by MCP clients.

## Current Setup

✅ **Package installed**: `mcp-devdiag[playwright,export]==0.2.1`  
✅ **Config file**: `ops/devdiag.yaml`  
✅ **EvalForge integration**: `/ops/diag` endpoint ready

## Why No Local Server?

DevDiag is an **MCP server** (like LSP for IDEs), not a standalone HTTP API. It's meant to be:
1. **Embedded in tools** (VS Code extensions, CLI tools)
2. **Called via MCP protocol** (JSON-RPC over STDIO)
3. **Deployed as HTTP wrapper** (requires custom server code)

## How It Works in EvalForge

### Production Flow:
```
PR opened → GitHub Actions → Calls remote DevDiag HTTP API → Posts results to PR
```

### Dev UI Flow:
```
User clicks "Run DevDiag" → POST /ops/diag → Calls DEVDIAG_BASE HTTP API → Returns results
```

### What You Need:
- **For CI**: Configure `DEVDIAG_BASE` GitHub secret to point to deployed DevDiag HTTP server
- **For Local**: Set `DEVDIAG_BASE=http://your-devdiag-server.com` env var

## Deployment Options

### Option 1: Cloud Run (Recommended)
Deploy a FastAPI wrapper around mcp-devdiag:
```python
from fastmcp import FastMCP
from mcp_devdiag import app as devdiag_app

# Wrap MCP server in HTTP
app = FastMCP(devdiag_app)
app.run_http(port=8080)
```

### Option 2: Use Existing Service
Point to an existing DevDiag deployment:
```bash
export DEVDIAG_BASE=https://devdiag.yourcompany.com
```

### Option 3: Mock for Development
The `/ops/diag` endpoint gracefully fails if `DEVDIAG_BASE` is not set, allowing you to develop without DevDiag running locally.

## Current Status

✅ **Backend ready**: `/ops/diag` endpoint implemented  
✅ **Frontend ready**: "Run DevDiag" button in Dev UI  
✅ **CI ready**: GitHub Actions workflows configured  
⏳ **Server needed**: Deploy DevDiag HTTP wrapper or use mock responses

## Testing Without DevDiag Server

The button will show an error toast if DevDiag is unavailable, which is fine for local development. All other features (chat, streaming, agents) work independently.

## Production Deployment

When ready to deploy DevDiag:
1. Deploy HTTP wrapper (FastAPI + mcp-devdiag)
2. Set `DEVDIAG_BASE` GitHub secret
3. Workflows will automatically start running diagnostics on PRs
4. Hourly canary will monitor production
