# Mission Hints: Schema Exploration

Need a hand navigating the archives? Use these gated hints to guide your tactical approach.

## Hint 1 — The Master Schema
PostgreSQL stores metadata about all tables in a special schema called `information_schema`. You can query the `tables` table there to see what exists.

## Hint 2 — Filtering by Schema
By default, `information_schema.tables` shows everything, including internal Postgres tables. You likely want to filter where `table_schema = 'public'`.

## Hint 3 — Finding Columns
If you need to know which columns a table has, check `information_schema.columns`. You can filter by `table_name` and `table_schema`.
