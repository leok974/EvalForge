# Training Grade Index

**Status:** CANONICAL
**Last Audit:** 2026-02-13

This index lists the canonical "Modern Wrappers" for all Training-Grade worlds.
Use these paths for all runners, testing, and development.

## Core Worlds

| World | Slug | Modern Wrapper | Runner | Status |
|---|---|---|---|---|
| **Python** | `world-python` | `data/questpacks/_modern/python_systems_core.json` | `scripts/run_python_questpack.py` | ✅ TRAINING-GRADE |
| **JavaScript** | `javascript_core` | `data/questpacks/_modern/javascript_core.json` | `node --test` | ✅ TRAINING-GRADE |
| **TypeScript** | `typescript_core` | `data/questpacks/_modern/typescript_core.json` | `scripts/run_ts_questpack.mjs` | ✅ TRAINING-GRADE |
| **Node.js** | `node_core` | `data/questpacks/_modern/node_core.json` | `node --test` | ✅ TRAINING-GRADE |
| **React** | `react_core` | `data/questpacks/_modern/react_core.json` | `node --test` | ✅ TRAINING-GRADE |
| **SQL** | `sql_core` | `data/questpacks/_modern/sql_core.json` | `scripts/run_sql_questpack.py` | ✅ TRAINING-GRADE |
| **Infra** | `infra_core` | `data/questpacks/_modern/infra_core.json` | `node --test` | ✅ TRAINING-GRADE |
| **Git** | `git_core` | `data/questpacks/_modern/git_core.json` | `scripts/run_git_questpack.py` | ✅ TRAINING-GRADE |
| **ML** | `ml_core` | `data/questpacks/_modern/ml_core.json` | `scripts/run_ml_questpack.py` | ✅ TRAINING-GRADE |
| **Docker** | `docker_core` | `data/questpacks/docker_core.json` | `node --test` | ✅ TRAINING-GRADE |
| **Web** | `web_core` | `data/questpacks/_modern/web_core.json` | `scripts/run_web_questpack.mjs` | ✅ TRAINING-GRADE |

## Prism & Labs

| World | Slug | Modern Wrapper | Runner | Status |
|---|---|---|---|---|
| **Prism JS** | `prism_js_core` | `data/questpacks/_modern/prism_js_core.json` | `node --test` | ✅ TRAINING-GRADE |
| **Prism TS** | `prism_ts_core` | `data/questpacks/_modern/prism_ts_core.json` | `scripts/run_ts_questpack.mjs` | ✅ TRAINING-GRADE |
| **Lab Workspace** | `lab_workspace` | `data/questpacks/_modern/lab_workspace.json` | `scripts/run_python_questpack.py` | ✅ TRAINING-GRADE |
| **Lab Hidden** | `lab_hidden_tests` | `data/questpacks/_modern/lab_hidden_tests.json` | `scripts/run_python_questpack.py` | ✅ TRAINING-GRADE |

## How to Verify

Run the unified verification script to test all modern worlds:

```bash
python scripts/verify_all_modern_worlds.py
```

This will generate:
- `docs/audits/FINAL_SWEEP_VERIFICATION.json`
- `docs/audits/FINAL_SWEEP_VERIFICATION.md`
