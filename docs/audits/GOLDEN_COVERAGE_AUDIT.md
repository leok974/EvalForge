# Golden Coverage Audit Report

**Date:** 2026-02-19T10:22:02.451722  
**Status:** ✅ PASS

## Summary

- **Total Quests:** 152
- **With golden.run.json:** 112 ✅
- **With golden.spec.json only:** 40 📋
- **Missing golden capture:** 0 ❌

---

## ✅ All Quests Have Golden Captures!

## ✅ Quests with Golden Run Captures (112)

These quests have actual solution runs captured:

- **agents-approvals-diffs** (World: unknown)
- **agents-budgets** (World: unknown)
- **agents-executor** (World: unknown)
- **agents-ignition** (World: unknown) (using legacy golden.json (should migrate to golden.run.json))
- **agents-memory** (World: unknown)
- **agents-observability** (World: unknown)
- **agents-planner** (World: unknown)
- **agents-prompts-contracts** (World: unknown) (using legacy golden.json (should migrate to golden.run.json))
- **agents-tools-basics** (World: unknown)
- **agents-verifier** (World: unknown)
- **cli-env-vars** (World: unknown)
- **cli-exit-codes** (World: unknown)
- **cli-files-folders** (World: unknown)
- **cli-ignition** (World: unknown)
- **cli-navigation** (World: unknown)
- **cli-pipes** (World: unknown)
- **cli-processes** (World: unknown)
- **cli-redirection** (World: unknown)
- **cli-scripting** (World: unknown)
- **compose-basics** (World: unknown)
- **compose-env-secrets** (World: unknown)
- **compose-networks-depends** (World: unknown)
- **compose-volumes-and-prod-hardening** (World: unknown)
- **css-box-model** (World: unknown)
- **css-cascade-inheritance** (World: unknown)
- **css-colors-backgrounds** (World: unknown)
- **css-flexbox** (World: unknown)
- **css-grid** (World: unknown)
- **css-ignition** (World: unknown)
- **css-position-zindex** (World: unknown)
- **css-responsive-media** (World: unknown)
- **css-selectors-specificity** (World: unknown)
- **css-units-typography** (World: unknown)
- **docker-ignition** (World: unknown)
- **dockerfile-basics** (World: unknown)
- **dockerfile-copy-vs-add** (World: unknown)
- **dockerfile-healthcheck** (World: unknown)
- **dockerfile-layers-cache** (World: unknown)
- **dockerfile-multistage** (World: unknown)
- **first-sparks** (World: unknown)
- **git-add-commit** (World: unknown)
- **git-branch-merge** (World: unknown)
- **git-ignition** (World: unknown)
- **git-init-clone** (World: unknown)
- **git-rebase-linear** (World: unknown)
- **git-remote-push** (World: unknown)
- **git-stash** (World: unknown)
- **git-status-diff** (World: unknown)
- **git-tag-release** (World: unknown)
- **git-undo-revert** (World: unknown)
- **hello-variable** (World: unknown) (using legacy golden.json (should migrate to golden.run.json))
- **html-accessibility-basics** (World: unknown)
- **html-debug-validate** (World: unknown)
- **html-forms-inputs** (World: unknown)
- **html-ignition** (World: unknown)
- **html-links-images** (World: unknown)
- **html-lists-tables** (World: unknown)
- **html-media-embed** (World: unknown)
- **html-meta-seo** (World: unknown)
- **html-semantic-layout** (World: unknown)
- **html-tags-attributes** (World: unknown)
- **infra-cors-cookies** (World: unknown)
- **infra-debug-playbook** (World: unknown)
- **infra-docker-compose** (World: unknown)
- **infra-env-config** (World: unknown)
- **infra-healthchecks** (World: unknown)
- **infra-ignition** (World: unknown)
- **infra-logs-metrics** (World: unknown)
- **infra-networking-dns** (World: unknown)
- **infra-ports-and-localhost** (World: unknown)
- **infra-reverse-proxy** (World: unknown)
- **js-ignition-q1-console-and-functions** (World: unknown) (using legacy golden.json (should migrate to golden.run.json))
- **js-vars-q1-let-const-var** (World: unknown) (using legacy golden.json (should migrate to golden.run.json))
- **ml-classification-basics** (World: unknown)
- **ml-data-preprocessing** (World: unknown)
- **ml-ignition** (World: unknown) (using legacy golden.json (should migrate to golden.run.json))
- **ml-linear-regression** (World: unknown)
- **ml-model-evaluation** (World: unknown)
- **ml-neural-networks-intro** (World: unknown)
- **ml-numpy-basics** (World: unknown) (using legacy golden.json (should migrate to golden.run.json))
- **ml-overfitting-regularization** (World: unknown)
- **ml-pandas-dataframes** (World: unknown)
- **ml-train-test-split** (World: unknown)
- **node-async** (World: unknown)
- **node-deploy-basics** (World: unknown)
- **node-env-config** (World: unknown)
- **node-fs-path** (World: unknown)
- **node-http** (World: unknown)
- **node-ignition** (World: unknown)
- **node-middleware** (World: unknown)
- **node-modules** (World: unknown)
- **node-npm** (World: unknown)
- **node-testing** (World: unknown)
- **python-data-forge** (World: unknown) (using legacy golden.json (should migrate to golden.run.json))
- **python-loop** (World: unknown) (using legacy golden.json (should migrate to golden.run.json))
- **python-systems-observability-sli** (World: unknown)
- **python-systems-performance-profile** (World: unknown)
- **python-systems-platform-tooling** (World: unknown)
- **python-systems-resilient-job-runner** (World: unknown)
- **python-systems-service-boundaries** (World: unknown)
- **quest-py-hidden** (World: unknown)
- **quest-py-workspace** (World: unknown)
- **sql-aggregates** (World: unknown)
- **sql-cte-subquery** (World: unknown)
- **sql-groupby-having** (World: unknown)
- **sql-ignition** (World: unknown)
- **sql-insert-update-delete** (World: unknown)
- **sql-joins** (World: unknown)
- **sql-left-join-null** (World: unknown)
- **sql-order-limit** (World: unknown)
- **sql-select** (World: unknown)
- **sql-where** (World: unknown)

---

## 📋 Quests with Golden Spec Only (40)

These quests are blocked from golden run capture:

### cli-globs-search (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\cli-globs-search\grading\golden.spec.json`

### git-branches (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\git-branches\grading\golden.spec.json`

### git-log (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\git-log\grading\golden.spec.json`

### git-merge-conflict (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\git-merge-conflict\grading\golden.spec.json`

### git-rebase-onto-main (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\git-rebase-onto-main\grading\golden.spec.json`

### git-tags (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\git-tags\grading\golden.spec.json`

### js-arrays-q1-basics (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\js-arrays-q1-basics\grading\golden.spec.json`

### js-arrays-q2-map-filter-reduce (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\js-arrays-q2-map-filter-reduce\grading\golden.spec.json`

### js-async-q1-promises-basics (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\js-async-q1-promises-basics\grading\golden.spec.json`

### js-control-q1-if-else-loops (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\js-control-q1-if-else-loops\grading\golden.spec.json`

### js-errors-q1-try-catch (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\js-errors-q1-try-catch\grading\golden.spec.json`

### js-functions-q1-arrow-vs-regular (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\js-functions-q1-arrow-vs-regular\grading\golden.spec.json`

### js-modules-q1-import-export (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\js-modules-q1-import-export\grading\golden.spec.json`

### js-objects-q1-properties-methods (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\js-objects-q1-properties-methods\grading\golden.spec.json`

### quest-ts-hello-console (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\quest-ts-hello-console\grading\golden.spec.json`

### quest-ts-hello-variable (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\quest-ts-hello-variable\grading\golden.spec.json`

### quest-ts-loop-countdown (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\quest-ts-loop-countdown\grading\golden.spec.json`

### react-components (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\react-components\grading\golden.spec.json`

### react-conditional-render (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\react-conditional-render\grading\golden.spec.json`

### react-context-theme (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\react-context-theme\grading\golden.spec.json`

### react-effects-mount (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\react-effects-mount\grading\golden.spec.json`

### react-ignition (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\react-ignition\grading\golden.spec.json`

### react-lists (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\react-lists\grading\golden.spec.json`

### react-props (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\react-props\grading\golden.spec.json`

### react-reducer-cart (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\react-reducer-cart\grading\golden.spec.json`

### react-state-counter (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\react-state-counter\grading\golden.spec.json`

### react-state-toggle (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\react-state-toggle\grading\golden.spec.json`

### ts-arrays (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-arrays\grading\golden.spec.json`

### ts-control (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-control\grading\golden.spec.json`

### ts-functions (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-functions\grading\golden.spec.json`

### ts-generics (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-generics\grading\golden.spec.json`

### ts-generics-q2-result-type (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-generics-q2-result-type\grading\golden.spec.json`

### ts-ignition (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-ignition\grading\golden.spec.json`

### ts-ignition-q1-types-and-interfaces (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-ignition-q1-types-and-interfaces\grading\golden.spec.json`

### ts-interfaces (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-interfaces\grading\golden.spec.json`

### ts-modules (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-modules\grading\golden.spec.json`

### ts-narrowing-q2-unions-and-guards (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-narrowing-q2-unions-and-guards\grading\golden.spec.json`

### ts-objects (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-objects\grading\golden.spec.json`

### ts-types (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-types\grading\golden.spec.json`

### ts-vars (World: unknown)

**Blocked Reason:** Missing entrypoint

**Path:** `data\quests\ts-vars\grading\golden.spec.json`

See [GOLDEN_BLOCKERS.md](GOLDEN_BLOCKERS.md) for resolution plan.

---

