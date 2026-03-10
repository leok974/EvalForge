# min

`MIN()` is an aggregate function that returns the smallest value of the selected column.

## Usage

```sql
-- Find the cheapest product
SELECT MIN(price) FROM products;
```

`MIN()` works on numbers, strings (A is smaller than Z), and dates (the oldest date is the smallest).
