---
id: glossary/sql/timestamptz
title: timestamptz
world: sql
---

# timestamptz

`TIMESTAMPTZ` (Timestamp with Time Zone) is the industry-standard data type for storing date and time in PostgreSQL. 

## The Golden Rule of Time
Internally, PostgreSQL stores `TIMESTAMPTZ` values in **UTC**. When you query the data, Postgres converts it to the time zone of your current session (standardized to UTC in EvalForge).

## Why use TIMESTAMPTZ?
The standard `TIMESTAMP` type ignores time zones. If you move your database or server to a different region, `TIMESTAMP` values stay the same, which can lead to "phantom" time shifts. `TIMESTAMPTZ` is safer and more predictable.

## Usage
```sql
CREATE TABLE historical_fragments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    discovered_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

## Comparison
```sql
-- These are handled correctly across regions
SELECT * FROM logs 
WHERE occurred_at > '2023-10-01 00:00:00+00';
```

> [!IMPORTANT]
> In production environments, **always use `TIMESTAMPTZ`** for event logs, audit trails, and any transaction-critical timestamps.
