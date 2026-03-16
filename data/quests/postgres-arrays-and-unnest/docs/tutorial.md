## Concept
PostgreSQL supports arrays natively. Instead of creating a separate mapping table for simple lists (like tags or skills), you can store them directly in a `TEXT[]` column.

To work with this data in a relational way, you need a way to **flatten** the array into individual rows. That's where `UNNEST` comes in.

## Why It Matters
When you use `UNNEST()` in your `SELECT` clause, Postgres takes the array and produces **a separate row for each element in that array**, duplicating the other columns in the `SELECT` list. This is necessary if you want to group by those skills, join them against another table, or simply provide a flat report.

## Syntax Pattern
```sql
SELECT column_name, UNNEST(array_column_name) AS single_item
FROM table_name;
```

## Example
Given:
| name | skills |
|---|---|
| Alice | {Python, SQL} |

Running:
```sql
SELECT name, UNNEST(skills) AS skill 
FROM employees;
```

Produces:
| name | skill |
|---|---|
| Alice | Python |
| Alice | SQL |

## Common Mistake
Trying to group or join directly on an array when you actually need to operate on the individual elements. Always `UNNEST` first when you need element-level granularity.
