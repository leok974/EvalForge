---
id: glossary/sql/on-conflict
title: on-conflict
world: sql
---

# on-conflict

The `ON CONFLICT` clause is a part of the `INSERT` statement in SQLite that defines the behavior of the database when a conflict occurs (such as violating a `UNIQUE` constraint or a `PRIMARY KEY`).

## Options

- **DO NOTHING**: Silently skip the insert if a conflict occurs.
- **DO UPDATE SET**: Perform an update on the existing row instead.

## Example: DO NOTHING

```sql
INSERT INTO user_logins (user_id) VALUES (1)
ON CONFLICT(user_id) DO NOTHING;
```

## Example: DO UPDATE

```sql
INSERT INTO user_logins (user_id, count) VALUES (1, 1)
ON CONFLICT(user_id) 
DO UPDATE SET count = user_logins.count + 1;
```