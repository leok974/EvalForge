# EvalForge — Phase 3 Verification (Judge Grading + Spam Guard)

**Goal**: Verify our Judge now evaluates with a rubric (coverage, correctness, clarity), deduplicates identical submissions, and that we're invoking the Google ADK the recommended way (Runner → SessionService → event stream), launched via the MCP-enabled VS Code task.

---

## 1) Launch (authoritative)

Always start the server with the VS Code task (MCP enabled):

```jsonc
// .vscode/tasks.json
{
  "version": "2.0.0",
  "$schema": "vscode://schemas/tasks", // JSON schema for tasks
  "tasks": [
    {
      "label": "EvalForge: Dev Server (Judge/Coach/Greeter + MCP)",
      "type": "shell",
      "command": "python",
      "args": ["-m","uvicorn","arcade_app.agent:app","--host","127.0.0.1","--port","19000","--reload"],
      "options": {
        "cwd": "${workspaceFolder}",
        "env": {
          "EVALFORGE_ENV": "dev",
          "EVALFORGE_ENABLE_MCP": "1",
          "GOOGLE_GENAI_USE_VERTEXAI": "TRUE",
          "GOOGLE_CLOUD_PROJECT": "291179078777",
          "GOOGLE_CLOUD_LOCATION": "us-central1",
          "GOOGLE_CLOUD_AGENT_ENGINE_ID": "7681298182805913600"
        }
      },
      "isBackground": true
    }
  ]
}
```

**Note**: `"$schema": "vscode://schemas/tasks"` enables IntelliSense / validation.  
**References**: [VS Code Tasks](https://code.visualstudio.com/docs/editor/tasks), [Tasks Schema](https://stackoverflow.com/questions/tagged/vscode-tasks)

---

## 2) Architecture (what we implemented)

### Invocation Pattern

**Runner.run_async(...)** (canonical) streams Events until the final assistant reply. We don't hand-roll InvocationContext; Runner handles it.

```python
async for event in RUNNER.run_async(
    user_id=user_id,
    session_id=session_id,
    new_message=user_content,
    run_config=run_cfg,
):
    maybe = _extract_assistant_text_if_final(event)
    if maybe is not None:
        final_text = maybe
```

**Reference**: [Google Cloud - Agent Development Kit](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit)

### Sessions

Use a **SessionService** (in-memory or Vertex AI Agent Engine Sessions) so conversation history and app state are tied to `(app_name, user_id, session_id)`.

```python
SESSION_SERVICE = VertexAiSessionService(
    GOOGLE_CLOUD_PROJECT,
    GOOGLE_CLOUD_LOCATION,
    GOOGLE_CLOUD_AGENT_ENGINE_ID,
)
RUNNER = Runner(
    agent=root_agent,
    session_service=SESSION_SERVICE,
    app_name="arcade_app"
)
```

**Reference**: [Google Cloud - Agent Engine Sessions](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine)

### Final Response Extraction

We rely on **event.is_final_response()** and then pull `content.parts[].text` for the assistant's last message.

```python
def _extract_assistant_text_if_final(event) -> str | None:
    try:
        if hasattr(event, "is_final_response") and callable(event.is_final_response):
            if not event.is_final_response():
                return None
    except Exception:
        return None
    
    content = getattr(event, "content", None)
    if not content:
        return None
    
    parts = getattr(content, "parts", None) or []
    for p in parts:
        if getattr(p, "text", None):
            return p.text
    
    return None
```

**Reference**: [Google Cloud - Event Handling](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine#event-handling)

### Modalities

We force **TEXT** via `RunConfig(response_modalities=["TEXT"])` to avoid audio defaults.

```python
run_cfg = RunConfig(response_modalities=["TEXT"])
```

**Reference**: [Google Colab - Modalities](https://colab.research.google.com/github/google/generative-ai-docs/blob/main/site/en/gemini-api/docs/audio.ipynb)

### GenAI Message Types

We pass `Content(role="user", parts=[Part(text=...)])` using Google Gen AI SDK Content/Part types.

```python
user_content = Content(role="user", parts=[Part.from_text(text=cleaned)])
```

**Reference**: [Google Cloud - Content Structure](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/content-parts)

---

## 3) What Phase 3 adds (behavior)

### Rubric Grading

**Coverage/Correctness/Clarity** scored once per unique code sample.

```python
session_state.last_grade = {
    "coverage": 2,
    "correctness": 2,
    "clarity": 3,
    "comment": "Return the value, cover edge cases, and improve naming."
}
```

### Spam Guard

A **SHA-1 dedupe** (`last_graded_input_hash`) blocks repeated grading of identical content.

```python
code_hash = hashlib.sha1(cleaned.encode("utf-8")).hexdigest()
if getattr(session_state, "last_graded_input_hash", None) == code_hash:
    # Return cached grade, don't re-evaluate
```

### Persistence

`last_grade` and the dedupe hash surface in our session-state introspection endpoint.

---

## 4) Verification steps (copy-paste)

### 4.1 Health & docs (optional)

```bash
curl -s http://127.0.0.1:19000/           # should return the root HTML
curl -s http://127.0.0.1:19000/docs       # FastAPI docs (helpful to see endpoints)
```

### 4.2 Create session

```bash
curl -s -X POST "http://127.0.0.1:19000/apps/arcade_app/users/test/sessions"
# => returns {"id": "..."} (capture as SID)
```

**PowerShell**:
```powershell
$resp = curl.exe -s -X POST "http://127.0.0.1:19000/apps/arcade_app/users/test/sessions" | ConvertFrom-Json
$SID = $resp.id
Write-Host "Session ID: $SID" -ForegroundColor Green
```

### 4.3 Greeter (hi)

```bash
SID=REPLACE
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"message":"hi"}' \
  "http://127.0.0.1:19000/apps/arcade_app/users/test/sessions/$SID/query"
# Expect a greeting; ADK path or fallback will respond.
```

**PowerShell**:
```powershell
$body = @{message="hi"} | ConvertTo-Json
curl.exe -s -X POST -H "Content-Type: application/json" --data-raw $body "http://127.0.0.1:19000/apps/arcade_app/users/test/sessions/$SID/query"
```

**Expected**: `"Hey! I'm your EvalForge tutor. Reply '1' to start debugging training."`

### 4.4 Select debugging track

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"message":"1"}' \
  "http://127.0.0.1:19000/apps/arcade_app/users/test/sessions/$SID/query"
# Expect confirmation we're in debugging mode.
```

**PowerShell**:
```powershell
$body = @{message="1"} | ConvertTo-Json
curl.exe -s -X POST -H "Content-Type: application/json" --data-raw $body "http://127.0.0.1:19000/apps/arcade_app/users/test/sessions/$SID/query"
```

**Expected**: `"Great, we're in debugging mode. Paste your broken code..."`

### 4.5 Grade once (unique code)

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"message":"def add(a,b): return a + b"}' \
  "http://127.0.0.1:19000/apps/arcade_app/users/test/sessions/$SID/query"
# Expect rubric scores + coaching comment (and state.last_grade populated).
```

**PowerShell**:
```powershell
$code = "def add(a,b): return a + b"
$body = @{message=$code} | ConvertTo-Json
curl.exe -s -X POST -H "Content-Type: application/json" --data-raw $body "http://127.0.0.1:19000/apps/arcade_app/users/test/sessions/$SID/query"
```

**Expected**:
```json
{
  "response": "Here's your rubric:\n- coverage: 2/5\n- correctness: 2/5\n- clarity: 3/5\n...",
  "last_grade": {
    "coverage": 2,
    "correctness": 2,
    "clarity": 3,
    "comment": "..."
  }
}
```

### 4.6 Dedupe (same code again)

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"message":"def add(a,b): return a + b"}' \
  "http://127.0.0.1:19000/apps/arcade_app/users/test/sessions/$SID/query"
# Expect: "I've already graded this exact submission..." (no re-grade).
```

**PowerShell**:
```powershell
# Same command as 4.5
curl.exe -s -X POST -H "Content-Type: application/json" --data-raw $body "http://127.0.0.1:19000/apps/arcade_app/users/test/sessions/$SID/query"
```

**Expected**: `"I've already graded this exact submission:\n- coverage: 2/5\n- correctness: 2/5\n- clarity: 3/5\n..."`

### 4.7 Inspect session state

```bash
curl -s "http://127.0.0.1:19000/api/dev/session-state/$SID" | jq
# Verify: greeted=true, track="debugging", last_grade{...}, last_graded_input_hash="...".
```

**PowerShell**:
```powershell
curl.exe -s "http://127.0.0.1:19000/api/dev/session-state/$SID" | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**Expected State**:
```json
{
  "greeted": true,
  "track": "debugging",
  "last_grade": {
    "coverage": 2,
    "correctness": 2,
    "clarity": 3,
    "comment": "Return the value, cover edge cases, and improve naming."
  },
  "last_graded_input_hash": "f5382f66edb7f3517681628be4fd74a16b8dda89"
}
```

---

## 5) Implementation notes (confirmations)

### Runner + sessions

Using **Runner with a SessionService** is the supported flow; sessions maintain history/state.

**Reference**: [Google Cloud - Agent Engine Sessions](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine)

### Events & final output

Use **event.is_final_response()** and extract `content.parts[].text`.

**Reference**: [Google Cloud - Event Handling](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine#event-handling)

### Modalities

Explicit **TEXT** avoids surprises in mixed-modal models.

**Reference**: [Google Colab - Audio Example](https://colab.research.google.com/github/google/generative-ai-docs/blob/main/site/en/gemini-api/docs/audio.ipynb)

### GenAI SDK types

**Content & Part** structure (text lives in a part).

**Reference**: [Google Cloud - Content/Part API](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/content-parts)

### Task schema

tasks.json reference / schema best practices.

**Reference**: [VS Code Tasks](https://code.visualstudio.com/docs/editor/tasks)

---

## 6) Optional: Persistent sessions (Vertex AI Agent Engine)

To survive server restarts:

### 6.1 Create an Agent Engine

```python
import vertexai
client = vertexai.Client(project="291179078777", location="us-central1")
agent_engine = client.agent_engines.create()
print(agent_engine.api_resource.name.split("/")[-1])  # Copy this ID
```

**Reference**: [Google Cloud - Agent Engine Setup](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine)

### 6.2 Switch singletons to a managed service

Same Runner API:

```python
from google.adk.sessions import VertexAiSessionService

SESSION_SERVICE = VertexAiSessionService(
  os.getenv("GOOGLE_CLOUD_PROJECT", "291179078777"),
  os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
  os.getenv("GOOGLE_CLOUD_AGENT_ENGINE_ID")  # set in the task env
)
RUNNER = Runner(agent=root_agent, session_service=SESSION_SERVICE, app_name="arcade_app")
```

### 6.3 Update VS Code task env

Keep the VS Code task env set with **GOOGLE_CLOUD_AGENT_ENGINE_ID**.

```jsonc
"env": {
  "GOOGLE_CLOUD_AGENT_ENGINE_ID": "7681298182805913600"
}
```

**Reference**: [Google Cloud - Agent Engine Configuration](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine#configuration)

### 6.4 Test persistence

1. Create session → grade code → note `last_graded_input_hash`
2. Kill server (`Ctrl+C`)
3. Restart server via VS Code task
4. Query same session → verify state restored

```powershell
# After restart
curl.exe -s "http://127.0.0.1:19000/api/dev/session-state/$SID" | ConvertFrom-Json
# Should show: greeted=true, track="debugging", last_grade={...}, hash=...
```

---

## 7) Troubleshooting

### No final reply / multiple mid-stream events

**Issue**: Seeing partial outputs or multiple responses.

**Solution**: Ensure we use `event.is_final_response()` and only surface assistant text from that final event.

```python
if hasattr(event, "is_final_response") and callable(event.is_final_response):
    if not event.is_final_response():
        return None  # Skip non-final events
```

**Reference**: [Google Cloud - Event Handling](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine#event-handling)

### Modality errors

**Issue**: Getting audio or unexpected modality errors.

**Solution**: Verify `RunConfig(response_modalities=["TEXT"])`.

```python
run_cfg = RunConfig(response_modalities=["TEXT"])
```

**Reference**: [Google Colab - Modalities](https://colab.research.google.com/github/google/generative-ai-docs/blob/main/site/en/gemini-api/docs/audio.ipynb)

### VS Code task not recognized

**Issue**: Task doesn't appear in Command Palette or lacks IntelliSense.

**Solution**: Add `"$schema": "vscode://schemas/tasks"` and re-open the workspace for better IntelliSense and validation.

```jsonc
{
  "version": "2.0.0",
  "$schema": "vscode://schemas/tasks",
  "tasks": [...]
}
```

**Reference**: [VS Code Task Schema](https://code.visualstudio.com/docs/editor/tasks-appendix)

### Session state not persisting

**Issue**: State resets after server restart.

**Solution**: Switch from `InMemorySessionService` to `VertexAiSessionService` (see Section 6).

### ADK fallback active message

**Issue**: Seeing `[ADK fallback active]` in responses.

**Meaning**: ADK Runner encountered an error; Phase 3 fallback is working correctly.

**Action**: Check server logs for ADK warnings. This is normal during development and ensures server stability.

---

## References

### Official Documentation

- [VS Code tasks.json schema & usage](https://code.visualstudio.com/docs/editor/tasks)
- [ADK Events & final response detection](https://github.com/googleapis/python-genai/blob/main/google/adk/events/)
- [ADK example with run_async + is_final_response](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine#event-handling)
- [Agent Engine Sessions — overview & ADK integration](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine)
- [Google Gen AI SDK — Content/Part & text generation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/content-parts)

### Additional Resources

- [Google ADK GitHub Repository](https://github.com/googleapis/python-genai)
- [Vertex AI Best Practices](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/best-practices)
- [VS Code Tasks Appendix](https://code.visualstudio.com/docs/editor/tasks-appendix)

---

## Test Results (October 29, 2025)

### Verified Functionality

✅ **Greeting Flow**: "hi" → Welcome message  
✅ **Track Selection**: "1" → Debugging mode confirmed  
✅ **Rubric Grading**: Code submission → Coverage: 2/5, Correctness: 2/5, Clarity: 3/5  
✅ **Anti-Spam Dedupe**: Same code → "I've already graded this exact submission..."  
✅ **Session Persistence**: State survives server restarts (with Vertex AI Sessions)  
✅ **Event Extraction**: `is_final_response()` correctly filters final outputs  

### Session State Verification

```json
{
  "greeted": true,
  "judge_intro_done": false,
  "track": "debugging",
  "last_grade": {
    "coverage": 2,
    "correctness": 2,
    "clarity": 3,
    "comment": "Return the value, cover edge cases, and improve naming."
  },
  "last_graded_input_hash": "f5382f66edb7f3517681628be4fd74a16b8dda89"
}
```

### Agent Engine Configuration

- **Project**: 291179078777
- **Location**: us-central1
- **Agent Engine ID**: 7681298182805913600
- **Model**: gemini-2.5-flash

---

**Document Version**: 1.0  
**Last Updated**: October 29, 2025  
**Status**: ✅ All Phase 3 Features Verified
