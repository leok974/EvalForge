# Tutorial — Internal Tooling & DX

## Approach
You have a tool router already. Your job is to implement the core helpers cleanly.

## Steps
1. Implement `slugify(text)` exactly per rules.
2. Implement `unique_sorted(items)`:
   - trim, lowercase, drop empty
   - unique + sorted
3. Run the quest and confirm the JSON output matches expected.

## Pitfalls
- Forgetting to collapse whitespace before replacing with "-"
- Leaving punctuation in the slug
- Not stripping leading/trailing "-"
- Not sorting after dedup
