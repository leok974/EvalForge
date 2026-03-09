# SQL Where — Filtering with Purpose

## What we’re practicing
Today you’re learning how to *filter rows* in SQL using the `WHERE` clause.

A useful mental model:

**SELECT** chooses the columns you want,  
**FROM** chooses where the data comes from,  
**WHERE** chooses which rows are allowed through,  
**ORDER BY** controls the output order.

If you skip `WHERE`, you’re asking for *everything* — even if the question clearly asks for a subset.

---

## The task in one sentence
Return a directory of **active users from Detroit**, showing:

- `name`
- `city`

…and sort the result alphabetically by `name`.

---

## Step 1 — Confirm the data source
You will query the `users` table:

`users(id, name, email, age, city, is_active)`

Two columns matter for filtering:
- `city` (text)
- `is_active` (0 or 1)

---

## Step 2 — Build the query in four parts
1) **SELECT** the two required columns (`name`, `city`)  
2) **FROM** the `users` table  
3) **WHERE**:
   - `city = 'Detroit'`
   - `is_active = 1`
4) **ORDER BY** `name ASC`

Important: When you have multiple conditions in `WHERE`, combine them with `AND`.

---

## Worked example (concept demo)
Open `example.sql`. It demonstrates the shape of a filter query:

```sql
SELECT
  name,
  city
FROM users
WHERE is_active = 1
ORDER BY name ASC;
```

Notice:

* The `WHERE` clause is the “gate” that filters rows.
* `ORDER BY` still matters after filtering.

This example is **not** the quest answer — your quest requires a different filter combination.

---

## Your job

Open `task.sql` and update the query so it matches the requirements exactly:

* Columns: `name, city` (in that order)
* Filter: Detroit users only
* Filter: active users only (`is_active = 1`)
* Sort by name ascending

---

## Common mistakes

* Forgetting quotes around text: use `'Detroit'`, not `Detroit`
* Using `OR` instead of `AND` (that returns too many rows)
* Forgetting `ORDER BY` (tests can fail due to ordering)

---

## How to verify

1. Click **Run**
2. Open **Query Result**
3. Confirm:

* Every row has `city = Detroit`
* Rows appear only for active users
* Sorted by `name` ascending
