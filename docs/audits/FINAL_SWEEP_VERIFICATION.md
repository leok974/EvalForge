# Final Sweep Verification Report

**Date:** 2026-05-21 16:04:13
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
| `react_core.json` | `solution` | ❌ | 0/10 | |
| `react_core.json` | `student` | ✅ (Expected) | 0/10 | |
| `sql_core.json` | `solution` | ✅ | 11/11 | |
| `sql_core.json` | `student` | ✅ (Expected) | 0/11 | |
| `sql_tier2.json` | `solution` | ❌ | 0/12 | |
| `sql_tier2.json` | `student` | ✅ (Expected) | 0/12 | |
| `sql_tier3.json` | `solution` | ✅ | 1/1 | |
| `sql_tier3.json` | `student` | ✅ (Expected) | 0/6 | |
| `typescript_core.json` | `solution` | ❌ | 0/10 | |
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
### ❌ react_core.json (Solution Mode)
```
  duration_ms: 42.701458
  location: '/app/data/quests/react-reducer-cart/grading/public/react-reducer-cart.public.test.mjs:1:1'
  failureType: 'testCodeFailure'
  exitCode: 1
  signal: ~
  error: 'test failed'
  code: 'ERR_TEST_FAILURE'
  ...
1..1
# tests 1
# suites 0
# pass 0
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 46.188003

EF_RUN_WORLD_SUMMARY: 0/10 quests passed.
EF_RUNNER_RESULT_JSON={"total":10,"passed":0,"failed":10,"errors":["react-ignition: react-ignition.public.test.mjs failed","react-components: react-components.public.test.mjs failed","react-props: react-props.public.test.mjs failed","react-conditional-render: react-conditional-render.public.test.mjs failed","react-lists: react-lists.public.test.mjs failed","react-state-counter: react-state-counter.public.test.mjs failed","react-state-toggle: react-state-toggle.public.test.mjs failed","react-effects-mount: react-effects-mount.public.test.mjs failed","react-context-theme: react-context-theme.public.test.mjs failed","react-reducer-cart: react-reducer-cart.public.test.mjs failed"],"slugs":[{"slug":"react-ignition","status":"failed"},{"slug":"react-components","status":"failed"},{"slug":"react-props","status":"failed"},{"slug":"react-conditional-render","status":"failed"},{"slug":"react-lists","status":"failed"},{"slug":"react-state-counter","status":"failed"},{"slug":"react-state-toggle","status":"failed"},{"slug":"react-effects-mount","status":"failed"},{"slug":"react-context-theme","status":"failed"},{"slug":"react-reducer-cart","status":"failed"}]}
```
### ❌ sql_tier2.json (Solution Mode)
```
[FAIL] sql-t2-indexes-explain
[FAIL] sql-t2-transactions-rollback
[FAIL] sql-t2-boss-data-quality-audit
EF_RUNNER_RESULT_JSON={"total": 12, "passed": 0, "failed": 12, "skipped": 0, "errors": [], "slugs": [{"slug": "sql-t2-groupby-having", "status": "failed"}, {"slug": "sql-t2-window-functions", "status": "failed"}, {"slug": "sql-t2-analytics-pack", "status": "failed"}, {"slug": "sql-t2-subqueries-exists", "status": "failed"}, {"slug": "sql-t2-cte-basics", "status": "failed"}, {"slug": "sql-t2-recursive-cte-hierarchy", "status": "failed"}, {"slug": "sql-t2-nulls-coalesce", "status": "failed"}, {"slug": "sql-t2-dates-grouping", "status": "failed"}, {"slug": "sql-t2-upsert-on-conflict", "status": "failed"}, {"slug": "sql-t2-indexes-explain", "status": "failed"}, {"slug": "sql-t2-transactions-rollback", "status": "failed"}, {"slug": "sql-t2-boss-data-quality-audit", "status": "failed"}]}

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
### ❌ typescript_core.json (Solution Mode)
```
=== Running 10 TS quests from data/questpacks/typescript_core.json in solution mode ===
❌ FAIL: ts-ignition
❌ FAIL: ts-vars
❌ FAIL: ts-types
❌ FAIL: ts-control
❌ FAIL: ts-arrays
❌ FAIL: ts-objects
❌ FAIL: ts-functions
❌ FAIL: ts-interfaces
❌ FAIL: ts-generics
❌ FAIL: ts-modules
EF_RUNNER_RESULT_JSON={"total":10,"passed":0,"failed":10,"errors":[],"slugs":[{"slug":"ts-ignition","status":"failed","error":"TAP version 13\n# node:internal/modules/esm/resolve:873\n#   throw new ERR_MODULE_NOT_FOUND(packageName, fileURLToPath(base), null);\n#         ^\n# Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'tsx' imported from /app/\n#     at packageResolve (node:internal/modules/esm/resolve:873:9)\n#     at moduleResolve (node:internal/modules/esm/resolve:946:18)\n#     at defaultResolve (node:internal/modules/esm/resolve:1188:11)\n#     at ModuleLoader.defaultResolve (node:internal/modules/esm/loader:708:12)\n#     at \\#cachedDefaultResolve (node:internal/modules/esm/loader:657:25)\n#     at ModuleLoader.resolve (node:internal/modules/esm/loader:640:38)\n#     at ModuleLoader.getModuleJobForImport (node:internal/modules/esm/loader:264:38)\n#     at ModuleLoader.import (node:internal/modules/esm/loader:605:34)\n#     at asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:112:36)\n#     at runEntryPointWithESMLoader (node:internal/modules/run_main:141:19) {\n#   code: 'ERR_MODULE_NOT_FOUND'\n# }\n# Node.js v20.20.2\n# Subtest: /tmp/ef-ts-ts-ignition-EgwyIv/grading/public/ts-ignition.public.test.mjs\nnot ok 1 - /tmp/ef-ts-ts-ignition-EgwyIv/grading/public/ts-ignition.public.test.mjs\n  ---\n  duration_ms: 26.028286\n  location: '/tmp/ef-ts-ts-ignition-EgwyIv/grading/public/ts-ignition.public.test.mjs:1:1'\n  failureType: 'testCodeFailure'\n  exitCode: 1\n  signal: ~\n  error: 'test failed'\n  code: 'ERR_TEST_FAILURE'\n  ...\n1..1\n# tests 1\n# suites 0\n# pass 0\n# fail 1\n# cancelled 0\n# skipped 0\n# todo 0\n# duration_ms 28.409263\n"},{"slug":"ts-vars","status":"failed","error":"TAP version 13\n# node:internal/modules/esm/resolve:873\n#   throw new ERR_MODULE_NOT_FOUND(packageName, fileURLToPath(base), null);\n#         ^\n# Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'tsx' imported from /app/\n#     at packageResolve (node:internal/modules/esm/resolve:873:9)\n#     at moduleResolve (node:internal/modules/esm/resolve:946:18)\n#     at defaultResolve (node:internal/modules/esm/resolve:1188:11)\n#     at ModuleLoader.defaultResolve (node:internal/modules/esm/loader:708:12)\n#     at \\#cachedDefaultResolve (node:internal/modules/esm/loader:657:25)\n#     at ModuleLoader.resolve (node:internal/modules/esm/loader:640:38)\n#     at ModuleLoader.getModuleJobForImport (node:internal/modules/esm/loader:264:38)\n#     at ModuleLoader.import (node:internal/modules/esm/loader:605:34)\n#     at asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:112:36)\n#     at runEntryPointWithESMLoader (node:internal/modules/run_main:141:19) {\n#   code: 'ERR_MODULE_NOT_FOUND'\n# }\n# Node.js v20.20.2\n# Subtest: /tmp/ef-ts-ts-vars-pnzf1k/grading/public/ts-vars.public.test.mjs\nnot ok 1 - /tmp/ef-ts-ts-vars-pnzf1k/grading/public/ts-vars.public.test.mjs\n  ---\n  duration_ms: 21.937577\n  location: '/tmp/ef-ts-ts-vars-pnzf1k/grading/public/ts-vars.public.test.mjs:1:1'\n  failureType: 'testCodeFailure'\n  exitCode: 1\n  signal: ~\n  error: 'test failed'\n  code: 'ERR_TEST_FAILURE'\n  ...\n1..1\n# tests 1\n# suites 0\n# pass 0\n# fail 1\n# cancelled 0\n# skipped 0\n# todo 0\n# duration_ms 24.408937\n"},{"slug":"ts-types","status":"failed","error":"TAP version 13\n# node:internal/modules/esm/resolve:873\n#   throw new ERR_MODULE_NOT_FOUND(packageName, fileURLToPath(base), null);\n#         ^\n# Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'tsx' imported from /app/\n#     at packageResolve (node:internal/modules/esm/resolve:873:9)\n#     at moduleResolve (node:internal/modules/esm/resolve:946:18)\n#     at defaultResolve (node:internal/modules/esm/resolve:1188:11)\n#     at ModuleLoader.defaultResolve (node:internal/modules/esm/loader:708:12)\n#     at \\#cachedDefaultResolve (node:internal/modules/esm/loader:657:25)\n#     at ModuleLoader.resolve (node:internal/modules/esm/loader:640:38)\n#     at ModuleLoader.getModuleJobForImport (node:internal/modules/esm/loader:264:38)\n#     at ModuleLoader.import (node:internal/modules/esm/loader:605:34)\n#     at asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:112:36)\n#     at runEntryPointWithESMLoader (node:internal/modules/run_main:141:19) {\n#   code: 'ERR_MODULE_NOT_FOUND'\n# }\n# Node.js v20.20.2\n# Subtest: /tmp/ef-ts-ts-types-pUJuhN/grading/public/ts-types.public.test.mjs\nnot ok 1 - /tmp/ef-ts-ts-types-pUJuhN/grading/public/ts-types.public.test.mjs\n  ---\n  duration_ms: 25.192959\n  location: '/tmp/ef-ts-ts-types-pUJuhN/grading/public/ts-types.public.test.mjs:1:1'\n  failureType: 'testCodeFailure'\n  exitCode: 1\n  signal: ~\n  error: 'test failed'\n  code: 'ERR_TEST_FAILURE'\n  ...\n1..1\n# tests 1\n# suites 0\n# pass 0\n# fail 1\n# cancelled 0\n# skipped 0\n# todo 0\n# duration_ms 27.856163\n"},{"slug":"ts-control","status":"failed","error":"TAP version 13\n# node:internal/modules/esm/resolve:873\n#   throw new ERR_MODULE_NOT_FOUND(packageName, fileURLToPath(base), null);\n#         ^\n# Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'tsx' imported from /app/\n#     at packageResolve (node:internal/modules/esm/resolve:873:9)\n#     at moduleResolve (node:internal/modules/esm/resolve:946:18)\n#     at defaultResolve (node:internal/modules/esm/resolve:1188:11)\n#     at ModuleLoader.defaultResolve (node:internal/modules/esm/loader:708:12)\n#     at \\#cachedDefaultResolve (node:internal/modules/esm/loader:657:25)\n#     at ModuleLoader.resolve (node:internal/modules/esm/loader:640:38)\n#     at ModuleLoader.getModuleJobForImport (node:internal/modules/esm/loader:264:38)\n#     at ModuleLoader.import (node:internal/modules/esm/loader:605:34)\n#     at asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:112:36)\n#     at runEntryPointWithESMLoader (node:internal/modules/run_main:141:19) {\n#   code: 'ERR_MODULE_NOT_FOUND'\n# }\n# Node.js v20.20.2\n# Subtest: /tmp/ef-ts-ts-control-vZjVfo/grading/public/ts-control.public.test.mjs\nnot ok 1 - /tmp/ef-ts-ts-control-vZjVfo/grading/public/ts-control.public.test.mjs\n  ---\n  duration_ms: 26.33851\n  location: '/tmp/ef-ts-ts-control-vZjVfo/grading/public/ts-control.public.test.mjs:1:1'\n  failureType: 'testCodeFailure'\n  exitCode: 1\n  signal: ~\n  error: 'test failed'\n  code: 'ERR_TEST_FAILURE'\n  ...\n1..1\n# tests 1\n# suites 0\n# pass 0\n# fail 1\n# cancelled 0\n# skipped 0\n# todo 0\n# duration_ms 29.040771\n"},{"slug":"ts-arrays","status":"failed","error":"TAP version 13\n# node:internal/modules/esm/resolve:873\n#   throw new ERR_MODULE_NOT_FOUND(packageName, fileURLToPath(base), null);\n#         ^\n# Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'tsx' imported from /app/\n#     at packageResolve (node:internal/modules/esm/resolve:873:9)\n#     at moduleResolve (node:internal/modules/esm/resolve:946:18)\n#     at defaultResolve (node:internal/modules/esm/resolve:1188:11)\n#     at ModuleLoader.defaultResolve (node:internal/modules/esm/loader:708:12)\n#     at \\#cachedDefaultResolve (node:internal/modules/esm/loader:657:25)\n#     at ModuleLoader.resolve (node:internal/modules/esm/loader:640:38)\n#     at ModuleLoader.getModuleJobForImport (node:internal/modules/esm/loader:264:38)\n#     at ModuleLoader.import (node:internal/modules/esm/loader:605:34)\n#     at asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:112:36)\n#     at runEntryPointWithESMLoader (node:internal/modules/run_main:141:19) {\n#   code: 'ERR_MODULE_NOT_FOUND'\n# }\n# Node.js v20.20.2\n# Subtest: /tmp/ef-ts-ts-arrays-n9STSf/grading/public/ts-arrays.public.test.mjs\nnot ok 1 - /tmp/ef-ts-ts-arrays-n9STSf/grading/public/ts-arrays.public.test.mjs\n  ---\n  duration_ms: 24.876879\n  location: '/tmp/ef-ts-ts-arrays-n9STSf/grading/public/ts-arrays.public.test.mjs:1:1'\n  failureType: 'testCodeFailure'\n  exitCode: 1\n  signal: ~\n  error: 'test failed'\n  code: 'ERR_TEST_FAILURE'\n  ...\n1..1\n# tests 1\n# suites 0\n# pass 0\n# fail 1\n# cancelled 0\n# skipped 0\n# todo 0\n# duration_ms 27.837221\n"},{"slug":"ts-objects","status":"failed","error":"TAP version 13\n# node:internal/modules/esm/resolve:873\n#   throw new ERR_MODULE_NOT_FOUND(packageName, fileURLToPath(base), null);\n#         ^\n# Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'tsx' imported from /app/\n#     at packageResolve (node:internal/modules/esm/resolve:873:9)\n#     at moduleResolve (node:internal/modules/esm/resolve:946:18)\n#     at defaultResolve (node:internal/modules/esm/resolve:1188:11)\n#     at ModuleLoader.defaultResolve (node:internal/modules/esm/loader:708:12)\n#     at \\#cachedDefaultResolve (node:internal/modules/esm/loader:657:25)\n#     at ModuleLoader.resolve (node:internal/modules/esm/loader:640:38)\n#     at ModuleLoader.getModuleJobForImport (node:internal/modules/esm/loader:264:38)\n#     at ModuleLoader.import (node:internal/modules/esm/loader:605:34)\n#     at asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:112:36)\n#     at runEntryPointWithESMLoader (node:internal/modules/run_main:141:19) {\n#   code: 'ERR_MODULE_NOT_FOUND'\n# }\n# Node.js v20.20.2\n# Subtest: /tmp/ef-ts-ts-objects-OMfroB/grading/public/ts-objects.public.test.mjs\nnot ok 1 - /tmp/ef-ts-ts-objects-OMfroB/grading/public/ts-objects.public.test.mjs\n  ---\n  duration_ms: 22.847818\n  location: '/tmp/ef-ts-ts-objects-OMfroB/grading/public/ts-objects.public.test.mjs:1:1'\n  failureType: 'testCodeFailure'\n  exitCode: 1\n  signal: ~\n  error: 'test failed'\n  code: 'ERR_TEST_FAILURE'\n  ...\n1..1\n# tests 1\n# suites 0\n# pass 0\n# fail 1\n# cancelled 0\n# skipped 0\n# todo 0\n# duration_ms 25.119792\n"},{"slug":"ts-functions","status":"failed","error":"TAP version 13\n# node:internal/modules/esm/resolve:873\n#   throw new ERR_MODULE_NOT_FOUND(packageName, fileURLToPath(base), null);\n#         ^\n# Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'tsx' imported from /app/\n#     at packageResolve (node:internal/modules/esm/resolve:873:9)\n#     at moduleResolve (node:internal/modules/esm/resolve:946:18)\n#     at defaultResolve (node:internal/modules/esm/resolve:1188:11)\n#     at ModuleLoader.defaultResolve (node:internal/modules/esm/loader:708:12)\n#     at \\#cachedDefaultResolve (node:internal/modules/esm/loader:657:25)\n#     at ModuleLoader.resolve (node:internal/modules/esm/loader:640:38)\n#     at ModuleLoader.getModuleJobForImport (node:internal/modules/esm/loader:264:38)\n#     at ModuleLoader.import (node:internal/modules/esm/loader:605:34)\n#     at asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:112:36)\n#     at runEntryPointWithESMLoader (node:internal/modules/run_main:141:19) {\n#   code: 'ERR_MODULE_NOT_FOUND'\n# }\n# Node.js v20.20.2\n# Subtest: /tmp/ef-ts-ts-functions-Oq066I/grading/public/ts-functions.public.test.mjs\nnot ok 1 - /tmp/ef-ts-ts-functions-Oq066I/grading/public/ts-functions.public.test.mjs\n  ---\n  duration_ms: 25.285422\n  location: '/tmp/ef-ts-ts-functions-Oq066I/grading/public/ts-functions.public.test.mjs:1:1'\n  failureType: 'testCodeFailure'\n  exitCode: 1\n  signal: ~\n  error: 'test failed'\n  code: 'ERR_TEST_FAILURE'\n  ...\n1..1\n# tests 1\n# suites 0\n# pass 0\n# fail 1\n# cancelled 0\n# skipped 0\n# todo 0\n# duration_ms 27.955224\n"},{"slug":"ts-interfaces","status":"failed","error":"TAP version 13\n# node:internal/modules/esm/resolve:873\n#   throw new ERR_MODULE_NOT_FOUND(packageName, fileURLToPath(base), null);\n#         ^\n# Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'tsx' imported from /app/\n#     at packageResolve (node:internal/modules/esm/resolve:873:9)\n#     at moduleResolve (node:internal/modules/esm/resolve:946:18)\n#     at defaultResolve (node:internal/modules/esm/resolve:1188:11)\n#     at ModuleLoader.defaultResolve (node:internal/modules/esm/loader:708:12)\n#     at \\#cachedDefaultResolve (node:internal/modules/esm/loader:657:25)\n#     at ModuleLoader.resolve (node:internal/modules/esm/loader:640:38)\n#     at ModuleLoader.getModuleJobForImport (node:internal/modules/esm/loader:264:38)\n#     at ModuleLoader.import (node:internal/modules/esm/loader:605:34)\n#     at asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:112:36)\n#     at runEntryPointWithESMLoader (node:internal/modules/run_main:141:19) {\n#   code: 'ERR_MODULE_NOT_FOUND'\n# }\n# Node.js v20.20.2\n# Subtest: /tmp/ef-ts-ts-interfaces-NezDxJ/grading/public/ts-interfaces.public.test.mjs\nnot ok 1 - /tmp/ef-ts-ts-interfaces-NezDxJ/grading/public/ts-interfaces.public.test.mjs\n  ---\n  duration_ms: 23.408109\n  location: '/tmp/ef-ts-ts-interfaces-NezDxJ/grading/public/ts-interfaces.public.test.mjs:1:1'\n  failureType: 'testCodeFailure'\n  exitCode: 1\n  signal: ~\n  error: 'test failed'\n  code: 'ERR_TEST_FAILURE'\n  ...\n1..1\n# tests 1\n# suites 0\n# pass 0\n# fail 1\n# cancelled 0\n# skipped 0\n# todo 0\n# duration_ms 25.867071\n"},{"slug":"ts-generics","status":"failed","error":"TAP version 13\n# node:internal/modules/esm/resolve:873\n#   throw new ERR_MODULE_NOT_FOUND(packageName, fileURLToPath(base), null);\n#         ^\n# Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'tsx' imported from /app/\n#     at packageResolve (node:internal/modules/esm/resolve:873:9)\n#     at moduleResolve (node:internal/modules/esm/resolve:946:18)\n#     at defaultResolve (node:internal/modules/esm/resolve:1188:11)\n#     at ModuleLoader.defaultResolve (node:internal/modules/esm/loader:708:12)\n#     at \\#cachedDefaultResolve (node:internal/modules/esm/loader:657:25)\n#     at ModuleLoader.resolve (node:internal/modules/esm/loader:640:38)\n#     at ModuleLoader.getModuleJobForImport (node:internal/modules/esm/loader:264:38)\n#     at ModuleLoader.import (node:internal/modules/esm/loader:605:34)\n#     at asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:112:36)\n#     at runEntryPointWithESMLoader (node:internal/modules/run_main:141:19) {\n#   code: 'ERR_MODULE_NOT_FOUND'\n# }\n# Node.js v20.20.2\n# Subtest: /tmp/ef-ts-ts-generics-a3pTLv/grading/public/ts-generics.public.test.mjs\nnot ok 1 - /tmp/ef-ts-ts-generics-a3pTLv/grading/public/ts-generics.public.test.mjs\n  ---\n  duration_ms: 23.284087\n  location: '/tmp/ef-ts-ts-generics-a3pTLv/grading/public/ts-generics.public.test.mjs:1:1'\n  failureType: 'testCodeFailure'\n  exitCode: 1\n  signal: ~\n  error: 'test failed'\n  code: 'ERR_TEST_FAILURE'\n  ...\n1..1\n# tests 1\n# suites 0\n# pass 0\n# fail 1\n# cancelled 0\n# skipped 0\n# todo 0\n# duration_ms 25.598323\n"},{"slug":"ts-modules","status":"failed","error":"TAP version 13\n# node:internal/modules/esm/resolve:873\n#   throw new ERR_MODULE_NOT_FOUND(packageName, fileURLToPath(base), null);\n#         ^\n# Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'tsx' imported from /app/\n#     at packageResolve (node:internal/modules/esm/resolve:873:9)\n#     at moduleResolve (node:internal/modules/esm/resolve:946:18)\n#     at defaultResolve (node:internal/modules/esm/resolve:1188:11)\n#     at ModuleLoader.defaultResolve (node:internal/modules/esm/loader:708:12)\n#     at \\#cachedDefaultResolve (node:internal/modules/esm/loader:657:25)\n#     at ModuleLoader.resolve (node:internal/modules/esm/loader:640:38)\n#     at ModuleLoader.getModuleJobForImport (node:internal/modules/esm/loader:264:38)\n#     at ModuleLoader.import (node:internal/modules/esm/loader:605:34)\n#     at asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:112:36)\n#     at runEntryPointWithESMLoader (node:internal/modules/run_main:141:19) {\n#   code: 'ERR_MODULE_NOT_FOUND'\n# }\n# Node.js v20.20.2\n# Subtest: /tmp/ef-ts-ts-modules-BFSQk5/grading/public/ts-modules.public.test.mjs\nnot ok 1 - /tmp/ef-ts-ts-modules-BFSQk5/grading/public/ts-modules.public.test.mjs\n  ---\n  duration_ms: 25.678682\n  location: '/tmp/ef-ts-ts-modules-BFSQk5/grading/public/ts-modules.public.test.mjs:1:1'\n  failureType: 'testCodeFailure'\n  exitCode: 1\n  signal: ~\n  error: 'test failed'\n  code: 'ERR_TEST_FAILURE'\n  ...\n1..1\n# tests 1\n# suites 0\n# pass 0\n# fail 1\n# cancelled 0\n# skipped 0\n# todo 0\n# duration_ms 28.65983\n"}]}

❌ TS questpack FAILED (0/10 passed)

EF_RUN_WORLD_SUMMARY: 0/10 public tests passed.
```
