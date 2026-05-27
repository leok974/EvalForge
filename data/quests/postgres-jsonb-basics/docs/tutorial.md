# Working with JSONB in PostgreSQL

PostgreSQL's `jsonb` type stores JSON in a binary format that supports indexed lookups and rich operators.

## The -> and ->> operators

| Operator | Returns | Example |
|----------|---------|---------|
| `->` | JSON value | `payload->'user'` → `{"id": 42}` |
| `->>` | Text value | `payload->>'user_id'` → `"42"` |

Use `->>` when you need a plain text value for comparison or display.

## Extracting nested fields

```sql
SELECT
    event_type,
    payload->>'user_id' AS user_id,
    payload->>'status'  AS status
FROM webhook_events;
```

## Filtering by JSONB value

```sql
WHERE payload->>'status' = 'active'
```

This extracts the `status` key as text and compares it to the string `'active'`.

## Nested paths

For deeply nested JSON, use multiple operators or the `#>>` path operator:

```sql
payload->'meta'->>'source'        -- two levels deep
payload#>>'{meta,source}'         -- equivalent, path syntax
```

## When to use JSONB vs TEXT columns

Use JSONB for semi-structured data that you need to query against. Use TEXT for opaque blobs you will pass through without inspection. JSONB adds about 10-20% storage overhead but enables indexing with GIN indexes.
