# Top-K Vector Retrieval

The core pattern of vector search is finding the **K most similar items** to a query vector.

## The Query Pattern
A typical Top-K query combines `ORDER BY` and `LIMIT`:

```sql
SELECT fragment_id, content
FROM historical_fragments
ORDER BY embedding <=> '[0.1, 0.5, 0.9]'::vector
LIMIT 5;
```

## How it Works
1. **Query Vector**: You provide a vector representing your search term (e.g., `'[0.1, 0.5, 0.9]'::vector`).
2. **Ranking**: The database calculates the distance between your query vector and every vector in the table using a distance operator like `<=>`.
3. **Sorting**: `ORDER BY` sorts the results from closest (most similar) to furthest.
4. **Capping**: `LIMIT K` returns only the top results.

## Performance
For small datasets, an **Exact Scan** (calculating every distance) is fast. For millions of rows, you would use an index like **HNSW** to speed up retrieval.
ama.
