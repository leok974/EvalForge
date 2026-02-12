# Tutorial — TS Functions

## What You’re Practicing
- Writing a clear function signature
- Validating `unknown` without crashing
- Keeping logic pure and testable

## Implementation Plan
1. Guard: if input is not an array, return 0.
2. Implement `isValidLineItem`:
   - confirm object shape
   - validate types and bounds
3. Loop through items:
   - if valid, add `priceCents * qty`
4. Return the final sum.

## Pitfalls
- Accepting floats as integers (use `Number.isInteger`)
- Forgetting to trim sku
- Throwing errors instead of ignoring invalid items
