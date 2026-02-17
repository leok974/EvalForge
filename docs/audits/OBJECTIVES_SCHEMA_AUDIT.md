# Objectives Schema Audit Report

**Date:** 2026-02-17T18:16:02.257556  
**Status:** ❌ FAIL

## Summary

- **Total Quests Scanned:** 15
- **Total Objectives:** 9
- **Valid Quests:** 3
- **Invalid Quests:** 0
- **Quests with No Objectives:** 12

---

## ⚠️  Quests with No Objectives (12)

- **js-ignition-q1-console-and-functions** (World: world-js)
  - objectives_json is missing or empty

- **js-vars-q1-let-const-var** (World: world-js)
  - objectives_json is missing or empty

- **sql-ignition** (World: world-sql)
  - objectives_json is missing or empty

- **sql-select** (World: world-sql)
  - objectives_json is missing or empty

- **infra-ignition** (World: world-infra)
  - objectives_json is missing or empty

- **infra-ports-and-localhost** (World: world-infra)
  - objectives_json is missing or empty

- **agents-ignition** (World: world-agents)
  - objectives_json is missing or empty

- **agents-prompts-contracts** (World: world-agents)
  - objectives_json is missing or empty

- **git-ignition** (World: world-git)
  - objectives_json is missing or empty

- **git-init-clone** (World: world-git)
  - objectives_json is missing or empty

- **ml-ignition** (World: world-ml)
  - objectives_json is missing or empty

- **ml-numpy-basics** (World: world-ml)
  - objectives_json is missing or empty

---

## Validator Registry

**Supported Objective Kinds:**

`ast`, `exit_code`, `exit_code_zero`, `json_output`, `not_timed_out`, `source_regex`, `stdout_exact`, `stdout_json_eq`, `stdout_regex`, `tests_pass`

## Per-Kind Rule Requirements

| Kind | Required Fields |
|------|----------------|
| `ast` | (none) |
| `exit_code` | `expected` |
| `exit_code_zero` | (none) |
| `json_output` | `expected` |
| `not_timed_out` | (none) |
| `source_regex` | `pattern` |
| `stdout_exact` | `pattern` |
| `stdout_json_eq` | `expected` |
| `stdout_regex` | `pattern` |
| `tests_pass` | (none) |
