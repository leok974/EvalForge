# Using Distance Operators

In pgvector, distance is calculated using specific operators between two vector columns (or a column and a literal).

### Calculating Cosine Distance
To find how "semantically close" a fragment is to a target, use the `<=>` operator:

```sql
SELECT content, embedding <=> '[1,0,0]'::vector as distance
FROM historical_fragments;
```

> [!TIP]
> **Smaller numbers mean closer vectors.** A distance of `0` means the vectors are pointing in the exact same direction.

### Your Task
Retrieve the `fragment_id` and the **Cosine distance** between our fragments and the target vector `'[0.5, 0.5, 0.5]'::vector`. Alias the distance column as `distance`.
