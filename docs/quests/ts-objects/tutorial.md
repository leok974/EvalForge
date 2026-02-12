# Tutorial — TS Objects

## What You’re Practicing
- Narrowing `unknown` to a plain object safely
- Applying defaults without losing type safety
- Normalizing nested objects (headers)

## Implementation Plan
1. If input isn’t a plain object, treat it as `{}`.
2. Start with defaults.
3. For each field:
   - validate its type
   - apply clamping/trim rules
4. For headers:
   - ensure it’s a plain object
   - only accept string values
   - lowercase keys + trim values
   - drop empty keys/values

## Pitfalls
- Treating arrays as plain objects
- Forgetting to use numeric comparator/clamp
- Allowing whitespace-only strings through
