# SQL Order By — Sorting with Two Keys

## What we’re practicing
Today you’re learning that sorting often requires **more than one key**.

A database will only sort by what you explicitly request. If two rows tie on the first sort key, you must provide a **second key** to guarantee a stable order.

Think of this as “alphabetize by city, then alphabetize by name within each city.”

---

## The task in one sentence
Return a directory of users showing:

- `city`
- `name`

…and sort:
1) by `city` ascending  
2) then by `name` ascending

---

## Step 1 — Confirm the columns and their order
Output must be exactly two columns, in this order:

1) `city`  
2) `name`

Column order is part of the contract.

---

## Step 2 — Multi-key ORDER BY
A multi-key sort looks like:

`ORDER BY first_key ASC, second_key ASC`

The first key groups rows. The second key orders *within each group*.

For this quest:
- first key: `city`
- second key: `name`

---

## Worked example (concept demo)
Open `example.sql`. It demonstrates multi-key sorting:

```sql
SELECT
  name,
  age
FROM users
ORDER BY age DESC, name ASC;
```

Notice:

* two keys in the ORDER BY clause
* the second key resolves ties on the first

This example is **not** the quest answer. Your quest requires a different output and different keys.

---

## Your job

Open `task.sql` and ensure:

* Columns are `city, name` (in that order)
* All rows included
* ORDER BY includes **two keys**: `city ASC, name ASC`

---

## Common mistakes

* Sorting by only one key (ties become unstable)
* Using the wrong column order in SELECT
* Sorting descending by accident

---

## How to verify

1. Click **Run**
2. Open **Query Result**
3. Confirm:

* Cities appear alphabetically
* Within the same city, names appear alphabetically
