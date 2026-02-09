---
title: Chunk
id: glossary/agents/chunk
world: agents
level: intermediate
tags: [agents, rag, retrieval]
related:
  - codex:glossary/agents/retrieval
  - codex:glossary/agents/rag
  - codex:glossary/agents/citation
---

# Chunk

## Definition
A **chunk** is a small piece of a larger document stored for retrieval. Chunking helps search work by indexing content in manageable units instead of whole files.

## Usage
- Split long docs into chunks (often 200–800 tokens) with overlap.
- Store chunk text + metadata (source, section, url, page).
- Retrieve top-k chunks to supply relevant context to an agent.

## Example
```json
{
  "chunk_id": "docs/codex/world-agents/retrieval.md#L40-L92",
  "source": "docs/codex/world-agents/retrieval.md",
  "text": "Retrieval finds the most relevant context...",
  "metadata": { "world": "agents", "section": "Retrieval", "tokens": 320 }
}
```

## Pitfalls

* Chunks that are too large reduce precision; too small lose meaning.
* No overlap can split definitions/examples apart, reducing usefulness.

## Related

* Retrieval: chunks are the unit of retrieval.
* RAG: RAG uses chunks for context.
* Citation: citations point to specific chunks.
