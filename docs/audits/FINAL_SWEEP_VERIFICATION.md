# Final Sweep Verification Report

**Date:** 2026-05-16 13:29:51
**Status:** FINAL_VERIFICATION

## Summary

| Questpack | Mode | Status | Pass/Total | Notes |
|---|---|---|---|---|
| `agents_core.json` | `solution` | ✅ | N/A | |
| `agents_core.json` | `student` | ✅ (Expected) | N/A | |
| `cli_core.json` | `solution` | ❌ | N/A | |
| `cli_core.json` | `student` | ✅ (Expected) | N/A | |
| `docker_core.json` | `solution` | ✅ | 10/10 | |
| `docker_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `foundry_python.json` | `solution` | ✅ | 2/2 | |
| `foundry_python.json` | `student` | ✅ (Expected) | 0/2 | |
| `git_core.json` | `solution` | ❌ | N/A | |
| `git_core.json` | `student` | ✅ (Expected) | N/A | |
| `git_tier2.json` | `solution` | ❌ | 0/3 | |
| `git_tier2.json` | `student` | ✅ (Expected) | 0/3 | |
| `infra_core.json` | `solution` | ✅ | 10/10 | |
| `infra_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `javascript_core.json` | `solution` | ❌ | 9/10 | |
| `javascript_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `ml_core.json` | `solution` | ✅ | 10/10 | |
| `ml_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `node_core.json` | `solution` | ✅ | 10/10 | |
| `node_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `python_selenium.json` | `solution` | ❌ | 0/5 | |
| `python_selenium.json` | `student` | ✅ (Expected) | 0/5 | |
| `python_systems.json` | `solution` | ✅ | 7/7 | |
| `python_systems.json` | `student` | ✅ (Expected) | 0/7 | |
| `python_tier2.json` | `solution` | ✅ | 6/6 | |
| `python_tier2.json` | `student` | ✅ (Expected) | 0/6 | |
| `react_core.json` | `solution` | ✅ | 10/10 | |
| `react_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `sql_core.json` | `solution` | ❌ | N/A | |
| `sql_core.json` | `student` | ✅ (Expected) | 0/11 | |
| `sql_tier2.json` | `solution` | ❌ | 0/12 | |
| `sql_tier2.json` | `student` | ✅ (Expected) | 0/12 | |
| `sql_tier3.json` | `solution` | ❌ | N/A | |
| `sql_tier3.json` | `student` | ✅ (Expected) | 0/10 | |
| `typescript_core.json` | `solution` | ✅ | 10/10 | |
| `typescript_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `web_css_core.json` | `solution` | ✅ | 10/10 | |
| `web_css_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `web_html_core.json` | `solution` | ✅ | 10/10 | |
| `web_html_core.json` | `student` | ✅ (Expected) | 0/10 | |

## Detailed Failures

### ❌ cli_core.json (Solution Mode)
```
=== Running 10 CLI quests from data\questpacks\cli_core.json in solution mode ===
```
### ❌ git_core.json (Solution Mode)
```
=== Running 10 Git quests from data\questpacks\git_core.json in solution mode ===
```
### ❌ git_tier2.json (Solution Mode)
```
=== Running 3 Git quests from data\questpacks\_tier2\git_tier2.json in solution mode ===
EF_RUNNER_RESULT_JSON={"total":3,"passed":0,"failed":3,"errors":[],"slugs":[{"slug":"git-t2-merge-conflict","status":"failed"},{"slug":"git-t2-rebase","status":"failed"},{"slug":"git-t2-release","status":"failed"}]}

❌ Git questpack FAILED (0/3 passed)

EF_RUN_WORLD_SUMMARY: 0/3 public tests passed.
```
### ❌ javascript_core.json (Solution Mode)
```
  type: 'test'
  ...
# Subtest: Default export circleArea
ok 2 - Default export circleArea
  ---
  duration_ms: 0.1023
  type: 'test'
  ...
1..2
# tests 2
# suites 0
# pass 2
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 54.5744

EF_RUN_WORLD_SUMMARY: 9/10 quests passed.
EF_RUNNER_RESULT_JSON={"total":10,"passed":9,"failed":1,"errors":["js-vars-q1-let-const-var: js-vars-q1-let-const-var.public.test.mjs failed"],"slugs":[{"slug":"js-ignition-q1-console-and-functions","status":"passed"},{"slug":"js-vars-q1-let-const-var","status":"failed"},{"slug":"js-control-q1-if-else-loops","status":"passed"},{"slug":"js-arrays-q1-basics","status":"passed"},{"slug":"js-arrays-q2-map-filter-reduce","status":"passed"},{"slug":"js-objects-q1-properties-methods","status":"passed"},{"slug":"js-functions-q1-arrow-vs-regular","status":"passed"},{"slug":"js-async-q1-promises-basics","status":"passed"},{"slug":"js-errors-q1-try-catch","status":"passed"},{"slug":"js-modules-q1-import-export","status":"passed"}]}
```
### ❌ python_selenium.json (Solution Mode)
```
DEBUG: Checking for solution overlay at data\questpacks\..\quests\selenium-take-screenshot\grading\solutions
   ⚠️ No solution found, running as student/starter.
DEBUG: Checking for tests at data\questpacks\..\quests\selenium-take-screenshot\grading\public
   ❌ FAILED
      Exit Code: 1
      - [take_screenshot] FAIL: Skipped due to runtime failure
      (stdout empty)
      --- STDERR ---
Traceback (most recent call last):
  File "C:\Users\pierr\AppData\Local\Temp\tmp71hzr7gs\main.py", line 2, in <module>
    from selenium import webdriver
ModuleNotFoundError: No module named 'selenium'

      --------------
EF_RUNNER_RESULT_JSON={"total": 5, "passed": 0, "failed": 5, "errors": ["aceback (most recent call last):\n  File \"C:\\Users\\pierr\\AppData\\Local\\Temp\\tmp96v52ipx\\main.py\", line 2, in <module>\n    from selenium import webdriver\nModuleNotFoundError: No module named 'selenium'\n", "aceback (most recent call last):\n  File \"C:\\Users\\pierr\\AppData\\Local\\Temp\\tmpra18uorv\\main.py\", line 2, in <module>\n    from selenium import webdriver\nModuleNotFoundError: No module named 'selenium'\n", "aceback (most recent call last):\n  File \"C:\\Users\\pierr\\AppData\\Local\\Temp\\tmp66iohggv\\main.py\", line 2, in <module>\n    from selenium import webdriver\nModuleNotFoundError: No module named 'selenium'\n", "aceback (most recent call last):\n  File \"C:\\Users\\pierr\\AppData\\Local\\Temp\\tmpp12ri6yp\\main.py\", line 2, in <module>\n    from selenium import webdriver\nModuleNotFoundError: No module named 'selenium'\n", "aceback (most recent call last):\n  File \"C:\\Users\\pierr\\AppData\\Local\\Temp\\tmp71hzr7gs\\main.py\", line 2, in <module>\n    from selenium import webdriver\nModuleNotFoundError: No module named 'selenium'\n"], "slugs": [{"slug": "selenium-open-page", "status": "failed"}, {"slug": "selenium-find-elements", "status": "failed"}, {"slug": "selenium-click-and-type", "status": "failed"}, {"slug": "selenium-read-text-and-assert", "status": "failed"}, {"slug": "selenium-take-screenshot", "status": "failed"}]}

========================================
❌ FAILED: 5/5 quests failed.

EF_RUN_WORLD_SUMMARY: 0/5 public tests passed.
```
### ❌ sql_core.json (Solution Mode)
```
            "engine": "sqlite",
            "statement": "",
            "plan_rows": []
        }
    
        try:
            # Load Schema
>           with open(schema_sql_path, "r", encoding="utf-8") as f:
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           FileNotFoundError: [Errno 2] No such file or directory: 'D:\\EvalForge\\.claude\\worktrees\\wonderful-galileo-95a5e6\\data\\quests\\sql-select\\fixtures\\schema.sql'

..\..\_shared\sql_test_helpers.py:114: FileNotFoundError
=========================== short test summary info ===========================
FAILED grading/public/test_sql_select.py::test_sql_select - FileNotFoundError...
1 failed in 0.31s
.                                                                        [100%]
1 passed in 0.13s
[FAIL] sql-ignition
[FAIL] sql-select
[PASS] sql-where
```
### ❌ sql_tier2.json (Solution Mode)
```
[FAIL] sql-t2-indexes-explain
[FAIL] sql-t2-transactions-rollback
[FAIL] sql-t2-boss-data-quality-audit
EF_RUNNER_RESULT_JSON={"total": 12, "passed": 0, "failed": 12, "errors": [], "slugs": [{"slug": "sql-t2-groupby-having", "status": "failed"}, {"slug": "sql-t2-window-functions", "status": "failed"}, {"slug": "sql-t2-analytics-pack", "status": "failed"}, {"slug": "sql-t2-subqueries-exists", "status": "failed"}, {"slug": "sql-t2-cte-basics", "status": "failed"}, {"slug": "sql-t2-recursive-cte-hierarchy", "status": "failed"}, {"slug": "sql-t2-nulls-coalesce", "status": "failed"}, {"slug": "sql-t2-dates-grouping", "status": "failed"}, {"slug": "sql-t2-upsert-on-conflict", "status": "failed"}, {"slug": "sql-t2-indexes-explain", "status": "failed"}, {"slug": "sql-t2-transactions-rollback", "status": "failed"}, {"slug": "sql-t2-boss-data-quality-audit", "status": "failed"}]}

Failed quests:
 - sql-t2-groupby-having
 - sql-t2-window-functions
 - sql-t2-analytics-pack
 - sql-t2-subqueries-exists
 - sql-t2-cte-basics
 - sql-t2-recursive-cte-hierarchy
 - sql-t2-nulls-coalesce
 - sql-t2-dates-grouping
 - sql-t2-upsert-on-conflict
 - sql-t2-indexes-explain
 - sql-t2-transactions-rollback
 - sql-t2-boss-data-quality-audit

EF_RUN_WORLD_SUMMARY: 0/12 public tests passed.
```
### ❌ sql_tier3.json (Solution Mode)
```
No output captured.
```
