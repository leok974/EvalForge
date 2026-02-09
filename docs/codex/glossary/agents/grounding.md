---
title: Grounding
id: glossary/agents/grounding
world: agents
level: intermediate
tags: [agents, reliability, safety]
related:
  - codex:glossary/agents/citation
  - codex:glossary/agents/retrieval
  - codex:glossary/agents/rag
---

# Grounding

## Definition
**Grounding** means an agent's output is supported by verifiable sources (retrieved chunks, code, tests, or tool outputs). Grounding reduces hallucinations by requiring evidence.

## Usage
- Require citations or "evidence blocks" for key claims.
- Prefer tool-verified facts (tests passing, API responses) over guesses.
- Mark unknowns explicitly when evidence is missing.

## Example
```txt
Claim: "Your API returns 404 because the route isn't registered."
Grounding:
- Evidence: routes.py does not include /api/foo
- Evidence: curl /api/foo -> 404
```

## Pitfalls

* "Grounded" doesn't mean "correct" if the sources are wrong/outdated.
* Selective quoting can mislead; include the most relevant supporting lines.

## Related

* Citation: citations demonstrate grounding.
* Retrieval: retrieval provides sources for grounding.
* RAG: RAG relies on grounding.
