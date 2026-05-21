# Final Sweep Verification Report

**Date:** 2026-05-21 16:58:49
**Status:** FINAL_VERIFICATION

## Summary

| Questpack | Mode | Status | Pass/Total | Notes |
|---|---|---|---|---|
| `agents_core.json` | `solution` | ✅ | N/A | |
| `agents_core.json` | `student` | ✅ (Expected) | N/A | |
| `cli_core.json` | `solution` | ✅ | 10/10 | |
| `cli_core.json` | `student` | ✅ (Expected) | 5/10 | |
| `docker_core.json` | `solution` | ✅ | 10/10 | |
| `docker_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `foundry_python.json` | `solution` | ✅ | 2/2 | |
| `foundry_python.json` | `student` | ✅ (Expected) | 0/2 | |
| `git_core.json` | `solution` | ✅ | 10/10 | |
| `git_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `git_tier2.json` | `solution` | ❌ | 0/3 | |
| `git_tier2.json` | `student` | ✅ (Expected) | 0/3 | |
| `infra_core.json` | `solution` | ✅ | 10/10 | |
| `infra_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `javascript_core.json` | `solution` | ✅ | 10/10 | |
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
| `sql_core.json` | `solution` | ✅ | 11/11 | |
| `sql_core.json` | `student` | ✅ (Expected) | 0/11 | |
| `sql_tier2.json` | `solution` | ❌ | 10/12 | |
| `sql_tier2.json` | `student` | ✅ (Expected) | 0/12 | |
| `sql_tier3.json` | `solution` | ✅ | 6/6 | |
| `sql_tier3.json` | `student` | ✅ (Expected) | 0/6 | |
| `typescript_core.json` | `solution` | ✅ | 10/10 | |
| `typescript_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `web_css_core.json` | `solution` | ✅ | 10/10 | |
| `web_css_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `web_html_core.json` | `solution` | ✅ | 10/10 | |
| `web_html_core.json` | `student` | ✅ (Expected) | 0/10 | |

## Detailed Failures

### ❌ git_tier2.json (Solution Mode)
```
=== Running 3 Git quests from data/questpacks/_tier2/git_tier2.json in solution mode ===
EF_RUNNER_RESULT_JSON={"total":3,"passed":0,"failed":3,"errors":[],"slugs":[{"slug":"git-t2-merge-conflict","status":"failed"},{"slug":"git-t2-rebase","status":"failed"},{"slug":"git-t2-release","status":"failed"}]}

❌ Git questpack FAILED (0/3 passed)

EF_RUN_WORLD_SUMMARY: 0/3 public tests passed.
```
### ❌ sql_tier2.json (Solution Mode)
```
1 passed in 0.07s
[PASS] sql-t2-groupby-having
[PASS] sql-t2-window-functions
[PASS] sql-t2-analytics-pack
[PASS] sql-t2-subqueries-exists
[PASS] sql-t2-cte-basics
[PASS] sql-t2-recursive-cte-hierarchy
[PASS] sql-t2-nulls-coalesce
[PASS] sql-t2-dates-grouping
[FAIL] sql-t2-upsert-on-conflict
[PASS] sql-t2-indexes-explain
[FAIL] sql-t2-transactions-rollback
[PASS] sql-t2-boss-data-quality-audit
EF_RUNNER_RESULT_JSON={"total": 12, "passed": 10, "failed": 2, "skipped": 0, "errors": [], "slugs": [{"slug": "sql-t2-groupby-having", "status": "passed"}, {"slug": "sql-t2-window-functions", "status": "passed"}, {"slug": "sql-t2-analytics-pack", "status": "passed"}, {"slug": "sql-t2-subqueries-exists", "status": "passed"}, {"slug": "sql-t2-cte-basics", "status": "passed"}, {"slug": "sql-t2-recursive-cte-hierarchy", "status": "passed"}, {"slug": "sql-t2-nulls-coalesce", "status": "passed"}, {"slug": "sql-t2-dates-grouping", "status": "passed"}, {"slug": "sql-t2-upsert-on-conflict", "status": "failed"}, {"slug": "sql-t2-indexes-explain", "status": "passed"}, {"slug": "sql-t2-transactions-rollback", "status": "failed"}, {"slug": "sql-t2-boss-data-quality-audit", "status": "passed"}]}

Failed quests:
 - sql-t2-upsert-on-conflict
 - sql-t2-transactions-rollback

EF_RUN_WORLD_SUMMARY: 10/12 public tests passed.
```
