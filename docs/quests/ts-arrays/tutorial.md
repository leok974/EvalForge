# Tutorial — TS Arrays

## What You’re Practicing
- Narrowing `unknown` into an array you can process
- Filtering invalid data (NaN, Infinity, out-of-range)
- Deterministic transforms (round + unique + sort)

## Implementation Plan
1. If `!Array.isArray(input)`, return [].
2. Filter elements to numbers:
   - `typeof x === "number"`
   - `Number.isFinite(x)`
3. Round with `Math.round`.
4. Filter to 0..100 inclusive.
5. Deduplicate (use a Set).
6. Sort ascending with `(a, b) => a - b`.

## Pitfalls
- `typeof NaN === "number"` (still invalid) → must use `Number.isFinite`
- Default `.sort()` sorts as strings → must provide numeric comparator
- Forgetting to dedupe after rounding (100.4 and 99.6 both become 100)
