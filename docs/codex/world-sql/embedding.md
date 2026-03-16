---
title: Embedding
summary: A numerical representation of semantic meaning.
---

# Embedding

In the context of **pgvector** and machine learning, an **embedding** is a representation of data (usually text, images, or audio) as a list of numbers, also known as a **vector**.

## Why Embeddings?
Computers cannot understand the "meaning" of text directly. By converting text into a vector, we map semantic meaning to a coordinate in a high-dimensional space.
- **Similar meanings** result in vectors that are "close" to each other.
- **Different meanings** result in vectors that are "far" apart.

## The `vector` Type
The `pgvector` extension provides a native `vector` data type for PostgreSQL.
```sql
-- Example of an embedding column definition
CREATE TABLE fragments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(3) -- A vector with 3 dimensions
);
```

## Dimensions
The number of elements in the vector list is its **dimension**. Modern large language models (LLMs) used for production RAG (Retrieval Augmented Generation) often produce embeddings with 768 or 1536 dimensions.

In this world, we use smaller vectors (like 3 or 8 dimensions) to make the math easier to visualize.
ama.
