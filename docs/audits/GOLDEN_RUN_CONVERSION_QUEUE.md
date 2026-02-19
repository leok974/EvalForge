# Golden Run Conversion Queue

**Date:** 2026-02-17T18:46:56.621169

This queue prioritizes quests that need to be converted to `golden.run.json`.

## 1. Spec-Only Quests (Blocked by Fixtures/Environment)

These quests have `golden.spec.json` but failed run capture previously.

| Quest Slug | World | Blocker | Fix Required |
|---|---|---|---|

## 2. Missing Golden Quests (Needs Investigation)

These quests have NO golden capture. Checking solution existence...

| Quest Slug | World | Status | Notes |
|---|---|---|---|
| `agents-ignition` | world-agents | ✅ Captured | Empty stdout (correct) |
| `agents-prompts-contracts` | world-agents | ✅ Captured | Empty stdout (correct) |
| `git-ignition` | world-git | ❌ Blocked | Needs Shell Runner |
| `git-init-clone` | world-git | ❌ Blocked | Needs Shell Runner |
| `infra-ignition` | world-infra | ❌ Blocked | Needs Shell Runner |
| `infra-ports-and-localhost` | world-infra | ❌ Blocked | Needs Shell Runner |
| `js-ignition-q1-console-and-functions` | world-js | ✅ Captured | Added Local JS Runner |
| `js-vars-q1-let-const-var` | world-js | ✅ Captured | Added Local JS Runner |
| `ml-ignition` | world-ml | ✅ Captured | Empty stdout (correct) |
| `ml-numpy-basics` | world-ml | ✅ Captured | Installed numpy, fixed Env |
| `python-ignition` | world-python | ✅ Captured | Created Solution |
| `sql-ignition` | world-sql | ✅ Captured | Via Python Wrapper |
| `sql-select` | world-sql | ✅ Captured | Via Python Wrapper |

## progress Tracking

- [ ] Phase B: Fix python-data-forge fixtures
- [ ] Phase C: Run batch capture for unblocked
- [ ] Phase D: Audit & Upgrade Objectives