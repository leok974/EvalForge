# union type

## Definition
A union type means “one of these types,” written with `|` (e.g., `string | number`).

## Tiny example
```ts
type Id = string | number;
```

## Common pitfall
When using unions, you often need runtime narrowing:

```ts
if (typeof id === "string") { ... }
```

## Related
type alias
