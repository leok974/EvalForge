**Quest: Groups & Filters (T2)**

### The Mission
A new inventory audit rule has been established: we need to identify any product category that has grown too large to manage.

Identify all [categories](glossary/sql/group-by) that contain **strictly more than 5** products.

### Requirements
1. **Columns**: Select the `category` and the [count](glossary/sql/count) of products (aliased as `count`).
2. **Mechanism**: Group the results by `category`.
3. **Filter**: Use the [HAVING](glossary/sql/having) clause to restrict results to categories with more than 5 items.
