# Hints: Building a Directory

## Hint 1 — Basic Structure
Every query in this quest needs at least a `SELECT` and a `FROM` clause.
`SELECT name, city FROM users;`

## Hint 2 — Sorting the Results
To sort your results, use the `ORDER BY` clause at the end of your query.
`ORDER BY name ASC;`

## Hint 3 — Putting it all together
Combine both to get the list of users and their cities, sorted alphabetically by name.
```sql
SELECT name, city
FROM users
ORDER BY name ASC;
```
