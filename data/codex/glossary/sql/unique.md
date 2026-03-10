# unique

**UNIQUE** is a constraint that ensures all values in a column (or a combination of columns) are different. This prevents duplicate data.

## Usage

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE  -- Two users cannot share the same email
);
```

While many rows can contain [NULL](glossary/sql/null) in a `UNIQUE` column (depending on settings), no two rows can contain the same non-null value.
