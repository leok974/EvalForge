# avg

`AVG()` is an aggregate function that returns the average value of a numeric column.

## Usage

```sql
-- Find the average price of all products
SELECT AVG(price) FROM products;

-- Find average salary per department
SELECT department, AVG(salary) 
FROM employees 
GROUP BY department;
```

`AVG()` ignores [NULL](glossary/sql/null) values.
