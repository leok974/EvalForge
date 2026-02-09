---
title: Citation
id: glossary/agents/citation
world: agents
level: beginner
tags: [agents, references, verification]
related:
  - codex:glossary/agents/grounding
  - codex:glossary/agents/chunk
  - codex:glossary/agents/rag
---

# Citation

## Definition
A **citation** is a reference that points to the source supporting a claim (a chunk, a file path + line range, a URL, or a tool result). Citations let users verify where information came from.

## Usage
- Cite the exact chunk/file used for an important statement.
- Prefer precise references (file + section or line range).
- Include multiple citations if multiple sources support the claim.

## Example
```txt
"Reverse proxies often fail due to missing upstream health checks." [docs/codex/world-infra/reverse-proxy.md#healthchecks]
```

## Pitfalls

* Vague citations ("from the docs") don't help verification.
* Citing irrelevant sources reduces trust.

## Related

* Grounding: citations prove grounding.
* Chunk: citations point to chunks.
* RAG: RAG systems produce citations.
