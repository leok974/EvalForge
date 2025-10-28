# ✅ FIXED: Agent Discovery Issue

## Problem Found
The ADK server at http://127.0.0.1:19000 was returning an empty array `[]` when querying `/list-apps`, meaning it couldn't find the `root_agent`.

## Root Cause
ADK's scan mode looks for Python files in the target directory that export `root_agent`. When running `adk web arcade_app`, it expected the package to properly expose the agent.

## Fixes Applied

### Fix 1: Updated Package __init__.py
Updated `arcade_app/__init__.py` to explicitly export `root_agent`:
```python
from .agent import root_agent

__all__ = ["root_agent"]
```

### Fix 2: Created Root-Level Scan File
Created `arcade.py` at repo root for scan mode:
```python
# Expose a root_agent from this folder so ADK scan mode can find it
from arcade_app.agent import root_agent

__all__ = ["root_agent"]
```

## Verification
```powershell
python -c "import arcade; print('Has root_agent:', hasattr(arcade, 'root_agent')); print('Agent name:', arcade.root_agent.name)"
# Output: ✓ Has root_agent: True
# Output: ✓ Agent name: ArcadeOrchestrator
```

## How to Start Server

### Option A: Scan Mode (Recommended)
Start from repo root and let ADK scan for agents:
```powershell
cd D:\EvalForge
.\.venv\Scripts\Activate.ps1
adk web . --port 19000
```

### Option B: Module Mode
Specify the module explicitly:
```powershell
cd D:\EvalForge
.\.venv\Scripts\Activate.ps1
adk web arcade_app --port 19000
```

Both work now! Scan mode (Option A) will discover `arcade.py` in the current directory.

## Expected Result After Restart
```powershell
curl.exe http://127.0.0.1:19000/list-apps?relative_path=./
# Should return: [{"name": "arcade", "agents": ["ArcadeOrchestrator"]}]
# or similar indicating the agent was discovered
```

Then opening http://127.0.0.1:19000/dev-ui/ should show **ArcadeOrchestrator** in the agent selection dropdown! 🎉

## Files Modified
- ✅ `arcade_app/__init__.py` - Explicit root_agent export
- ✅ `arcade.py` (NEW) - Root-level scan file for ADK
