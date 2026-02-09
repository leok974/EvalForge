---
title: RAG
id: glossary/agents/rag
world: agents
level: intermediate
tags: [agents, architecture, generation]
related:
  - codex:glossary/agents/retrieval
  - codex:glossary/agents/grounding
  - codex:glossary/agents/citation
---

# RAG

## Definition
**RAG (Retrieval-Augmented Generation)** combines retrieval + generation. The model first retrieves relevant chunks, then uses them as context to produce a final answer.

## Usage
- Use RAG for questions that depend on project-specific docs.
- Keep retrieved text visible to the user (or cite it) for trust.
- Log retrieval results for debugging.

## Example
```txt
RAG pipeline:
1) Retrieve top-k chunks for the query
2) Rerank for relevance
3) Generate an answer that references those chunks
4) Provide citations to the chunk sources
```

## Pitfalls

* If you don't enforce grounding, the model may ignore retrieved context.
* Too many chunks can overwhelm the model; pick top-k with a reranker.

## Related

* Retrieval: RAG starts with retrieval.
* Grounding: RAG enables grounded answers.
* Citation: RAG answers should cite sources.
