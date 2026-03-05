# Hints

<details>
  <summary><strong>Hint 1 — Start from the skeleton</strong></summary>

Make sure your query selects **name, city** in that exact order from the `users` table.

</details>

<details>
  <summary><strong>Hint 2 — Ordering is usually the failure</strong></summary>

If results look right but tests fail, you probably forgot to sort it:

```sql
ORDER BY name ASC
```

</details>

<details>
  <summary><strong>Hint 3 — Inspect schema if you're unsure</strong></summary>

List all tables:
```sql
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
```

Check columns for `users`:
```sql
PRAGMA table_info('users');
```

</details>
