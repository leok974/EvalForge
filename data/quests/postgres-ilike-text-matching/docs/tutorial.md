## Concept
When working with real-world user data, text is rarely clean. Users might type `bob@example.com`, `Bob@Example.com`, or `BOB@EXAMPLE.COM`.

In PostgreSQL, the `ILIKE` operator provides **case-insensitive pattern matching**. It is the forgiving sibling of the strict `LIKE` operator.

## Why It Matters
A strict `LIKE '%@example.com'` search will miss any row where the user capitalized "Example". Using `ILIKE` ensures you find all relevant records without needing to manually convert everything to lowercase first using `LOWER(email)`.

## Syntax Pattern
```sql
SELECT column_name
FROM table_name
WHERE text_column ILIKE '%pattern%';
```

## Example
To find anyone with "admin" in their name, regardless of capitalization (Admin, admin, ADMIN):
```sql
SELECT name, email
FROM employees
WHERE name ILIKE '%admin%';
```

## Common Mistake
Using strict `=` or `LIKE` on user-input text and wondering why half your expected results are missing. Always default to `ILIKE` when searching human-entered string data unless you strictly require case sensitivity.
