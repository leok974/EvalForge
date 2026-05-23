# Filtering and Ranking

In PostgreSQL, the `WHERE` clause is processed before or during the ranking phase.

### The Hybrid Query
```sql
SELECT content
FROM historical_fragments
WHERE category = 'Politics'
ORDER BY embedding <=> '[0,0,1]'::vector
LIMIT 1;
```

This ensures that only 'Politics' documents are considered, and then we pick the best semantic match among them.

### Your Task
Retrieve the `fragment_id` and `content` for the top **1** fragment where the `category` is `'Astronomy'`. Order the results by Cosine distance to `'[0.9, 0.1, 0.1]'::vector`.
