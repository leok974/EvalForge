# Hints: The Art of Change

## Hint 1 — Concept
Use [INSERT](glossary/sql/insert), [UPDATE](glossary/sql/update), and [DELETE](glossary/sql/delete) in sequence. Remember to separate your statements with semicolons (`;`).

## Hint 2 — Precision
When updating or deleting, always use a [WHERE](glossary/sql/where) clause to target specific records. Filtering by `id` is the safest way to ensure precision.

## Hint 3 — The Answer
Your query should look something like this:
```sql
INSERT INTO users (id, name, email, age, city, is_active)
VALUES (7, 'Grace', 'grace@example.com', 30, 'Berlin', 1);

UPDATE users SET city = 'London' WHERE id = 2;

DELETE FROM orders WHERE id = 4;

SELECT * FROM users;
```
This performs all three mutations and then displays the updated user list.
