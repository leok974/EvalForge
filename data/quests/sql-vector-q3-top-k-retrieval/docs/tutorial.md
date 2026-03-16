# Top-K Query Pattern

To perform a vector search, you follow a simple three-step pattern:

1. **Calculate distance**: Use `<=>`.
2. **Order results**: Use `ORDER BY` on your distance calculation.
3. **Limit the count**: Use `LIMIT K`.

### Example
```sql
SELECT content
FROM historical_fragments
ORDER BY embedding <=> '[0,1,0]'::vector
LIMIT 3;
```

### Your Task
Retrieve the `fragment_id` and `content` for the top 2 fragments nearest to `'[0.1, 0.1, 0.9]'::vector`. Order them by their Cosine distance.
