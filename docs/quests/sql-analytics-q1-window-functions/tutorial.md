## Outcome
You will learn how SQL window functions compute values across related rows without collapsing your result set, enabling rankings and running totals.

## Concept in 30 seconds
A window function is like doing an aggregate calculation (rank, sum, avg) but keeping every row. The “window” is defined by `OVER (...)`. Use `PARTITION BY` to group rows (like per user), and `ORDER BY` to define the row order for rankings or running calculations.

## Key terms
- **Window Function**: A function that computes over a window of rows while keeping each row.
- **OVER**: The clause that defines the window.
- **PARTITION BY**: Splits rows into groups for separate windows.
- **ORDER BY**: Defines row order inside each partition.
- **ROW_NUMBER**: Assigns a unique rank order per partition.

## Walkthrough
1) Start with a base query selecting the columns you need.
2) Add a window function with `OVER (PARTITION BY ... ORDER BY ...)`.
3) Verify that your query still returns one row per original record.
4) Use **Run** to inspect results and confirm ranks/totals match expectations.
5) Use **Submit** when the computed window columns match the quest’s required output.

## Example implementation
Ranking purchases per customer by most recent date:

```sql
SELECT
  customer_id,
  order_id,
  order_date,
  amount,
  ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY order_date DESC
  ) AS rn
FROM orders
ORDER BY customer_id, rn;
```

A running total per customer:

```sql
SELECT
  customer_id,
  order_id,
  order_date,
  amount,
  SUM(amount) OVER (
    PARTITION BY customer_id
    ORDER BY order_date
  ) AS running_total
FROM orders
ORDER BY customer_id, order_date;
```

## Common mistakes
- **Forgetting `OVER (...)`** (window functions require it).
- **Using window functions when you meant `GROUP BY`** (GROUP BY collapses rows).
- **Missing `ORDER BY`** when you need rankings or running totals.
- **Partitioning incorrectly** (ranking across all rows instead of per group).
- **Confusing `ROW_NUMBER` with `RANK`** (ties behave differently).

## Check yourself
- What does a window function let you do that GROUP BY does not?
- What does PARTITION BY change?
- Why is ORDER BY important for running totals?
