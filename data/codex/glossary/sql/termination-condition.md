# termination-condition

Recursive systems, like a [recursive CTE](glossary/sql/cte-recursive), must have a **termination condition** to prevent them from running forever (infinite loops).

## SQL Specifics

In SQL, a recursive CTE automatically stops when the recursive member returns **no more rows**.

For example, when walking down an organizational chart, the recursion terminates when it reaches an employee who manages nobody—the "leaf nodes" of the tree.
