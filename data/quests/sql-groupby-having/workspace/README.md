# sql-groupby-having

Requirements:
- Count errors per service (`status='error'`)
- Return columns: `service`, `error_count`
- Only include services with error_count >= 2
- Order by error_count DESC, then service ASC
