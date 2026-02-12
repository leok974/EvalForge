# Tutorial — TS Control

## What You’re Practicing
- Using `unknown` safely
- Narrowing with runtime checks
- Writing clean, readable control flow

## Implementation Plan
1. Check type: `typeof code === "number"`.
2. Check integer: `Number.isInteger(code)`.
3. Check range: `code >= 100 && code <= 599`.
4. Use numeric ranges to return the correct label.

## Pitfalls
- Accepting `"200"` (string) by accident
- Accepting floats like `200.5`
- Forgetting the range gate (100–599)
