# Tutorial: Correlated Subqueries & EXISTS

A **correlated [subquery](glossary/sql/subquery)** is a query that depends on the "outer" query for its values. It executes once for every [row](glossary/sql/row) processed by the main query.

## The EXISTS Operator

The `EXISTS` operator is used to test for the existence of any record in a subquery. It returns `TRUE` if the subquery returns one or more records.

```sql
SELECT name
FROM employees e1
WHERE EXISTS (
  SELECT 1 
  FROM employees e2 
  WHERE e2.manager_id = e1.id
);
```

### How it works mentally:
1. SQL looks at the first employee (`e1.id = 1`).
2. It runs the subquery: "Are there any employees whose `manager_id` is 1?"
3. If yes, the employee is included in the final result.
4. Move to the next employee and repeat.

## Performance Advantage

`EXISTS` is often faster than a `JOIN` or `IN` when you only care *if* a match exists, but don't actually need to retrieve data from the second table. As soon as the database finds a single match in the subquery, it can stop looking and return `TRUE`.

In this quest, you will use `EXISTS` to identify managers—employees who have at least one person reporting to them.
