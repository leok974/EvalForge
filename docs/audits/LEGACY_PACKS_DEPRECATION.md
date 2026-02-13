# Legacy Questpacks Deprecation

**Date:** 2026-02-13
**Status:** DEPRECATED

The files in `data/questpacks/*.json` (root) are **DEPRECATED**. 
All tooling and usage should now use the canonical "Modern Wrappers" located in `data/questpacks/_modern/`.

## Deprecation Mapping

| Legacy Pack (DEPRECATED) | Modern Pack (CANONICAL) | Status |
|---|---|---|
| `agents_core.json` | `_modern/agents_core.json` | ✅ Mapped |
| `cli_core.json` | `_modern/cli_core.json` | ✅ Mapped |
| `git_core.json` | `_modern/git_core.json` | ✅ Mapped |
| `infra_core.json` | `_modern/infra_core.json` | ✅ Mapped |
| `javascript_core.json` | `_modern/javascript_core.json` | ✅ Mapped |
| `ml_core` (folder/legacy idea) | `_modern/ml_core.json` | ✅ Mapped |
| `node_core.json` | `_modern/node_core.json` | ✅ Mapped |
| `prism_js.json` | `_modern/prism_js_core.json` | ✅ Mapped |
| `prism_typescript.json` | `_modern/prism_ts_core.json` | ✅ Mapped |
| `python_foundry.json` | `_modern/python_foundry_core.json` | ✅ Mapped |
| `python_systems.json` | `_modern/python_systems_core.json` | ✅ Mapped |
| `react_core.json` | `_modern/react_core.json` | ✅ Mapped |
| `sql_core.json` | `_modern/sql_core.json` | ✅ Mapped |
| `typescript_core.json` | `_modern/typescript_core.json` | ✅ Mapped |
| `web_core.json` | `_modern/web_core.json` | ✅ Mapped |
| `web_css_core.json` | `_modern/web_css_core.json` | ✅ Mapped |
| `web_html_core.json` | `_modern/web_html_core.json` | ✅ Mapped |
| `lab_workspace.json` | `_modern/lab_workspace.json` | ✅ Mapped |
| `lab_hidden_tests.json` | `_modern/lab_hidden_tests.json` | ✅ Mapped |

## Guidance

1. **Do not edit** the legacy JSON files.
2. **Do not run** tests against legacy paths if a modern one exists.
3. All `run_world_public_tests.mjs` calls should point to `data/questpacks/_modern/...`.
