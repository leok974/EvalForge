# PostgreSQL: Arrays

PostgreSQL strongly supports arrays as a first-class data type. You can store a list of values directly in a single column instead of requiring a separate associative table.

### Why use Arrays?
- **Simplicity**: Quick way to store tags, skills, or multiple flags without complex normalized tables.
- **Performance**: Keeps related data physically together.

### Syntax
An array type is defined by appending `[]` to the base type, e.g., `TEXT[]` or `INTEGER[]`.

### Array Literals
You can create arrays using the `ARRAY[]` constructor or string literal syntax:
```sql
-- Constructor syntax
SELECT ARRAY['Python', 'SQL', 'Go'];

-- String literal syntax
SELECT '{Python, SQL, Go}'::TEXT[];
```

### Querying Arrays
To check if an array contains a specific value, the most powerful tool is the `ANY` operator.

#### The ANY() Operator
The `ANY()` operator checks if a condition is true for at least one element in an array. To check if an array contains 'SQL':

```sql
SELECT name 
FROM employees
WHERE 'SQL' = ANY(skills);
```
*(This translates to "Is 'SQL' equal to any of the elements inside the skills array?")*

### Common Mistake
Treating arrays like comma-separated strings. You cannot use `LIKE '%SQL%'` on an array reliably. Use `= ANY(matrix)` or the contains operator (`@>`).
