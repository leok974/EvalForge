# Agent Engine Verification Guide

## Quick Verification (No UI)

Test the updated session service and app_name handling:

### 1. Create Session
```powershell
# EvalForge on port 19010
$SID = (curl -s -X POST -H "Content-Length: 0" "http://127.0.0.1:19010/apps/arcade_app/users/test/sessions" | ConvertFrom-Json).id
Write-Host "Session ID: $SID"
```

### 2. Non-Streaming Query (should work)
```powershell
curl -s -H "Content-Type: application/json" `
  -d (@{message="hi"} | ConvertTo-Json) `
  "http://127.0.0.1:19010/apps/arcade_app/users/test/sessions/$SID/query"
```

Expected: JSON response with greeting from Greeter agent.

### 3. Streaming Query (should emit SSE events)
```powershell
curl -s -H "Content-Type: application/json" `
  -H "Accept: text/event-stream" `
  -d (@{message="hi"} | ConvertTo-Json) `
  "http://127.0.0.1:19010/apps/arcade_app/users/test/sessions/$SID/query/stream"
```

Expected output:
```
data: {"type":"start"}

data: {"type":"delta","text":"Hey"}

data: {"type":"delta","text":"!"}

data: {"type":"final","text":"Hey! I'm your EvalForge tutor..."}

data: {"type":"done"}
```

If you see `INVALID_ARGUMENT` error, it means:
- ❌ Old code: You're still passing `app_name="arcade_app"` to Vertex AI create_session
- ✅ New code: Should use InMemorySessionService or full engine resource path

## Configuration Options

### Option A: InMemorySessionService (Default - Local Dev)

**Environment:**
```bash
GOOGLE_CLOUD_AGENT_ENGINE_ID=
```

**Behavior:**
- Uses InMemorySessionService (sessions in RAM)
- No Vertex AI session persistence
- `app_name="arcade_app"` passed only to InMemorySessionService (harmless label)
- ✅ Works without ReasoningEngine deployment

**When to use:**
- Local development
- Testing without cloud resources
- Quick prototyping

### Option B: VertexAiSessionService with Agent Engine (Production)

**Environment:**
```bash
GOOGLE_CLOUD_AGENT_ENGINE_ID=projects/291179078777/locations/us-central1/reasoningEngines/REASONING_ENGINE_ID
```

**Behavior:**
- Uses VertexAiSessionService (sessions in Vertex AI)
- Session persistence across restarts
- Full resource path passed as `app_name` to create_session
- ✅ Requires valid ReasoningEngine deployment

**When to use:**
- Production deployments
- Cloud Run services
- When session persistence is required

## Common Gotchas & Fixes

### Issue: Same INVALID_ARGUMENT error still appears

**Diagnosis:**
```powershell
# Search for hardcoded app_name
git grep -n 'app_name=.*arcade_app'
```

**Fix:** Remove `app_name="arcade_app"` from `create_session()` calls. Only use it as:
1. Runner label: `Runner(..., app_name="arcade_app")` ✅
2. InMemorySessionService label ✅
3. NOT in VertexAiSessionService create_session ❌

### Issue: Wrong engine path format

**Error:** Resource name format error

**Fix:** Must use full resource path:
```
projects/<PROJECT_NUMBER>/locations/<REGION>/reasoningEngines/<ENGINE_ID>
```

Not just the engine ID number!

### Issue: Two servers running on same port

**Error:** Port 19010 already in use

**Fix:**
- Check both TasteOS and EvalForge aren't using same port
- Use separate ports: TasteOS on 19000, EvalForge on 19010

## ChatPanel Resilience

The frontend now shows streaming errors in the assistant bubble instead of leaving it blank.

**Before:**
- Streaming error → Empty assistant bubble
- User only sees toast notification

**After:**
- Streaming error → `[stream error] <error message>` in bubble
- User sees error in both toast AND message area

**Test:**
1. Start server with invalid engine ID (trigger INVALID_ARGUMENT)
2. Send message via UI
3. Check that error appears in assistant bubble: `[stream error] ...`

## Log Verification

When `EVALFORGE_EVENT_LOG=1`, you should see:

**Using InMemorySessionService:**
```
INFO:evalforge.adk:Using InMemorySessionService (no Agent Engine configured)
INFO:evalforge.adk:[Session] project=291179078777 location=us-central1 engine=none (using InMemorySessionService) ...
INFO:evalforge.adk:Attempting to create ADK session (no engine): user_id=test session_id=abc123
```

**Using VertexAiSessionService:**
```
INFO:evalforge.adk:Using VertexAiSessionService with engine: projects/291179078777/locations/us-central1/reasoningEngines/123456
INFO:evalforge.adk:[Session] project=291179078777 location=us-central1 engine=projects/.../reasoningEngines/123456 ...
INFO:evalforge.adk:Attempting to create ADK session with engine: app_name=projects/.../reasoningEngines/123456 ...
```

## Summary of Changes

### `arcade_app/agent.py` (and cloud_run_deploy version)

1. **Conditional SessionService:**
   ```python
   if GOOGLE_CLOUD_AGENT_ENGINE_ID:
       SESSION_SERVICE = VertexAiSessionService(...)  # Vertex AI
   else:
       SESSION_SERVICE = InMemorySessionService()     # Local RAM
   ```

2. **Updated _ensure_session:**
   - Only passes `app_name` with full resource path when engine is configured
   - Uses `"arcade_app"` label for InMemorySessionService only
   - Better logging with engine info

3. **Runner label stays:**
   ```python
   RUNNER = Runner(..., app_name="arcade_app")  # Just a label, not sent to Vertex
   ```

### `.vscode/tasks.json`

- Changed `GOOGLE_CLOUD_AGENT_ENGINE_ID` from hardcoded ID to empty string
- Allows local dev without engine by default
- Set to full resource path when needed for production

### `apps/web/src/components/chat/ChatPanel.tsx`

- Shows errors in assistant message bubble
- Format: `[stream error] <error message>`
- User sees error even if toast is dismissed

## Next Steps

1. **Verify local dev works (no engine):**
   ```bash
   # Start server (GOOGLE_CLOUD_AGENT_ENGINE_ID is empty)
   # Run verification commands above
   ```

2. **Test with Agent Engine (optional):**
   ```bash
   # Set full resource path in tasks.json
   GOOGLE_CLOUD_AGENT_ENGINE_ID=projects/291179078777/locations/us-central1/reasoningEngines/YOUR_ENGINE_ID
   # Restart server and test
   ```

3. **Check frontend error display:**
   - Send message with invalid configuration
   - Verify error appears in bubble
