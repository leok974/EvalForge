# Hints

<details>
  <summary><strong>Hint 1 — Keep it minimal</strong></summary>

You only need:

```sql
SELECT name, city
FROM users
ORDER BY name ASC;
```

</details>

<details>
  <summary><strong>Hint 2 — Column order matters</strong></summary>

Even if your data is correct, tests can fail if you return `city, name` instead of `name, city`.

</details>
