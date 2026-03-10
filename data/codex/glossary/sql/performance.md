# performance

In SQL, **performance** refers to how quickly a database can execute a query and return results. 

## Key Factors

- **Scanning vs. Searching**: A "Table Scan" checks every row (slow). Using an [index](glossary/sql/index) allows the database to "Search" (fast).
- **Complexity**: Deeply nested subqueries or joins across huge tables increase processing time.
- **Resources**: CPU, Memory (RAM), and Disk Speed all play a role.

The primary tool for analyzing performance is the [EXPLAIN QUERY PLAN](glossary/sql/explain-query-plan) command.
