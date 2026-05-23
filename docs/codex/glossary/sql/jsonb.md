---
id: glossary/sql/jsonb
title: jsonb
world: sql
---

# jsonb

**JSONB** (JSON Binary) is a PostgreSQL data type for storing semi-structured data. Unlike the standard `json` type, `jsonb` stores data in a decomposed binary format, which makes it slightly slower to input but **much faster** to query and process.

## Why JSONB?
It allows you to store flexible data (like raw API responses, user preferences, or dynamic metadata) without needing a rigid schema for every single field.

## Key Operators

### `->` (Get as JSON)
Returns a value from a JSON object as a JSON type. Used for chaining.
```sql
-- returns {"name": "Alice"} as jsonb
SELECT payload -> 'user' FROM events;
```

### `->>` (Get as Text)
Returns a value from a JSON object as a standard string. Used for filtering and comparisons.
```sql
-- returns "Alice" as text
SELECT payload -> 'user' ->> 'name' FROM events;
```

### `@>` (Contains)
Checks if a JSONB document contains a specific set of keys and values.
```sql
-- Find events where the metadata has "status": "error"
SELECT * FROM events 
WHERE metadata @> '{"status": "error"}';
```

## Example
```sql
SELECT 
    event_type,
    payload ->> 'source' as source
FROM webhook_events
WHERE payload -> 'user' ->> 'email' = 'dev@evalforge.com';
```

> [!TIP]
> Always use `jsonb` instead of `json` unless you have a very specific reason to preserve the exact whitespace and key order of the original JSON string.
