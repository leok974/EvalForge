**SQL Select — Building a Directory (name + city)**

### What we’re practicing

Today’s goal is to learn the *shape* of a basic SQL query:

**SELECT → FROM → ORDER BY**

A database is not a spreadsheet — rows do not have a “natural order.”
If you want sorted output, you must **ask** for it using [ORDER BY](glossary/sql/order-by).

---

### The task in one sentence

Return a directory of users showing:

* `name`
* `city`

…and sort the rows alphabetically by `name`.

---

### Step 1 — Confirm the data source

You will query the `users` table.

**Schema (you don’t need every column):**
`users(id, name, email, age, city, is_active)`

For this quest, you only need **name** and **city**.

---

### Step 2 — Build the query in three parts

1. **[SELECT](glossary/sql/select)** the columns you want
2. **[FROM](glossary/sql/from)** the table they live in
3. **[ORDER BY](glossary/sql/order-by)** the column that defines the sort order

For this quest:

* Columns: `name`, `city`
* Table: `users`
* Sort: `ORDER BY name ASC`

---

### Worked example (concept demo)

Open `example.sql`.
It demonstrates the same query shape (SELECT/FROM/ORDER BY), but it is **not** the quest answer.

**What to notice in the example:**

* Two explicit column names
* A clear `FROM` table
* An `ORDER BY` that controls the row order

---

### Your job

Open `task.sql` and modify the starter query so it matches the quest requirements exactly:

* Columns: `name`, `city` (in that order)
* All rows (no `WHERE`)
* `ORDER BY name ASC`

---

### Common mistakes

* Using `SELECT *` (extra columns fail the shape check)
* Returning columns in the wrong order (`city, name`)
* Forgetting `ORDER BY` (tests may fail due to unordered rows)

---

### How to verify

1. Click **Run**
2. Open **Query Result**
3. Confirm:

* Columns are `name`, then `city`
* Rows are sorted by `name` ascending
