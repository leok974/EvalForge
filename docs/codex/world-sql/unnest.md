# PostgreSQL: UNNEST

In PostgreSQL, `UNNEST` takes an array and expands it into a set of rows.

### Why use UNNEST?
- **Flattening Data**: When you have an array column (like `skills TEXT[]`) and want to analyze or filter each item individually.
- **Joining on Arrays**: You can unnest an array and join the resulting rows against another table.

### Syntax
```sql
UNNEST(array_column)
```

### Example

Given a table `employees` with a `skills` array:
| name | skills |
|---|---|
| Alice | {Python, SQL} |

You can unnest it to get one row per skill:
```sql
SELECT name, UNNEST(skills) AS skill
FROM employees;
```

**Result:**
| name | skill |
|---|---|
| Alice | Python |
| Alice | SQL |

### Common Mistake
Forgetting that `UNNEST` in the `SELECT` list produces multiple rows for the surrounding columns. It multiplies the output rows based on the length of the array.
