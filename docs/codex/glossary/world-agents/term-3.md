---
title: Policy Guardrail
id: glossary/world-agents/term-3
world: world-agents
level: intermediate
tags: [agents, safety, control]
related:
  - codex:glossary/world-agents/term-2
  - codex:glossary/world-agents/term-1
  - codex:glossary/agents/grounding
---

# Policy Guardrail

## Definition
**Policy Guardrail** is a rule that constrains what an agent can do (or must do) to remain safe and reliable—like requiring approval, banning destructive actions, or enforcing evidence.

## Usage
- Require explicit user approval for destructive actions (delete/purge).
- Enforce "no placeholders" and "must cite sources" policies.
- Set budgets (time, token, tool-call limits) to prevent runaway behavior.

## Example
```txt
Guardrail: "Any database purge requires EF_PURGE_CONFIRM=1"
Guardrail: "Any explanation must cite retrieved chunks"
```

## Pitfalls

* Too strict guardrails can block productivity; calibrate per environment (dev vs prod).
* Guardrails without enforcement become documentation-only and drift over time.

## Related

* Verifier: verifiers enforce guardrails (Term 2).
* Tool Contract: contracts enforce schema guardrails (Term 1).
* Grounding: grounding is a common policy.
