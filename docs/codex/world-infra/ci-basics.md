---
title: "CI Basics"
world_id: world-infra
type: codex_entry
level: tier1
---

# CI Basics

CI is “your repo runs from a clean machine.”
It catches hidden dependencies and prevents regressions.

## What CI should do at Tier-1
- install deps
- lint/format (optional but helpful)
- run unit tests
- run minimal integration checks
- fail with clear logs

## Common pitfalls
- tests depend on local services not started in CI
- missing env vars
- nondeterministic timing (no readiness checks)

## Rule
If CI fails, fix the root cause — don’t “just rerun.”
