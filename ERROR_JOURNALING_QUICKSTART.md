# 🎉 Error Journaling System - Quick Start

## ✅ System Ready!

All error journaling infrastructure is now installed and tested.

## 🚀 Try It Now

### Method 1: VS Code Tasks (Easiest)

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Tasks: Run Task"
3. Select **"Run: Vitest (logged)"**
4. Watch the test run with automatic error logging!

### Method 2: Command Line

```powershell
# Windows
pwsh -File scripts/log_wrap.ps1 --tag vitest --cmd "pwsh -File scripts/run_vitest.ps1 debounce" --art "exercises/js/coverage/coverage-final.json"

# Linux/Mac
bash scripts/log_wrap.sh --tag vitest --cmd "bash scripts/run_vitest.sh debounce" --art "exercises/js/coverage/coverage-final.json"
```

## 📊 View Results

After a few test runs:

```powershell
python tools/aggregate_errors.py
```

You'll see:
- Total runs and success rate
- Top recurring failures
- Quest generation suggestions

## 🎮 Current Status

✅ **Test Run**: 1 successful Vitest run logged
✅ **Journal**: `logs/error-journal.ndjson` created
✅ **Success Rate**: 100% (no failures yet)

## 📁 What Was Created

```
.vscode/
  └─ tasks.json                    # ✅ 5 logging tasks ready

scripts/
  ├─ log_wrap.ps1                  # ✅ Windows wrapper
  └─ log_wrap.sh                   # ✅ Linux/Mac wrapper

tools/
  └─ aggregate_errors.py           # ✅ Analysis tool

logs/
  └─ error-journal.ndjson          # ✅ 1 entry captured

docs/
  └─ ERROR_JOURNALING.md           # ✅ Full documentation
```

## 🎯 Next Steps

### 1. Run More Tests (5 min)
```powershell
# Try all the logging tasks:
# - Run: Vitest (logged)
# - Run: Pytest (logged)  
# - Run: Judge Agent Test (logged)
```

### 2. Analyze Patterns (2 min)
```powershell
python tools/aggregate_errors.py
```

### 3. Create Your First Error-Based Quest (15 min)
- Look at top recurring errors
- Copy `seed/quests/js_debounce_B.json` as a template
- Modify to reproduce the error
- Add to skill tree

## 💡 Pro Tips

### Track Quest Performance
```powershell
$env:QUEST_ID = "quest-js-debounce-b"
# Run task...
# Now errors are linked to this quest!
```

### View Journal Entries
```powershell
Get-Content logs/error-journal.ndjson | ConvertFrom-Json | Select-Object ts, tag, exit_code | Format-Table
```

### Sample a Failing Test
```powershell
# Create a broken test
$badCode = @"
export function debounce() {
  return undefined; // This will fail!
}
"@
Set-Content exercises/js/src/debounce-broken.ts -Value $badCode

# Run and capture the failure
pwsh -File scripts/log_wrap.ps1 --tag vitest-fail --cmd "npm test"

# Analyze
python tools/aggregate_errors.py
```

## 📚 Documentation

- **ERROR_JOURNALING.md** - Complete documentation
- **TESTING_DEPLOYMENT.md** - Testing and deployment guide
- **SETUP_COMPLETE.md** - System overview

## 🔥 Cool Features

✨ **Automatic fingerprinting** - Dedupe repeated errors
✨ **Coverage capture** - See coverage when tests fail
✨ **Quest linking** - Track errors per quest
✨ **Cross-platform** - Works everywhere
✨ **VS Code integration** - One-click testing
✨ **Historical analysis** - Track progress over time

## 🎓 Example: Build a Quest from Real Errors

1. **Collect errors** (work for a few days)
2. **Run analysis**:
   ```
   python tools/aggregate_errors.py
   
   Top failure:
   [vitest] × 15 occurrences
   Error: Cannot read property 'length' of undefined
   ```

3. **Create quest**: `seed/quests/js_nullcheck_B.json`
   ```json
   {
     "id": "quest-js-nullcheck-b",
     "concept": "js.defensive",
     "symptom": "Cannot read property 'length' of undefined",
     "goal": "Add null checks before accessing properties"
   }
   ```

4. **Students fix real errors you encountered!**

## 🚀 You're All Set!

The error journaling system is **fully operational** and ready to:
- Capture every test run
- Track failures and successes
- Generate quest ideas from real errors
- Provide data-driven insights

**Start running tests and watch your error database grow!** 📈
