## Outcome
You will learn the basics of grounding an agent with retrieved information (RAG) so answers are based on provided sources instead of guesswork.

## Concept in 30 seconds
Grounding means “show your work.” In **RAG (Retrieval-Augmented Generation)**, you retrieve relevant chunks of information first, then generate an answer using only those chunks. This reduces hallucinations because the agent is constrained by evidence, and can include **citations** to show where each claim came from.

## Key terms
- **RAG**: Retrieve relevant context, then generate using that context.
- **Retrieval**: Finding the most relevant chunks for a query.
- **Chunk**: A small slice of a document used for retrieval.
- **Grounding**: Constraining answers to evidence you provide.
- **Citation**: A pointer to which chunk supports a claim.

## Walkthrough
1) Start with a user question (the query).
2) Retrieve relevant chunks from your knowledge source (top-k results).
3) Build a context block with those chunks and stable identifiers (chunk ids).
4) Ask the model to answer using only the provided chunks.
5) Require citations: each major claim should reference chunk ids.
6) Click **Run** to inspect retrieval + citations. Iterate on chunking/top-k if citations look wrong.
7) Use **Submit** when your answer is grounded and citations match the provided context.

## Example implementation
A minimal RAG pipeline in pseudocode. The key ideas: chunk ids, top-k retrieval, and citations.

```py
def retrieve(query: str, chunks: list[dict], k: int = 3) -> list[dict]:
    # In a real system you'd use embeddings or BM25.
    # Here we just fake "relevance" for demonstration.
    return chunks[:k]

def answer_with_citations(query: str, retrieved: list[dict]) -> dict:
    context = "\n\n".join([f"[{c['id']}] {c['text']}" for c in retrieved])
    prompt = f"""
You must answer using ONLY the context below.
For every key claim, include citations like [chunk-id].
If the context is insufficient, say so.

Question: {query}

Context:
{context}
"""
    # llm(prompt) returns a string; you would parse it into a structured result.
    return {"answer": "...", "citations": ["doc-1:chunk-2"]}

chunks = [
    {"id": "doc-1:chunk-1", "text": "RAG retrieves context before generation."},
    {"id": "doc-1:chunk-2", "text": "Grounding reduces hallucinations by using evidence."},
    {"id": "doc-2:chunk-1", "text": "Citations point to supporting sources."},
]
```

## Common mistakes
- **Generating an answer before retrieval** (you lose grounding).
- **Using giant chunks** (retrieval becomes noisy; citations become vague).
- **No stable chunk ids** (you can’t cite consistently).
- **Letting the model use “general knowledge”** instead of the provided context.
- **Citing chunks that don’t actually support the claim**.

## Check yourself
- What are the two steps in RAG?
- Why do chunk ids matter?
- What should the agent do if the retrieved context is insufficient?
