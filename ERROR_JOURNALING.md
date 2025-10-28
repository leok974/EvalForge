# Error Journaling System

Automatically captures all test runs, failures, and successes to generate new quest exercises from real error patterns.

## 🎯 Overview

Every time you run tests (Vitest, Pytest, ADK, etc.), the system:
1. **Captures** stdout, stderr, and exit code
2. **Fingerprints** failures for deduplication
3. **Stores** normalized records in `logs/error-journal.ndjson`
4. **Preserves** artifacts like coverage reports
5. **Links** to quest IDs for tracking

## 📁 Files Created

```
.vscode/
  └─ tasks.json              # VS Code task definitions

scripts/
  ├─ log_wrap.ps1            # PowerShell wrapper (Windows)
  └─ log_wrap.sh             # Bash wrapper (Linux/Mac)

tools/
  └─ aggregate_errors.py     # Error pattern analyzer

logs/
  └─ error-journal.ndjson    # Captured error data (git-ignored)
```

## 🚀 Usage

### Option 1: VS Code Tasks (Recommended)

Press `Ctrl+Shift+P` → **Tasks: Run Task** → Select:

- **Run: Vitest (logged)** - Run Vitest with coverage tracking
- **Run: Pytest (logged)** - Run Python tests
- **Run: ADK web (logged)** - Start ADK server with logging
- **Run: Judge Agent Test (logged)** - Test the Judge agent
- **Analyze Error Patterns** - View recurring failures

### Option 2: Command Line

#### Windows (PowerShell)
```powershell
# Run Vitest with logging
pwsh -File scripts/log_wrap.ps1 `
  --tag vitest `
  --cmd "pwsh -File scripts/run_vitest.ps1 debounce" `
  --art "exercises/js/coverage/coverage-final.json"

# Run with quest tracking
$env:QUEST_ID = "quest-js-debounce-b"
pwsh -File scripts/log_wrap.ps1 --tag vitest --cmd "npm test"
```

#### Linux/Mac (Bash)
```bash
# Run Vitest with logging
bash scripts/log_wrap.sh \
  --tag vitest \
  --cmd "bash scripts/run_vitest.sh debounce" \
  --art "exercises/js/coverage/coverage-final.json"

# Run with quest tracking
export QUEST_ID="quest-js-debounce-b"
bash scripts/log_wrap.sh --tag vitest --cmd "npm test"
```

## 📊 Journal Entry Format

Each run creates a JSON record in `logs/error-journal.ndjson`:

```json
{
  "ts": "2025-10-13T21:20:45Z",
  "os": "windows",
  "tag": "vitest",
  "cwd": "D:\\EvalForge",
  "command": "pwsh -File scripts/run_vitest.ps1 debounce",
  "exit_code": 0,
  "fingerprint": "",
  "stdout_tail": "✓ test/debounce.test.ts (2 tests)...",
  "stderr_tail": "",
  "artifact": { /* coverage JSON */ },
  "quest_id": "quest-js-debounce-b"
}
```

### Fields

- **ts**: Timestamp in ISO 8601 format
- **os**: Operating system (`windows` or `unix`)
- **tag**: Test category (vitest, pytest, adk, etc.)
- **cwd**: Working directory
- **command**: Exact command executed
- **exit_code**: Process exit code (0 = success)
- **fingerprint**: SHA1 hash of stderr (for deduplication)
- **stdout_tail**: Last 50 lines of stdout
- **stderr_tail**: Last 50 lines of stderr
- **artifact**: Parsed JSON artifact (e.g., coverage report)
- **quest_id**: Optional quest identifier from `$env:QUEST_ID`

## 📈 Analyzing Error Patterns

Run the aggregator to find recurring failures:

```powershell
python tools/aggregate_errors.py
```

Output example:
```
================================================================================
Error Journal Analysis
================================================================================
Total runs: 47
Failed runs: 12
Success rate: 74.5%
Unique error patterns: 5
================================================================================

Top 10 recurring failures:

1. [vitest] × 5 occurrences
   Fingerprint: 8e3b3a5c1f2e...
   Error: ReferenceError: debounce is not defined
   Command: pwsh -File scripts/run_vitest.ps1 debounce

2. [pytest] × 3 occurrences
   Fingerprint: 4f8a2b9d7c1e...
   Error: AssertionError: Expected 5, got 3
   Command: pytest tests/test_utils.py

================================================================================
💡 Quest Generation Suggestions
================================================================================

Quest Candidate #1 (5 occurrences):
  Tag: vitest
  Create: seed/quests/vitest_8e3b3a5c.json
  Symptom: ReferenceError: debounce is not defined
  Goal: Fix the vitest issue and achieve 100% test pass
```

## 🎮 Turning Errors into Quests

### Workflow

1. **Work Normally**: Use VS Code tasks or CLI wrappers
2. **Periodically Analyze**: Run `python tools/aggregate_errors.py`
3. **Pick Top Errors**: Select frequent failure patterns
4. **Create Quest**: Build exercise that reproduces the error

### Example: Creating a Quest from an Error

1. **Find the error pattern**:
   ```
   Error: ReferenceError: debounce is not defined
   Fingerprint: 8e3b3a5c1f2e...
   Tag: vitest
   ```

2. **Create quest file**: `seed/quests/vitest_8e3b3a5c.json`
   ```json
   {
     "id": "quest-js-debounce-undefined",
     "concept": "js.imports",
     "tier": "B",
     "time_limit_sec": 600,
     "recipe": "bug_fix",
     "rubric": {
       "correctness": 5,
       "imports": 3,
       "tests_pass": 2
     },
     "symptom": "ReferenceError: debounce is not defined",
     "goal": "Fix the import statement to properly load the debounce function",
     "tests": {
       "runner": "vitest",
       "command": "scripts/run_vitest.sh debounce",
       "artifacts": ["exercises/js/coverage/coverage-final.json"]
     }
   }
   ```

3. **Create broken exercise** that matches the error
4. **Add solution path** for the Judge to grade against

## 🔧 Customization

### Add New Test Types

Edit `.vscode/tasks.json`:

```json
{
  "label": "Run: MyTool (logged)",
  "type": "shell",
  "command": "pwsh -File scripts/log_wrap.ps1",
  "args": [
    "--tag", "mytool",
    "--cmd", "python my_tool.py",
    "--art", "output/results.json"
  ]
}
```

### Filter Analysis by Tag

Modify `tools/aggregate_errors.py`:

```python
# Only analyze vitest failures
if obj.get("tag") != "vitest":
    continue
```

### Custom Fingerprinting

In `scripts/log_wrap.ps1` or `log_wrap.sh`, modify the fingerprint logic:

```powershell
# Use first line of error instead of full stderr
$firstError = ($stdErr -split "`n")[0]
$fingerprint = (Get-FileHash -InputStream ([IO.MemoryStream]::new([Text.Encoding]::UTF8.GetBytes($firstError)))).Hash
```

## 📋 Best Practices

### 1. Use Quest IDs for Tracking
```powershell
$env:QUEST_ID = "quest-js-debounce-b"
# Run task...
```

### 2. Commit Sample Errors
Keep a few example entries in version control:
```powershell
# Keep first 10 entries as examples
Get-Content logs/error-journal.ndjson | Select-Object -First 10 > logs/error-journal.sample.ndjson
```

### 3. Regular Analysis
Set up a weekly task to review error patterns:
```json
{
  "label": "Weekly Error Review",
  "type": "shell",
  "command": "python tools/aggregate_errors.py > reports/weekly-errors.txt"
}
```

### 4. Archive Old Logs
```powershell
# Rotate logs monthly
$date = Get-Date -Format "yyyy-MM"
Move-Item logs/error-journal.ndjson "logs/error-journal-$date.ndjson"
```

## 🎯 Example Workflow

### Day 1-5: Collect Data
```powershell
# Run tests with logging
# Press Ctrl+Shift+P → Run Task → Run: Vitest (logged)
# Repeat for different exercises
```

### Day 6: Analyze
```powershell
python tools/aggregate_errors.py
```

### Day 7: Create Quests
```powershell
# Top error: "Cannot read property 'length' of undefined"
# Create: seed/quests/js_nullcheck_B.json
# Build exercise that reproduces this common mistake
```

## 🔬 Advanced: Artifact Analysis

The system captures artifacts like coverage reports. Access them in analysis:

```python
# In tools/aggregate_errors.py
for key, entries in buckets.items():
    for entry in entries:
        artifact = entry.get('artifact')
        if artifact and isinstance(artifact, dict):
            coverage = artifact.get('total', 0)
            print(f"Coverage was {coverage}% when this error occurred")
```

## 📊 Sample Analysis Output

```
================================================================================
Error Journal Analysis
================================================================================
Total runs: 153
Failed runs: 47
Success rate: 69.3%
Unique error patterns: 15
================================================================================

Top 10 recurring failures:

1. [vitest] × 23 occurrences
   Fingerprint: 8e3b3a5c1f2e...
   Error: Expected debounce to be called 1 time, but it was called 2 times
   Command: pwsh -File scripts/run_vitest.ps1 debounce
   Quest: quest-js-debounce-b

2. [vitest] × 12 occurrences
   Fingerprint: 4f8a2b9d7c1e...
   Error: Timeout waiting for element to appear
   Command: pwsh -File scripts/run_vitest.ps1 csp
   
3. [pytest] × 8 occurrences
   Fingerprint: 9a1c5e7f3b2d...
   Error: assert 404 == 200
   Command: pytest tests/test_api.py
```

## 🚀 Integration with Judge Agent

The Judge can read the error journal to provide context:

```python
# In arcade_app/agent.py
def analyze_student_errors(quest_id: str) -> str:
    """Load error patterns for a specific quest"""
    journal = Path("logs/error-journal.ndjson")
    errors = []
    for line in journal.read_text().splitlines():
        entry = json.loads(line)
        if entry.get("quest_id") == quest_id and entry.get("exit_code") != 0:
            errors.append(entry["stderr_tail"])
    return f"Common errors for this quest: {errors[:3]}"
```

## 📝 Notes

- Journal file can grow large - consider rotating or archiving
- Fingerprints help deduplicate but may miss subtle variations
- Artifact depth is limited to 6 levels in JSON serialization
- stderr/stdout are truncated to last 50 lines to keep entries manageable

## 🎉 Benefits

✅ **Automatic error collection** - No manual tracking needed
✅ **Quest generation data** - Real errors from real runs
✅ **Deduplication** - Find the most common issues
✅ **Coverage tracking** - Links errors to test coverage
✅ **Cross-platform** - Works on Windows, Linux, and Mac
✅ **VS Code integration** - Run tasks with one click
✅ **Historical data** - Track improvement over time
