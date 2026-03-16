# PostgreSQL: ILIKE

In PostgreSQL, `ILIKE` is used for case-insensitive pattern matching. It works exactly like `LIKE` but ignores the case of the letters.

### Why use ILIKE?
- **Data Cleanup**: Often user inputs like emails or names are inconsistently capitalized.
- **Search**: When you want to find all variations of a word (e.g. "Smith", "smith", "SMITH").
- **Robustness**: Makes queries less brittle to accidental data entry variations.

### Comparison
- `=`: Exact case-sensitive match. `'Admin' = 'admin'` is FALSE.
- `LIKE`: Case-sensitive pattern match. `'Admin' LIKE 'admin%'` is FALSE.
- `ILIKE`: Case-insensitive pattern match. `'Admin' ILIKE 'admin%'` is TRUE.

### Wildcards
- `%`: Matches any sequence of zero or more characters.
- `_`: Matches any single character.

### Example
```sql
-- Finds "john.doe@example.com", "JOHN.DOE@EXAMPLE.COM"
SELECT name, email
FROM employees
WHERE email ILIKE '%@example.com';
```

### Common Mistake
Using `LIKE` when you actually want case-insensitive search. If you use `LIKE '%admin%'`, you will miss `"Admin"` or `"ADMIN"`.
