# 🎯 Starting the ADK Server - Complete Guide

## ✅ Setup Complete

All fixes have been applied. You can now start the ADK server using either scan mode or module mode.

## 🚀 Recommended: Scan Mode

### Start Server
```powershell
cd D:\EvalForge
.\.venv\Scripts\Activate.ps1
adk web . --port 19000
```

**Why this works:**
- ADK scans the current directory for Python files
- Finds `arcade.py` which exports `root_agent`
- Automatically discovers the `ArcadeOrchestrator` agent

### Verify Discovery
```powershell
# In a NEW terminal
curl.exe http://127.0.0.1:19000/list-apps?relative_path=./
```

**Expected output:** JSON showing discovered agents
```json
[{"name": "arcade", "path": "arcade.py"}]
```

### Open UI
Open browser: **http://127.0.0.1:19000/dev-ui/**

You should see **ArcadeOrchestrator** in the agent dropdown! 🎉

## 🔧 Alternative: Module Mode

### Start Server
```powershell
cd D:\EvalForge
.\.venv\Scripts\Activate.ps1
adk web arcade_app --port 19000
```

**Why this works:**
- Explicitly tells ADK to load the `arcade_app` module
- Uses the updated `arcade_app/__init__.py` that exports `root_agent`

## 📋 Pre-Flight Checklist

Before starting the server, verify:

1. **Virtual environment activated**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   # Prompt should show (.venv)
   ```

2. **In correct directory**
   ```powershell
   cd D:\EvalForge
   pwd
   # Should show: D:\EvalForge
   ```

3. **Agent imports work**
   ```powershell
   python -c "import arcade; print(arcade.root_agent.name)"
   # Should output: ArcadeOrchestrator
   ```

4. **Port is available**
   ```powershell
   Test-NetConnection -ComputerName 127.0.0.1 -Port 19000 -InformationLevel Quiet
   # Should return: False (port not in use)
   ```

## 🎮 Quick Test Workflow

### 1. Start Server
```powershell
cd D:\EvalForge
.\.venv\Scripts\Activate.ps1
adk web . --port 19000
```

**Watch for:**
```
+-----------------------------------------------------------------------------+
| ADK Web Server started                                                      |
|                                                                             |
| For local testing, access at http://127.0.0.1:19000.                        |
+-----------------------------------------------------------------------------+
```

### 2. Test Agent Discovery (New Terminal)
```powershell
curl.exe http://127.0.0.1:19000/list-apps?relative_path=./
```

### 3. Open Web UI
Navigate to: http://127.0.0.1:19000/dev-ui/

### 4. Select Agent
Click "Select an agent" → Choose **ArcadeOrchestrator**

### 5. Test Judge → Coach Flow
Send message:
```
Run the debounce quest and evaluate it
```

Watch:
1. Judge agent runs tests
2. Judge grades submission based on coverage
3. Coach suggests next quests

## 🐛 Troubleshooting

### Issue: "No agents found" in UI

**Solution 1:** Check scan mode is finding the file
```powershell
# Verify arcade.py exists
Test-Path arcade.py
# Should return: True

# Verify import works
python -c "import arcade; print(arcade.root_agent.name)"
# Should output: ArcadeOrchestrator
```

**Solution 2:** Restart server
- Stop server (Ctrl+C)
- Clear any cached imports
- Start again

### Issue: Port already in use

**Solution:** Use different port
```powershell
adk web . --port 19001
```

Or kill existing process:
```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

### Issue: Import errors on startup

**Check terminal output** where ADK is running - it will show Python tracebacks

**Common fixes:**
```powershell
# Verify all imports
python -c "from arcade_app.agent import root_agent; print('OK')"

# Check for syntax errors
python -m py_compile arcade.py
python -m py_compile arcade_app/agent.py
```

### Issue: Server starts but agent not showing

**Verify scan result:**
```powershell
curl.exe http://127.0.0.1:19000/list-apps?relative_path=./
```

If returns `[]`, ADK isn't finding agents. Check:
1. Are you in the right directory? (`pwd` should show `D:\EvalForge`)
2. Does `arcade.py` exist in current directory?
3. Does `arcade.py` have proper import?

## 📁 Files That Enable Discovery

### `arcade.py` (Repo Root)
```python
# Expose a root_agent from this folder so ADK scan mode can find it
from arcade_app.agent import root_agent

__all__ = ["root_agent"]
```

**Purpose:** Allows ADK scan mode (`adk web .`) to discover the agent

### `arcade_app/__init__.py`
```python
from .agent import root_agent

__all__ = ["root_agent"]
```

**Purpose:** Allows module mode (`adk web arcade_app`) to work

### `arcade_app/agent.py`
Contains:
- `root_agent = SequentialAgent(...)` - The actual agent definition
- `judge` - Judge agent
- `coach` - Coach agent
- Tool functions: `run_tests`, `grade_submission`, `suggest_next_quests`

## 🎯 Success Criteria

✅ Server starts without errors
✅ `curl` returns non-empty agent list
✅ Web UI shows agent dropdown
✅ Can select **ArcadeOrchestrator**
✅ Can send messages and get responses
✅ Judge runs tests and grades
✅ Coach suggests next quests

## 🚀 You're Ready!

**Recommended command:**
```powershell
cd D:\EvalForge
.\.venv\Scripts\Activate.ps1
adk web . --port 19000
```

Then open: **http://127.0.0.1:19000/dev-ui/**

Happy training! 🎉
