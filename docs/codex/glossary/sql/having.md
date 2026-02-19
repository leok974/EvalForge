---
title: HAVING
---

# Definition
Filters groups created by GROUP BY.

# Why It Matters
WHERE filters rows; HAVING filters groups.

# Minimal Example
```sql
HAVING COUNT(*) > 5
```

# Common Mistakes
* Using HAVING without GROUP BY.

# In EvalForge
* Tested in `sql-t2-groupby-having`.
