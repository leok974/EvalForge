# Tutorial: Performance Profiling

In system design, **Efficiency** is as important as correctness. Profiling helps us identify which parts of our code are slow.

## Big O Complexity
When searching a list for an item, the computer must check every element until it finds a match. This is **O(N)**. If you have `M` queries and `N` items, a nested loop search is **O(N * M)**.

## The Power of Sets
A **Set** in Python uses a Hash Table. This allows it to check for membership in **O(1)** time on average, regardless of how many items are in the set.

- **Cost to build set**: O(N)
- **Cost per search**: O(1)
- **Total Cost**: O(N + M)

## Deterministic Cost Models
In this quest, we use a simple "Op Count" to measure performance without relying on system clocks.

```python
# Naive Cost
comparisons = 0
for q in queries:
    for item in items:
        comparisons += 1
        if item == q:
            break
```

```python
# Set Cost
cost = len(items) + len(queries)
```

By comparing these numbers, you can mathematically prove why one approach is better as scale increases.
