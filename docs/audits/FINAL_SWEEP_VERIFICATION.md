# Final Sweep Verification Report

**Date:** 2026-05-15 12:39:21
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
| `python_systems.json` | `solution` | ❌ | 1/7 | |
| `python_systems.json` | `student` | ✅ (Expected) | 0/7 | |
| `react_core.json` | `solution` | ✅ | 10/10 | |
| `react_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `sql_core.json` | `solution` | ❌ | N/A | |
| `sql_core.json` | `student` | ✅ (Expected) | 0/11 | |
| `typescript_core.json` | `solution` | ✅ | 10/10 | |
| `typescript_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `web_css_core.json` | `solution` | ✅ | 10/10 | |
| `web_css_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `web_html_core.json` | `solution` | ❌ | 0/10 | |
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
### ❌ javascript_core.json (Solution Mode)
```
  type: 'test'
  ...
# Subtest: Default export circleArea
ok 2 - Default export circleArea
  ---
  duration_ms: 0.1057
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
# duration_ms 55.6251

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
  File "C:\Users\pierr\AppData\Local\Temp\tmpdjr31__a\main.py", line 17
    options.add_argument("--disable-dev-shm-usage")from selenium.webdriver.chrome.service import Service
                                                   ^^^^
SyntaxError: invalid syntax

      --------------
EF_RUNNER_RESULT_JSON={"total": 5, "passed": 0, "failed": 5, "errors": ["aceback (most recent call last):\n  File \"C:\\Users\\pierr\\AppData\\Local\\Temp\\tmpeas9pemg\\main.py\", line 2, in <module>\n    from selenium import webdriver\nModuleNotFoundError: No module named 'selenium'\n", "\", line 12\n    options.add_argument(\"--disable-dev-shm-usage\")from selenium.webdriver.chrome.service import Service\n                                                   ^^^^\nSyntaxError: invalid syntax\n", "\", line 12\n    options.add_argument(\"--disable-dev-shm-usage\")from selenium.webdriver.chrome.service import Service\n                                                   ^^^^\nSyntaxError: invalid syntax\n", "\", line 12\n    options.add_argument(\"--disable-dev-shm-usage\")from selenium.webdriver.chrome.service import Service\n                                                   ^^^^\nSyntaxError: invalid syntax\n", "\", line 17\n    options.add_argument(\"--disable-dev-shm-usage\")from selenium.webdriver.chrome.service import Service\n                                                   ^^^^\nSyntaxError: invalid syntax\n"], "slugs": [{"slug": "selenium-open-page", "status": "failed"}, {"slug": "selenium-find-elements", "status": "failed"}, {"slug": "selenium-click-and-type", "status": "failed"}, {"slug": "selenium-read-text-and-assert", "status": "failed"}, {"slug": "selenium-take-screenshot", "status": "failed"}]}

========================================
❌ FAILED: 5/5 quests failed.

EF_RUN_WORLD_SUMMARY: 0/5 public tests passed.
```
### ❌ python_systems.json (Solution Mode)
```
DEBUG: files_from=../../docs/quests/python-systems-service-boundaries/workspace, resolved=D:\EvalForge\.claude\worktrees\wonderful-galileo-95a5e6\docs\quests\python-systems-service-boundaries\workspace
   ❌ ERROR: Workspace path not found: D:\EvalForge\.claude\worktrees\wonderful-galileo-95a5e6\docs\quests\python-systems-service-boundaries\workspace
👉 Running python-systems-resilient-job-runner [solution]...
DEBUG: files_from=../../docs/quests/python-systems-resilient-job-runner/workspace, resolved=D:\EvalForge\.claude\worktrees\wonderful-galileo-95a5e6\docs\quests\python-systems-resilient-job-runner\workspace
   ❌ ERROR: Workspace path not found: D:\EvalForge\.claude\worktrees\wonderful-galileo-95a5e6\docs\quests\python-systems-resilient-job-runner\workspace
👉 Running python-systems-observability-sli [solution]...
DEBUG: files_from=../../docs/quests/python-systems-observability-sli/workspace, resolved=D:\EvalForge\.claude\worktrees\wonderful-galileo-95a5e6\docs\quests\python-systems-observability-sli\workspace
   ❌ ERROR: Workspace path not found: D:\EvalForge\.claude\worktrees\wonderful-galileo-95a5e6\docs\quests\python-systems-observability-sli\workspace
👉 Running python-systems-performance-profile [solution]...
DEBUG: files_from=../../docs/quests/python-systems-performance-profile/workspace, resolved=D:\EvalForge\.claude\worktrees\wonderful-galileo-95a5e6\docs\quests\python-systems-performance-profile\workspace
   ❌ ERROR: Workspace path not found: D:\EvalForge\.claude\worktrees\wonderful-galileo-95a5e6\docs\quests\python-systems-performance-profile\workspace
👉 Running python-systems-platform-tooling [solution]...
DEBUG: files_from=../../docs/quests/python-systems-platform-tooling/workspace, resolved=D:\EvalForge\.claude\worktrees\wonderful-galileo-95a5e6\docs\quests\python-systems-platform-tooling\workspace
   ❌ ERROR: Workspace path not found: D:\EvalForge\.claude\worktrees\wonderful-galileo-95a5e6\docs\quests\python-systems-platform-tooling\workspace
EF_RUNNER_RESULT_JSON={"total": 7, "passed": 1, "failed": 6, "errors": ["", "", "", "", "", ""], "slugs": [{"slug": "python-data-forge", "status": "failed"}, {"slug": "python-loop", "status": "passed"}, {"slug": "python-systems-service-boundaries", "status": "failed"}, {"slug": "python-systems-resilient-job-runner", "status": "failed"}, {"slug": "python-systems-observability-sli", "status": "failed"}, {"slug": "python-systems-performance-profile", "status": "failed"}, {"slug": "python-systems-platform-tooling", "status": "failed"}]}

========================================
❌ FAILED: 6/7 quests failed.

EF_RUN_WORLD_SUMMARY: 1/7 public tests passed.
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
1 failed in 0.29s
.                                                                        [100%]
1 passed in 0.19s
[FAIL] sql-ignition
[FAIL] sql-select
[PASS] sql-where
```
### ❌ web_html_core.json (Solution Mode)
```
EF_RUNNER_RESULT_JSON={"total": 10, "passed": 0, "failed": 10, "errors": [], "slugs": [{"slug": "html-ignition", "status": "failed", "error": "No test files"}, {"slug": "html-tags-attributes", "status": "failed", "error": "No test files"}, {"slug": "html-links-images", "status": "failed", "error": "No test files"}, {"slug": "html-lists-tables", "status": "failed", "error": "No test files"}, {"slug": "html-forms-inputs", "status": "failed", "error": "No test files"}, {"slug": "html-semantic-layout", "status": "failed", "error": "No test files"}, {"slug": "html-accessibility-basics", "status": "failed", "error": "No test files"}, {"slug": "html-media-embed", "status": "failed", "error": "No test files"}, {"slug": "html-meta-seo", "status": "failed", "error": "No test files"}, {"slug": "html-debug-validate", "status": "failed", "error": "No test files"}]}

EF_RUN_WORLD_SUMMARY: 0/10 public tests passed.
```
