# anti-join

An **anti-join** is a query pattern used to find records in one table that have **no matching record** in another table.

## Implementation

The most common way to perform an anti-join is using a `LEFT JOIN` combined with a `WHERE` clause that checks for [NULL](glossary/sql/null) on the joined side.

## Example: Finding customers with no orders

```sql
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```

In this query:
1. We attempt to join every customer to their orders.
2. Customers without orders will have `NULL` in the order columns (like `o.id`).
3. We filter for those `NULL` values to find the "orphans."
