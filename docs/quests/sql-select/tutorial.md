**SQL Select — Building a Directory (name + city)**

**What you’re practicing**
In this quest, you’re learning the basic shape of a SQL query:
**SELECT → FROM → ORDER BY**.

Think of it like asking the database a very specific question:

> “Show me each user’s name and city, sorted alphabetically by name.”

---

### Step 1 — Read the required output

Your result must have **exactly two columns**, in this order:

1. `name`
2. `city`

No extra columns. No missing columns. Column order matters.

---

### Step 2 — Choose the table

All the data you need is in the `users` table.

**Schema (for reference):**

* `users(id, name, email, age, city, is_active)`

You only need **name** and **city** for this quest.

---

### Step 3 — Write the query (the three required parts)

**A. SELECT** the two columns:

* `name`
* `city`

**B. FROM** the correct table:

* `users`

**C. ORDER BY** `name` ascending:

* This is important because tables are not “naturally sorted.”

---

### A worked example (read-only reference)

Open `example.sql` to see a correct, fully formatted query.
Your job is **not** to copy it blindly — it’s to understand why each line exists.

```sql
-- example.sql
-- A correct solution example for sql-select.
-- Goal: return each user's name and city, sorted by name.

SELECT
  name,
  city
FROM users
ORDER BY name ASC;
```

---

### Common mistakes (and how to avoid them)

* **Using `SELECT *`**
  This returns extra columns and will fail the output shape check.
* **Forgetting `ORDER BY`**
  Your rows may appear “random” and tests may fail.
* **Wrong column order**
  `city, name` is not the same as `name, city`.

---

### How to verify quickly

1. Click **Run**
2. Open **Query Result**
3. Confirm:

   * Columns are `name`, then `city`
   * Rows are sorted alphabetically by `name`

---

### Key terms for this quest

* `SELECT`
* `FROM`
* `ORDER BY`
* `WHERE` (not needed here)
* `LIMIT` (not needed here)
