# Guardrails & Safety

Agent safety is engineered, not wished for.

---

## Guardrail checklist

- allowlist tools
- allowlist paths
- denylist destructive commands
- diff-only proposals by default
- approvals for risky actions
- strict verification gate
- budgets for retries/cost/time

---

## Safe defaults

- read-only mode until proven safe
- dry-run for edits
- require tests before apply
- require “rollback instructions” in report

---

## Red flags

- editing auth without tests
- deploying without health checks
- changing DB schema without migration strategy
- wide-scope search/replace across repo
