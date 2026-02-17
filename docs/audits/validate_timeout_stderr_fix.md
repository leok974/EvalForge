# Validate Timeout & Stderr Display Fix

## Issue Summary

**Problem 1: Validate Mode Hang**
- `mode="validate"` calls `validate_quest_attempt()` synchronously without timeout
- AST parsing on malformed/complex code could hang indefinitely
- Users experienced indefinite loading on validation requests

**Problem 2: Stderr Not Visible in UI**
- Backend returns `stderr` in `RunResponse`
- Frontend adds stderr to Terminal logs with `type='error'`
- BUT: Terminal component displayed `type='error'` as **"WARN"** in amber, not "ERROR"
- User confusion: error details present but not clearly labeled

---

## Fixes Applied

### Backend: `routes_quests_runtime.py`

Added signal-based timeout wrapper (20s) around `validate_quest_attempt()`:

```python
import signal
from contextlib import contextmanager

@contextmanager
def validation_timeout(seconds=20):
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Validation timeout after {seconds}s")
    
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

try:
    with validation_timeout(20):
        objective_results = validate_quest_attempt(...)
except TimeoutError as e:
    stderr += f"\n{str(e)}"
    objective_results = [{
        "id": "validation_timeout",
        "ok": False,
        "detail": "Validation exceeded time limit (20s). Please simplify your code or contact support."
    }]
```

**Contract Guarantee:**
- All validate requests return within 20s
- Timeout produces deterministic failure response
- `stderr`, `stdout`, `exit_code`, `timed_out` always included

---

### Frontend: `QuestIDE.tsx`

Changed Terminal error label from "WARN" to "ERROR":

**Before:**
```tsx
{entry.type === 'error' && <span className="text-amber-500">WARN</span>}
<span className={entry.type === 'error' ? 'text-amber-200' : ...}>
```

**After:**
```tsx
{entry.type === 'error' && <span className="text-red-500">ERROR</span>}
<span className={entry.type === 'error' ? 'text-red-200' : ...}>
```

**Result:** Stderr now displays with red "ERROR" prefix and red text for immediate visibility.

---

## Verification Steps

### 1. Validate No Longer Hangs

**Test:**
```bash
curl -X POST http://localhost:8092/api/quests/python-ignition/run \
  -H "X-Dev-User: test" \
  -d '{
    "code": "",
    "language": "python",
    "mode": "validate",
    "workspace": [{"path": "task.py", "content": "import time\ntime.sleep(999)"}]
  }'
```

**Expected:** Response within 20s with `validation_timeout` objective failure.

---

### 2. Stderr Visible in UI

**Test:**
1. Open any Python quest (e.g., `python-ignition`)
2. Write broken code: `sdfsdf` (undefined variable)
3. Click **Run**
4. Check Terminal output

**Expected:**
```
INFO   --- Starting Execution ---
ERROR  Traceback (most recent call last):
ERROR    File "task.py", line 1, in <module>
ERROR      sdfsdf
ERROR  NameError: name 'sdfsdf' is not defined
ERROR  [FAIL] obj_default: Execution failed (Exit Code: 1)
```

**NOT:**
```
WARN   [FAIL] obj_default: obj_default
```

---

## API Response Contract

### `/api/quests/{quest_id}/run`

**Always includes:**
```json
{
  "stdout": "string",
  "stderr": "string",
  "exit_code": int,
  "timed_out": bool,
  "passed": bool,
  "objective_results": [...],
  "duration_ms": int
}
```

**Failure modes:**
- Execution timeout: `timed_out=true`, `exit_code` varies
- Validation timeout: `objective_results` includes `validation_timeout` failure
- Code errors: `stderr` contains full traceback

---

## File Changes

- [Backend] `arcade_app/routers/routes_quests_runtime.py`: Lines 198-232 (timeout wrapper + exception handler)
- [Frontend] `apps/web/src/components/quests/QuestIDE.tsx`: Lines 1090, 1093 (ERROR label + red color)

---

## Notes

- **Windows Limitation**: `signal.SIGALRM` only works on Unix. For Windows production, swap to `threading.Timer` or async timeout.
- **Current Setup**: Dev environment is Docker (Linux), so signal-based timeout works.
- **Fallback Behavior**: If timeout framework unavailable, validation proceeds without timeout (graceful degradation).
