# PostgreSQL: Timestamptz

In PostgreSQL, `TIMESTAMPTZ` (Timestamp with Time Zone) is the industry-standard way to store temporal data.

### Why use Timestamptz?
- **Normalization**: PostgreSQL stores values in UTC internally.
- **Context**: When you query the data, it is converted to the time zone of your current session (or remains UTC).
- **DST Safety**: Handles Daylight Saving Time transitions gracefully.

### Comparison
- `TIMESTAMP`: "Wall clock" time. No timezone context. Risky for global apps.
- `TIMESTAMPTZ`: Absolute point in time. Safer for logs and audit trails.

### Conversion Example
```sql
SELECT '2024-01-01 10:00:00'::timestamptz AT TIME ZONE 'UTC';
```
