# ✅ Agent Discovery Fixed!

## 🎉 Status: Agent Now Visible in UI

**Service:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/dev-ui/
**Revision:** evalforge-agents-00008-p9n
**Agent:** ArcadeOrchestrator (with Greeter sub-agent)

## What Was Wrong

The previous agent had complex tool imports and function definitions that weren't properly working in the Cloud Run environment. The agent was technically valid but ADK wasn't exposing it in the UI.

## What Was Fixed

### 1. Simplified Agent to Known-Good Minimal Version

**Before (d:\EvalForge\arcade_app\agent.py.backup):**
- Complex tool functions (run_tests, grade_submission, suggest_next_quests)
- FunctionTool wrappers
- Subprocess calls
- File system operations
- JSON parsing

**After (d:\EvalForge\arcade_app\agent.py):**
```python
import os
from google.adk.agents import Agent, SequentialAgent

DEFAULT_MODEL = os.getenv("EVALFORGE_MODEL", "gemini-1.5-flash")

greeter = Agent(
    name="Greeter",
    instruction="Say a short friendly greeting. No tools.",
    model=DEFAULT_MODEL,
)

root_agent = SequentialAgent(
    name="ArcadeOrchestrator",
    sub_agents=[greeter],
    # SequentialAgent doesn't have a model param - uses sub-agents' models
)
```

### 2. Key Learnings

**✅ Model Parameter:**
- `Agent` requires `model` parameter
- `SequentialAgent` does NOT take `model` - it uses sub-agents' models
- Always set `DEFAULT_MODEL = os.getenv("EVALFORGE_MODEL", "gemini-1.5-flash")`

**✅ Dockerfile Configuration:**
```dockerfile
WORKDIR /app
COPY . .
CMD ["sh", "-c", "python -m google.adk.cli web . --host 0.0.0.0 --port ${PORT:-8080}"]
```
- `web .` = scan current directory (/app)
- WORKDIR must contain arcade_app/ subdirectory
- arcade_app/__init__.py must export root_agent

**✅ Environment Variables (Already Set):**
```
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=evalforge-1063529378
GOOGLE_CLOUD_LOCATION=us-central1
EVALFORGE_MODEL=gemini-1.5-flash
```

## Verification Steps

### 1. Agent Appears in List

```bash
curl "https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/list-apps?relative_path=./"
# Returns: ["arcade_app","exercises","scripts","seed"]
```

### 2. Agent Endpoints Work

Logs show successful requests to:
- `/apps/arcade_app/eval_sets`
- `/apps/arcade_app/eval_results`
- `/apps/arcade_app/users/user/sessions`

### 3. Web UI Access

**URL:** https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/dev-ui/

**Steps:**
1. Click "Select an agent" button
2. Choose **arcade_app** from dropdown
3. Agent loads: **ArcadeOrchestrator**
4. Can send messages and get greetings from Greeter sub-agent

## Next Steps to Restore Full Functionality

### Phase 1: Add Tools Back Gradually

Create a new version of agent.py that adds tools one at a time:

1. **First:** Add `run_tests` function only
2. **Test:** Deploy and verify it works
3. **Second:** Add `grade_submission` function
4. **Test:** Deploy and verify
5. **Third:** Add `suggest_next_quests` function
6. **Test:** Deploy and verify

### Phase 2: Test Each Tool

```python
# Test run_tests
message: "Run tests for debounce"
tool_call: run_tests(
    command="cd exercises/js && npm test debounce",
    artifacts=["exercises/js/coverage/coverage-final.json"]
)

# Test grade_submission  
message: "Grade this coverage result"
tool_call: grade_submission(
    test_result={...from run_tests...},
    rubric="80% coverage = PASS"
)

# Test suggest_next_quests
message: "What should I do next after debounce?"
tool_call: suggest_next_quests(
    concept="debounce",
    tier="intermediate"
)
```

### Phase 3: Restore Full Agent

Once all tools work individually, restore the complete Judge + Coach architecture:

```python
judge = Agent(
    name="Judge",
    instruction="Run tests and grade submissions",
    tools=[FunctionTool(run_tests), FunctionTool(grade_submission)],
    model=DEFAULT_MODEL,
)

coach = Agent(
    name="Coach",
    instruction="Suggest next quests based on results",
    tools=[FunctionTool(suggest_next_quests)],
    model=DEFAULT_MODEL,
)

root_agent = SequentialAgent(
    name="ArcadeOrchestrator",
    sub_agents=[judge, coach],
)
```

## Files

**Current Working Files:**
- `d:\EvalForge\arcade_app\agent.py` - Minimal working agent
- `d:\EvalForge\arcade_app\agent.py.backup` - Original complex agent (saved for reference)
- `d:\EvalForge\arcade_app\__init__.py` - Exports root_agent
- `d:\EvalForge\cloud_run_deploy\Dockerfile` - Working configuration

**To Restore Full Agent:**
```powershell
# When ready to restore tools:
Copy-Item d:\EvalForge\arcade_app\agent.py.backup d:\EvalForge\arcade_app\agent.py

# Fix model parameter issue:
# Remove `model=DEFAULT_MODEL` from SequentialAgent

# Deploy:
.\manual_deploy.ps1
```

## Success Metrics

✅ Agent visible in `/list-apps` endpoint
✅ Agent loads in Web UI dropdown
✅ Can select and interact with agent
✅ Agent responds to messages
✅ No import errors in logs
✅ Container starts successfully
✅ Health checks pass

## Deployment Command

```powershell
cd D:\EvalForge
Remove-Item -Recurse -Force cloud_run_deploy -ErrorAction SilentlyContinue
.\manual_deploy.ps1
```

Takes ~3-5 minutes, deploys to:
- https://evalforge-agents-uc7hnhrrkq-uc.a.run.app
- https://evalforge-agents-uc7hnhrrkq-uc.a.run.app/dev-ui/

---

**Fixed:** October 14, 2025
**Revision:** evalforge-agents-00008-p9n
**Status:** ✅ Working with Minimal Agent
