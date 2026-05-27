## Concept
Until now, you've been reading data with `SELECT`. Now you will mutate it with `UPDATE`.
An `UPDATE` statement modifies existing rows in a table.

## Why It Matters
Data is not static. Prices change, statuses update, and employees get raises. Performing updates safely is critical, because an incorrect `UPDATE` can overwrite an entire column across millions of rows, causing a destructive data loss event.

## Syntax Pattern
```sql
UPDATE table_name
SET column1 = new_value, column2 = another_new_value
WHERE condition;
```

## Example
If we want to move `Alice` to department 2:
```sql
UPDATE employees
SET department_id = 2
WHERE name = 'Alice';
```

## The Golden Rule of Safe Mutating
**Always write your `WHERE` clause first.**

If you execute:
```sql
UPDATE employees
SET salary = 0;
```
Every single employee's salary becomes 0. You have ruined the company.

Before running an `UPDATE`, it is best practice to run a `SELECT` with the exact same `WHERE` clause to preview exactly which rows you are about to modify.

*Note: This Quest IDE uses a sandboxed transaction per run. Even if you mess up, the data is rolled back automatically before your next attempt.*
