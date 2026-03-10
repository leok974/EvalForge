---
title: GROUP BY
id: glossary/sql/group-by
world: sql
level: intermediate
tags: [fundamentals, aggregates, analytical]
related:
  - codex:glossary/sql/having
  - codex:glossary/sql/count
  - codex:glossary/sql/sum
---

# GROUP BY

## Definition
The `GROUP BY` clause is used to arrange identical data into groups. It "collapses" multiple rows with the same values into single summary rows, often to be used with aggregate functions like `COUNT()`, `SUM()`, or `AVG()`.

## Why It Matters
`GROUP BY` is the foundation of data summarization. Without it, you could only get totals for the *entire* table. With it, you can get totals *per category*, such as "Sales per Month," "Users per City," or "Orders per Customer."

## Mental Model
Think of `GROUP BY` as sorting your data into buckets based on a specific label. Once the data is in buckets, you can count the items in each bucket or sum up their values.

## Example
```sql
-- Find the number of users in each city
SELECT city, COUNT(*) AS user_count
FROM users
GROUP BY city;
```

## Pitfalls
- **Non-Aggregated Columns**: Every column in your `SELECT` list that isn't inside an aggregate function **must** be included in the `GROUP BY` clause. Failing to do this causes a common "not a GROUP BY expression" error.
- **Filtering Logic**: Remember that `WHERE` filters rows *before* they are grouped. If you need to filter the resulting groups, use `HAVING`.

## Related
- HAVING: Used to filter the summarized results *after* grouping.
- COUNT: The most common companion to GROUP BY.
