## Outcome
You will learn how to write a basic SELECT query to retrieve columns from a table and shape results using filters, ordering, and limits.

## Concept in 30 seconds
A SQL query asks the database for rows. `SELECT` chooses which columns to return, and `FROM` chooses the table. You can narrow results with `WHERE`, sort them with `ORDER BY`, and cap the output with `LIMIT`. The mental model: “Start broad, then filter, then sort, then limit.”

## Key terms
- **SELECT**: Chooses which columns to return.
- **FROM**: Chooses which table to read from.
- **WHERE**: Filters rows based on conditions.
- **ORDER BY**: Sorts rows by one or more columns.
- **LIMIT**: Restricts how many rows are returned.

## Walkthrough
1) Identify the table you need and the columns you care about.
2) Write `SELECT ... FROM ...` first and run it to confirm the base shape.
3) Add `WHERE` to filter down to the right rows.
4) Add `ORDER BY` so results are in the intended order.
5) Add `LIMIT` if the quest expects only top N rows.
6) Use **Run** to iterate; use **Submit** when the query matches the expected output.

## Example implementation
Basic retrieval:

```sql
SELECT id, name
FROM users;
```

Filter + sort + limit:

```sql
SELECT id, name, created_at
FROM users
WHERE active = true
ORDER BY created_at DESC
LIMIT 10;
```

## Common mistakes
- **Selecting `*`** when you should return only specific columns.
- **Forgetting the `WHERE` clause** and returning too many rows.
- **Sorting ascending vs descending incorrectly**.
- **Using single quotes for column names** (single quotes are for string values).
- **Writing `ORDER BY` before `WHERE`** (SQL clause order matters).

## Check yourself
- What does SELECT control vs FROM?
- When should you use WHERE?
- Why might LIMIT be useful in analytics or debugging?
