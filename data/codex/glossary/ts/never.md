# never

## Definition
`never` is a type meaning “no possible value.” It’s used for code paths that can’t happen or values that never exist.

## Tiny example
In `Result` helpers:
- `ok<T>(value: T)` can be `Result<T, never>` because success has no error.

## Common pitfall
Confusing `never` with `null` or `undefined`. `never` means the value cannot exist at all.

## Related
Result type
