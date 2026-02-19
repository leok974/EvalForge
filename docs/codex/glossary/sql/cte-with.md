---
title: CTE (Common Table Expression)
---

# Definition
A temporary result set defined within the execution of a statement.

# Why It Matters
Improves readability and allows recursion.

# Minimal Example
```sql
WITH ActiveUsers AS (...)
```

# Common Mistakes
* Assuming it persists like a temp table.

# In EvalForge
* Tested in `sql-t2-analytics-pack`.
