# VS Code Tasks Quick Reference

This workspace now includes production-ready VS Code tasks for development and testing workflows.

## Available Tasks

Run tasks via:
- **Command Palette**: `Ctrl+Shift+P` → "Tasks: Run Task" → select task
- **Terminal Menu**: Terminal → Run Task
- **Keyboard**: Configure custom keybindings in `keybindings.json`

### Development Tasks

| Task | Description | Output |
|------|-------------|--------|
| `serve:local` | Start local ADK server (background) | Terminal: SERVER group<br>Log: `logs/server.local.log` |
| `smoke:local` | Test local server endpoints | Terminal: CHECKS group<br>Log: `logs/smoke.local.log` |
| `smoke:cloud` | Test Cloud Run production endpoints | Terminal: CHECKS group<br>Log: `logs/smoke.cloud.log` |
| `smoke:all` | Start server + run both smoke tests | Sequential execution |
| `test:guardrail` | Run model version guardrail test | Terminal: CHECKS group<br>Log: `logs/test.guardrail.log` |

### Deployment Tasks

| Task | Description | Output |
|------|-------------|--------|
| `deploy:cloud` | Deploy to Cloud Run (runs `manual_deploy.ps1`) | Terminal: DEPLOY group |
| `rollback:fast` | Emergency rollback (runs `fast_rollback.ps1`) | Terminal: DEPLOY group |

### Legacy Tasks (Preserved)

| Task | Description |
|------|-------------|
| `Run: Vitest (logged)` | Run Vitest tests with logging |
| `Run: ADK web (logged)` | Start ADK server with log wrapper |
| `Run: Pytest (logged)` | Run Python tests with logging |
| `Run: Judge Agent Test (logged)` | Test judge agent functionality |
| `Analyze Error Patterns` | Run error aggregation tool |

## Launch Configurations (F5)

Available debug configurations:

1. **App (attach) – web**
   - Launches Chrome browser at `http://127.0.0.1:19000/dev-ui/`
   - Pre-starts local server with `serve:local` task
   - Best for: End-to-end testing in browser

2. **Python: Debug Agent**
   - Debugs Python ADK agent with breakpoints
   - Sets all required environment variables
   - Best for: Agent code debugging

## Common Workflows

### 1. Start local development
```
Ctrl+Shift+P → "Tasks: Run Task" → "serve:local"
```
or
```
F5 → "App (attach) – web"
```

### 2. Test after code changes
```
Ctrl+Shift+P → "Tasks: Run Task" → "smoke:local"
```

### 3. Full smoke test (local + cloud)
```
Ctrl+Shift+P → "Tasks: Run Task" → "smoke:all"
```

### 4. Deploy to production
```
Ctrl+Shift+P → "Tasks: Run Task" → "deploy:cloud"
```
Then verify:
```
Ctrl+Shift+P → "Tasks: Run Task" → "smoke:cloud"
```

### 5. Emergency rollback
```
Ctrl+Shift+P → "Tasks: Run Task" → "rollback:fast"
```

## Task Terminal Groups

Tasks are organized into dedicated terminal groups:

- **SERVER**: Background server processes
- **CHECKS**: Smoke tests and validation
- **DEPLOY**: Deployment and rollback operations

This keeps output organized and easy to find.

## Reading Task Output

All tasks log to files in `logs/` directory:

```powershell
# View server logs
Get-Content logs/server.local.log -Tail 50 -Wait

# View smoke test results
Get-Content logs/smoke.cloud.log

# View guardrail test
Get-Content logs/test.guardrail.log
```

Or ask Copilot:
```
"Copilot, read logs/server.local.log and check for errors"
"Copilot, run task smoke:cloud and analyze the output"
```

## Standalone Scripts

You can also run the smoke tests directly:

**PowerShell:**
```powershell
.\scripts\smoke.ps1
```

**Bash (Mac/Linux/Cloud Shell):**
```bash
bash scripts/smoke.sh
```

## Problem Matchers

The `serve:local` task includes a problem matcher that detects when the server is ready:
- Looks for `[startup]` log lines
- Waits for `vertexai.init() called` message
- Tasks that depend on the server (like `smoke:all`) wait for this signal

## Troubleshooting

**Task not found:**
- Reload window: `Ctrl+Shift+P` → "Developer: Reload Window"

**Server already running:**
- Stop the task: Click trash icon in terminal
- Or find process: `Get-Process | Where-Object {$_.Path -like "*python*"}`

**Smoke tests fail:**
1. Check server is running: `curl http://127.0.0.1:19000/list-apps?relative_path=arcade_app`
2. Check logs: `Get-Content logs/server.local.log -Tail 50`
3. Verify environment: Run `test:guardrail` task

**Need to customize:**
- Edit `.vscode/tasks.json`
- Adjust commands, ports, or environment variables as needed
