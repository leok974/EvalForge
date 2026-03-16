---
id: world-sql/pgvector_fundamentals
title: pgvector_fundamentals
world: sql
---

# pgvector Fundamentals

The `pgvector` extension adds vector similarity search capabilities to PostgreSQL. It allows you to store embeddings and perform fast searches for "nearest neighbors" in embedding space.

## The `vector` Type
When defining a schema, you specify the number of dimensions for the vector:
```sql
CREATE TABLE items (
  id serial PRIMARY KEY,
  embedding vector(3) -- A vector with 3 dimensions
);
```

## Distance Operators
pgvector provides three primary operators to calculate the "closeness" of vectors:

### L2 Distance
`<->` - Euclidean Distance. Best for physical distance, magnitude matters.

### Cosine Distance
`<=>` - Semantic similarity, ignores magnitude. Standard choice for text embeddings.

### Inner Product
`<#>` - Dot product, often used with normalized vectors.

## Why Cosine Distance?
For text embeddings, we usually care about the **angle** between concepts, not the length of the vector. **Cosine Distance (`<=>`)** measures this angle, making it the standard choice for "Semantic Search."
