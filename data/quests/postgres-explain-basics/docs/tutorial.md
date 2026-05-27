# Understanding EXPLAIN in PostgreSQL

`EXPLAIN` shows the execution plan PostgreSQL will use for a query without actually running it. This is the first tool to reach for when diagnosing slow queries.

## Basic usage

```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 42;
```

Output example:
```
Seq Scan on orders  (cost=0.00..45.00 rows=1 width=72)
  Filter: (customer_id = 42)
```

## Key plan nodes

- **Seq Scan** — full table scan; every row is read. Slow on large tables.
- **Index Scan** — uses an index to locate matching rows directly. Fast.
- **Bitmap Heap Scan** — uses an index to build a bitmap of page locations, then reads those pages. Good for moderate selectivity.

## EXPLAIN ANALYZE

`EXPLAIN ANALYZE` actually executes the query and shows real timings:

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42;
```

Use ANALYZE to see the difference between estimated and actual row counts.

## When to use EXPLAIN

- Before adding an index: confirm the query is doing a Seq Scan
- After adding an index: verify the planner picks it up
- When a query is slower than expected: check for wrong estimates or bad join order

## cost=X..Y

The `cost` is in arbitrary planner units. `X` is startup cost, `Y` is total cost. Lower is better, but what matters more is whether the plan is an Index Scan or Seq Scan.
