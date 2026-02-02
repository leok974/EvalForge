# Retrieval

## Definition
**Retrieval** is the step where you search a knowledge source (documents, database, vector index) to find the most relevant pieces of information for a query.

## Tiny example
Top-k retrieval: return the 3 most relevant chunks to “How do I reset my password?”

## Common pitfall
Retrieval quality depends on chunking. Giant chunks lead to noisy results; tiny chunks can lose context. Start with moderate chunk sizes and verify by checking whether the retrieved chunks actually answer the question.

## Related
RAG, Chunk
