---
id: glossary/sql/count
level: beginner
tags:
- fundamentals
- aggregates
title: COUNT
world: sql
---

The `COUNT()` function returns the number of rows that matches a specified criterion.

## Variations

- **COUNT(*)**: Returns the total number of rows in the table.
- **COUNT(col)**: Returns the number of non-null values in a specific column.
- **COUNT(DISTINCT col)**: Returns the number of unique non-null values.

## Usage

```sql
-- Count active users
SELECT COUNT(*) FROM users WHERE is_active = 1;

-- Count unique zip codes
SELECT COUNT(DISTINCT zip_code) FROM users;
```