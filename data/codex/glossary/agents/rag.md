# RAG (Retrieval-Augmented Generation)

## Definition
**RAG** is a pattern where you **retrieve relevant context** first, then **generate an answer using that context**. It’s used to ground answers in evidence instead of general guesswork.

## Tiny example
1) Retrieve top 3 document chunks about “refund policy”
2) Ask the model to answer using only those chunks
3) Include citations to chunk ids

## Common pitfall
If chunk ids are missing or unstable, citations become meaningless. Always include stable identifiers like `doc:chunk` and require “answer only from context; if insufficient, say so.”

## Related
Retrieval, Chunk, Grounding, Citation
