# table

A **table** is a collection of related data held in a structured format within a database. It consists of vertical **columns** (identified by their name) and horizontal **rows** (each representing a single data record).

## Structure

- **Columns**: Define the data type and properties of the data (e.g., `id` as an INTEGER PRIMARY KEY).
- **Rows**: Contain the actual data points for each column.
- **Schema**: The blueprint of the table, defining its columns, types, and constraints.

## Basic Query

To see all the data in a table, you use the [SELECT](glossary/sql/select) and [FROM](glossary/sql/from) clauses:

```sql
SELECT * FROM users;
```
