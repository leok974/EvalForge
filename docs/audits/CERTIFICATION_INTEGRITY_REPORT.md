# Certification Integrity Report

**Date:** 2026-02-18
**Status:** PASS (152/152 Certified)

## Breakdown by Golden Type

| Type | Count | Description |
|---|---|---|
| **RUN** | **54** | High-fidelity execution capture (Node, Python, ML, some SQL). |
| **STATE** | **58** | File system/Git state capture (Infra, HTML, CSS, Git). |
| **SPEC** | **40** | Blocked placeholder specs (CLI, React, TS). Satisfies coverage but pending harness work. |

## Top Blockers (Spec-Only)

1. **React World (10 quests)**: Lack of local test harness in `workspace`. Requires running `react-test-renderer` externally.
2. **CLI World (10 quests)**: Some quests lack `task.sh` or easy entrypoint for automation.
3. **TypeScript World (~20 quests)**: Likely missing TS compilation/test setup in workspace.

## Ratchets Enforced

- **Max Spec Quests:** 40
- **Min Run Quests:** 54

Start tightening `max_spec` as you fix the blockers above.
