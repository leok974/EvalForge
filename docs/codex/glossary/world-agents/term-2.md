---
title: Verifier
id: glossary/world-agents/term-2
world: world-agents
level: intermediate
tags: [agents, testing, reliability]
related:
  - codex:glossary/agents/grounding
  - codex:glossary/agents/rag
---

# Verifier

## Definition
**Verifier** is a step (or sub-agent) that checks whether an agent's proposed solution is actually correct—usually by running tests, validating schemas, or re-checking tool outputs.

## Usage
- Run unit tests or smoke checks after applying a patch.
- Validate that requirements are satisfied (starter fails, solution passes).
- Reject or revise proposals when verification fails.

## Example
```txt
Agent proposes fix → apply patch → run tests → verify green → finalize response
```

## Pitfalls

* Skipping verification turns the system into "guess and ship."
* Verifiers must be deterministic; flaky checks cause noise and mistrust.

## Related

* Grounding: verification grounds the solution in reality.
* RAG: RAG answers can be verified.
