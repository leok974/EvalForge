# Tutorial — Data Forge

## What You’ll Learn
- Reading and writing JSON in Python
- String manipulation and type coercion
- List processing and sorting
- Constructing a deterministic data pipeline

## Approach
1. **Load Data**: Use `json.load()` to read the fixture file.
2. **Normalize Function**: Create a helper function `normalize_record(record)` that takes a raw dict and returns a clean one.
   - Handle missing keys using `.get()`.
   - Use `strip()`, `lower()`, `title()` for strings.
   - Use `try/except` or `int()` checks to coerce IDs.
3. **Process Loop**: Iterate through the raw data, normalize each item, and collect them in a new list.
4. **Sort**: Use `normalized_list.sort(key=lambda x: x['id'])` to ensure deterministic order.
5. **Output**: Use `json.dumps()` to print the final result.

## Pitfalls
- **Keys**: The output keys (`is_active` vs `active`) must match the spec exactly.
- **Nulls**: Ensure empty strings become Python `None` (which dumps as `null`), not `"null"` string.
- **Tags**: Handling "tags" that might be a CSV string OR a list requires an `isinstance` check.
