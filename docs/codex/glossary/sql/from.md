---
title: FROM
id: glossary/sql/from
world: sql
level: beginner
tags: [queries, fundamentals, tables]
related:
  - codex:glossary/world-sql/term-2
  - codex:glossary/sql/select
  - codex:glossary/sql/where
---

# FROM

## Definition
`FROM` defines the source table(s) for your query. It can reference tables, views, subqueries, and CTEs, and it's where joins are attached.

## Usage
- Specify the dataset you're querying.
- Add joins to combine tables.
- Reference subqueries or CTEs as tables.

## Example
```sql
SELECT id, email
FROM users;
```

## Pitfalls

* Forgetting join conditions can cause huge row multiplication.
* Subqueries in `FROM` should be aliased.

## Related

* JOIN: joins are attached in the FROM clause (Term 2).
* SELECT: SELECT pulls columns from FROM tables.
* WHERE: WHERE filters FROM results.
