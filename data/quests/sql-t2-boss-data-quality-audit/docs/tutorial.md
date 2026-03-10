# Tutorial: BOSS - Data Quality Audit (Anti-Joins)

Welcome to the final BOSS quest of Tier 2. In this challenge, you will perform a **Data Quality Audit** to find broken relationships in your tables.

## Foreign Key Integrity

A **Foreign Key** is a column that points to an ID in another table (or the same table). In a healthy database, every foreign key should point to an existing record.

- **Orphaned Record**: A row that has a foreign key pointing to an ID that **does not exist**.
- **Data Quality Audit**: The process of finding and fixing these orphans.

## The Anti-Join Pattern

To find orphans, you use a **LEFT JOIN** and look for rows where the right side is [NULL](glossary/sql/null). This is often called an "Anti-Join."

```sql
SELECT e.name, e.manager_id
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id
WHERE e.manager_id IS NOT NULL  -- They have a manager field filled...
  AND m.id IS NULL;            -- ...but that manager doesn't exist in the table.
```

## Why this happens

In high-concurrency systems, records might be deleted out of order, or manual data entry might bypass safety checks. Auditing for these broken links is a critical task for any senior SQL technician.

In this BOSS quest, you will intentionally create a "Ghost Employee" with a non-existent manager and then write a query to detect this data quality issue.
