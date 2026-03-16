---
title: Cosine Distance
summary: A measure of similarity between two vectors based on the angle between them.
---

# Cosine Distance

**Cosine distance** is one of the most common distance metrics used for text search and RAG (Retrieval Augmented Generation). It measures the similarity between two vectors based on the **angle** between them, rather than their magnitude.

## Why use Cosine Distance?
In text search, the length of a vector often corresponds to the length of the document. Two documents might have the exact same topic (same angle) but different lengths (different magnitudes). 
- **Cosine Distance** ignores the length and focuses only on the "direction" of the meaning.
- A distance of **0** means the vectors are identical in direction.
- A distance of **2** means they are complete opposites.

## Using `<=>` in pgvector
The `pgvector` extension uses the `<=>` operator to calculate cosine distance.

```sql
-- Find fragments closest to a target coordinate using cosine distance
SELECT 
  content, 
  embedding <=> '[0.5, 0.5, 0.5]'::vector AS distance
FROM historical_fragments
ORDER BY distance ASC
LIMIT 5;
```

> [!NOTE]
> Cosine **Similarity** is `1 - Cosine Distance`. In pgvector, we generally work with distance for easier sorting (`ORDER BY distance ASC`).
ama.
