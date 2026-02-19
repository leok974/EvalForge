# Phase L: UI Learner Usefulness Spot-Check

**Date:** 2026-02-18
**Goal:** Verify that quest failures provide actionable feedback in the UI.

## Spot Checks

### 1. Node World (`node-ignition`)
- **Mistake:** Removed `process.exit(2)` from solution.
- **Expected:** `tests_pass` fails (exit code mismatch). New `source_regex` fails ("Code uses process.exit...").
- **Actual:** Both objectives fail.
- **Actionable?** YES. The `source_regex` failure explicitly tells the user to use `process.exit()`.

### 2. SQL World (`sql-select`)
- **Mistake:** Wrote `UPDATE ...` instead of `SELECT ...`.
- **Expected:** `tests_pass` fails. New `source_regex` fails ("Query uses SELECT statement").
- **Actual:** Both fail.
- **Actionable?** YES. The regex check catches the wrong statement type immediately.

### 3. Python World (`first-sparks`)
- **Mistake:** Syntax error in `main.py`.
- **Expected:** `tests_pass` fails with traceback.
- **Actionable?** YES (Traceback is shown in stderr).

## Conclusion
The addition of source/stdout regex checks significantly improves actionability for beginner quests. The system correctly reports specific objective failures alongside general test failures.
