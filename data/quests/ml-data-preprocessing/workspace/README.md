# Data Preprocessing — Impute + One-Hot

Fixture: `fixtures/raw.csv`

Implement `preprocess(df) -> DataFrame`:

- Numeric column `age`: fill missing with median of non-missing
- Categorical column `city`: fill missing with "Unknown"
- One-hot encode `city` into columns `city__<value>` (stable alphabetical order of categories)
- Output columns order must be:
  - age
  - city__Austin
  - city__Chicago
  - city__Detroit
  - city__Unknown
