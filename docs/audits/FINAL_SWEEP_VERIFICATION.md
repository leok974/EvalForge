# Final Sweep Verification Report

**Date:** 2026-05-16 18:31:39
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
| `infra_core.json` | `solution` | ❌ | 0/10 | |
| `infra_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `javascript_core.json` | `solution` | ❌ | 9/10 | |
| `javascript_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `ml_core.json` | `solution` | ✅ | 10/10 | |
| `ml_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `node_core.json` | `solution` | ✅ | 10/10 | |
| `node_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `python_selenium.json` | `solution` | ✅ | 5/5 | |
| `python_selenium.json` | `student` | ✅ (Expected) | 3/5 | |
| `python_systems.json` | `solution` | ✅ | 7/7 | |
| `python_systems.json` | `student` | ✅ (Expected) | 0/7 | |
| `python_tier2.json` | `solution` | ✅ | 6/6 | |
| `python_tier2.json` | `student` | ✅ (Expected) | 0/6 | |
| `react_core.json` | `solution` | ✅ | 10/10 | |
| `react_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `sql_core.json` | `solution` | ❌ | N/A | |
| `sql_core.json` | `student` | ✅ (Expected) | 1/11 | |
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
### ❌ infra_core.json (Solution Mode)
```
    wrappedFn (node:internal/errors:537:14)
    ChildProcess.exithandler (node:child_process:417:12)
    ChildProcess.emit (node:events:518:28)
    maybeClose (node:internal/child_process:1101:16)
    Socket.<anonymous> (node:internal/child_process:456:11)
    Socket.emit (node:events:518:28)
    Pipe.<anonymous> (node:net:346:12)
  ...
1..1
# tests 1
# suites 0
# pass 0
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 197.7802

EF_RUN_WORLD_SUMMARY: 0/10 quests passed.
EF_RUNNER_RESULT_JSON={"total":10,"passed":0,"failed":10,"errors":["infra-ignition: infra-ignition.public.test.mjs failed","infra-ports-and-localhost: infra-ports-and-localhost.public.test.mjs failed","infra-env-config: infra-env-config.public.test.mjs failed","infra-healthchecks: infra-healthchecks.public.test.mjs failed","infra-logs-metrics: infra-logs-metrics.public.test.mjs failed","infra-docker-compose: infra-docker-compose.public.test.mjs failed","infra-networking-dns: infra-networking-dns.public.test.mjs failed","infra-reverse-proxy: infra-reverse-proxy.public.test.mjs failed","infra-cors-cookies: infra-cors-cookies.public.test.mjs failed","infra-debug-playbook: infra-debug-playbook.public.test.mjs failed"],"slugs":[{"slug":"infra-ignition","status":"failed"},{"slug":"infra-ports-and-localhost","status":"failed"},{"slug":"infra-env-config","status":"failed"},{"slug":"infra-healthchecks","status":"failed"},{"slug":"infra-logs-metrics","status":"failed"},{"slug":"infra-docker-compose","status":"failed"},{"slug":"infra-networking-dns","status":"failed"},{"slug":"infra-reverse-proxy","status":"failed"},{"slug":"infra-cors-cookies","status":"failed"},{"slug":"infra-debug-playbook","status":"failed"}]}
```
### ❌ javascript_core.json (Solution Mode)
```
  type: 'test'
  ...
# Subtest: Default export circleArea
ok 2 - Default export circleArea
  ---
  duration_ms: 0.1029
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
# duration_ms 56.1343

EF_RUN_WORLD_SUMMARY: 9/10 quests passed.
EF_RUNNER_RESULT_JSON={"total":10,"passed":9,"failed":1,"errors":["js-vars-q1-let-const-var: js-vars-q1-let-const-var.public.test.mjs failed"],"slugs":[{"slug":"js-ignition-q1-console-and-functions","status":"passed"},{"slug":"js-vars-q1-let-const-var","status":"failed"},{"slug":"js-control-q1-if-else-loops","status":"passed"},{"slug":"js-arrays-q1-basics","status":"passed"},{"slug":"js-arrays-q2-map-filter-reduce","status":"passed"},{"slug":"js-objects-q1-properties-methods","status":"passed"},{"slug":"js-functions-q1-arrow-vs-regular","status":"passed"},{"slug":"js-async-q1-promises-basics","status":"passed"},{"slug":"js-errors-q1-try-catch","status":"passed"},{"slug":"js-modules-q1-import-export","status":"passed"}]}
```
### ❌ sql_core.json (Solution Mode)
```
            "plan_rows": []
        }
    
        try:
            # Load Schema
>           with open(schema_sql_path, "r", encoding="utf-8") as f:
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           FileNotFoundError: [Errno 2] No such file or directory: 'D:\\EvalForge\\.claude\\worktrees\\wonderful-galileo-95a5e6\\data\\quests\\sql-ignition\\fixtures\\schema.sql'

..\..\_shared\sql_test_helpers.py:114: FileNotFoundError
=========================== short test summary info ===========================
FAILED grading/public/test_sql_ignition.py::test_sql_ignition - FileNotFoundE...
1 failed in 0.27s
.                                                                        [100%]
1 passed in 0.12s
.                                                                        [100%]
1 passed in 0.18s
[FAIL] sql-ignition
[PASS] sql-select
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
