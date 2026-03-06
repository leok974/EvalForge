# Mission: Filter the Data

**World:** SQL Fundamentals — **Quest:** WHERE Clause

---

## Situation

The `users` table in the Archive contains both active and inactive agents. An inactive agent's records should never appear in mission-critical reports.

Your task: write a query that returns **only active users** — their `id`, `name`, and `city` — sorted alphabetically by name.

---

## Objectives

1. **Select the right columns** — return `id`, `name`, and `city` only
2. **Filter inactive users** — use `WHERE is_active = 1`
3. **Order the results** — sort by `name ASC`

Expected result: **4 rows** (Alice, Bob, Diana, Fay — Charlie and Evan are inactive)

---

## Schema (reference)

```sql
users(id, name, email, age, city, is_active)
```

`is_active` is `1` for active users, `0` for inactive.
