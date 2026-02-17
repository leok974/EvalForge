# Objectives Schema Audit Report

**Date:** 2026-02-17T18:22:17.230615  
**Status:** ✅ PASS

## Summary

- **Total Quests Scanned:** 16
- **Total Objectives:** 37
- **Valid Quests:** 16
- **Invalid Quests:** 0
- **Quests with No Objectives:** 0

---

## ✅ All Quests Valid!

No issues found. All objectives have proper kind+rule schema.
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
