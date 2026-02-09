---
title: Retrieval
id: glossary/agents/retrieval
world: agents
level: intermediate
tags: [agents, search, rag]
related:
  - codex:glossary/agents/chunk
  - codex:glossary/agents/rag
  - codex:glossary/agents/grounding
---

# Retrieval

## Definition
**Retrieval** is the step where an agent searches a knowledge base to find relevant context for a question. The goal is to reduce guessing by bringing grounded source text into the prompt.

## Usage
Common retrieval steps:
- Embed query and chunks (vector search) and/or keyword search.
- Rank results (reranking).
- Select top-k chunks and pass them to the model.

## Example
```txt
User question: "Why is my reverse proxy returning 502?"
Retrieve: ["reverse-proxy.md#common-502", "healthchecks.md#readiness", ...]
Answer: uses retrieved snippets to propose fixes
```

## Pitfalls

* Retrieval returning irrelevant chunks leads to confident wrong answers.
* Stale indexes cause "missing knowledge" even if docs exist.

## Related

* Chunk: retrieval finds chunks.
* RAG: retrieval is the "R" in RAG.
* Grounding: retrieval provides grounding for answers.
