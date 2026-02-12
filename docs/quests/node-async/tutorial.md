# Tutorial — node-async

## What You’re Practicing
- `async/await` control flow
- handling thrown errors in awaited calls
- preventing crashes / unhandled rejections

## Implementation Plan
1. Call `await loadUser(id)` inside `getUserName`.
2. Return `user.name` on success.
3. Wrap the await in `try/catch`.
4. In the catch block, return `"Guest"`.

## Pitfalls
- forgetting `await` (you’ll return a Promise instead of a string)
- catching but not returning `"Guest"`
- letting the error escape and failing the test
