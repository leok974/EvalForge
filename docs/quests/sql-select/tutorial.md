# SQL Select

## Task (do this first)
Open `task.sql` and write **one SELECT query**.

### Output shape (must match exactly)
Return all rows, with **these columns in this exact order**:

1. `name`
2. `city`

### Rules
- Sort: `name` **ascending**
- No `WHERE` filters and no `LIMIT` are needed for this query.

> If the tests check ordering, `ORDER BY` is required. Assume they do.

---

## Data you're given
This quest uses a database that includes:

### Table: `users`
Columns:
- `id` (integer)
- `name` (text)
- `email` (text)
- `age` (integer)
- `city` (text)
- `is_active` (integer)

> If you ever forget what tables exist, run:
> `SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;`

---

## How to verify quickly
1) Click **Run**  
2) Open **Query Inspector → Result**  
3) Confirm:
- column names and order are exactly `name`, `city`
- sorted alphabetically by `name`

If failing:
- **Trace** shows the exact SQL that was graded
- **Result** shows what you actually returned

---

## Common pitfalls
- Wrong column order (tests are strict)
- Missing sort (SQL tables are unordered by default)
- Using `SELECT *` (fragile and will fail the shape check)

---

### Key terms (Codex)
SELECT, FROM, ORDER BY
