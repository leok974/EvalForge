# Tutorial — TS Types

## What You’re Practicing
- Modeling data with unions + object types
- Narrowing `unknown` values safely
- Using a type guard (`value is User`) to enforce contracts

## Implementation Plan
1. In `isUser`:
   - Check value is an object (and not null).
   - Validate `id` is a number and `name` is a string.
   - Validate `role` is exactly one of the allowed strings.
2. In `parseUser`:
   - Try `JSON.parse`.
   - Call `isUser` on the parsed value.
   - If valid return it; otherwise throw `Error("EF_TS_TYPES_INVALID")`.

## Pitfalls
- Treating `typeof value === "object"` as enough (null is an object!)
- Forgetting to validate `role`
- Throwing a different error message (tests require exact text)
