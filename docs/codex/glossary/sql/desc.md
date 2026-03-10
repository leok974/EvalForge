---
id: glossary/sql/desc
title: desc
world: sql
---

# desc

`DESC` (short for "Descending") is a keyword used in the `ORDER BY` clause to sort data from highest to lowest (e.g., Z to A, or 100 to 1).

## Usage

```sql
-- See most recent events first
SELECT * FROM events ORDER BY event_date DESC;

-- See highest salaries first
SELECT * FROM employees ORDER BY salary DESC;
```

`DESC` is the opposite of [ASC](glossary/sql/asc).