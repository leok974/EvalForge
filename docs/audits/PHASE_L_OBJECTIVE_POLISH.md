# Phase L: Objective Polish Report

**Date:** 2026-02-18
**Goal:** Enrich beginner quests with "source_regex" or "stdout_regex" checks to improve feedback beyond opaque "tests_pass" failures.

## Quests Polished

### 1. `node-ignition` (Node)
- **Previous:** Single `tests_pass` objective.
- **Added:** `source_regex` ("Code uses process.exit() for status codes").
- **Why:** Ensures learner explicitly handles exit codes as per spec, providing immediate feedback if missing.

### 2. `sql-select` (SQL)
- **Previous:** `tests_pass` + `fs_snapshot`.
- **Added:** `source_regex` ("Query uses SELECT statement").
- **Why:** Validates basic SQL syntax presence before running DB query tests, catching empty/wrong files early.

## Next Steps
- Monitor failure rates for these quests.
- Expand polish to other "Ignition" quests (Python, Infra) once they are fully scaffolded.
