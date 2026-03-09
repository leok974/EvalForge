# Briefing: Top 3 Inventory

The archive is too large to inspect all at once, so Mission Control wants a short ranked report.

Find the active products, sort them from most expensive to least expensive, and return only the first 3 rows.
Use `name ASC` as the tie-breaker so the result stays stable and readable.

## Requirements:
1.  **Return**: `id`, `name`, `category`, `price_cents`
2.  **Filter**: Only include products that are not discontinued (`is_discontinued = FALSE`)
3.  **Sort**: by `price_cents` descending, then `name` ascending
4.  **Count**: Return exactly **3** rows
