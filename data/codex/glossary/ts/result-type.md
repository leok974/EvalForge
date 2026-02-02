# Result type

## Definition
A Result type represents success or failure explicitly as a union:
- success: `{ ok: true, value: T }`
- failure: `{ ok: false, error: E }`

## Tiny example
```ts
type Result<T,E> = { ok: true; value: T } | { ok: false; error: E };
```

## Common pitfall
Mixing shapes (sometimes returning `{ value }` without `ok`) makes code fragile. Keep Result variants consistent.

## Related
discriminated union, union type
