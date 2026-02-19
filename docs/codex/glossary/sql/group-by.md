---
title: GROUP BY
---

# Definition
Groups rows sharing a property so aggregate functions apply to each group.

# Why It Matters
Essential for reporting.

# Minimal Example
```sql
SELECT cat, COUNT(*) FROM prod GROUP BY cat
```

# Common Mistakes
* Selecting non-aggregated columns not in GROUP BY.

# In EvalForge
* Tested in `sql-t2-groupby-having`.
