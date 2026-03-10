# Tutorial: Groups & Filters (GROUP BY + HAVING)

In your earlier studies, you learned how to use `GROUP BY` to summarize data into categories. But how do you filter those results *after* they've been summarized?

## The Difference Between WHERE and HAVING

- **WHERE**: Filters individual [rows](glossary/sql/row) *before* they are grouped.
- **HAVING**: Filters [groups](glossary/sql/group-by) *after* they have been calculated.

Think of it like this: If you want to find "all fruits that cost more than $1.00," you use `WHERE` because you are looking at items. If you want to find "all categories that have more than 5 items," you must use `HAVING` because you can't count the items until you've grouped them.

## The Standard Pipeline

The order of clauses is critical in SQL:

1. **SELECT**: Columns and Aggregates
2. **FROM**: Tables
3. **WHERE**: Row-level filtering (pre-grouping)
4. **GROUP BY**: Categorization
5. **HAVING**: Group-level filtering (post-grouping)

## Example

```sql
-- Find categories with a total value of over $1000
SELECT category, SUM(price) as total_value
FROM products
GROUP BY category
HAVING SUM(price) > 1000;
```

In this quest, you will identify high-volume product categories by filtering for those with a high item count.
