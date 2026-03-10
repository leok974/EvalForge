# hierarchy

In database terms, a **hierarchy** is a way of organizing data where items are ranked one above another, forming a tree-like structure. Examples include organizational charts (Manager -> Employee) or file systems (Folder -> Subfolder).

## Implementation

Hierarchies are typically stored using a "Parent-Child" relationship:

```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT,
    parent_id INTEGER  -- References another category's id
);
```

To query an entire branch of a hierarchy, a [recursive CTE](glossary/sql/cte-recursive) is often used.
