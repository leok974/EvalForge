# Tutorial — node-testing

## What You’re Practicing
- `node:test` for defining test cases
- `node:assert/strict` for real checks that fail loudly

## Implementation Plan
1) In the add test:
   - call `add(2, 3)`
   - assert the result equals `5`

2) In the subtract test:
   - call `subtract(5, 2)`
   - assert the result equals `3`

## Pitfalls
- forgetting to call the function (asserting on the function itself)
- using loose equality when strict is expected
