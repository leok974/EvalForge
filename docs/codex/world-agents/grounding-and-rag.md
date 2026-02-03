# Grounding & RAG

Grounding means “use reality as truth.”

RAG (Retrieval-Augmented Generation) is a structured way to ground an agent in documents.

---

## Grounding rules

- Prefer file/tool outputs over model guesses
- Cite sources (file paths + snippets)
- If uncertain, inspect before acting

---

## Minimal RAG loop

1) Retrieve relevant chunks (search)
2) Summarize with citations
3) Apply to plan/decision
4) Verify via tool output

---

## Common RAG pitfalls

- retrieving too much (noise)
- retrieving irrelevant chunks
- not citing sources
- treating retrieval as proof (it’s evidence, not verification)

---

## EvalForge angle

RAG is best used for:
- policies
- runbooks
- architecture docs
- prior artifacts/reports
Then verified by:
- tests
- diffs
- runtime checks
