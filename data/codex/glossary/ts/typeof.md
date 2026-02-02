# typeof

## Definition
`typeof` is a runtime operator that reports the primitive type of a value (e.g., "string", "number"). In TypeScript, it helps narrow unions.

## Tiny example
```ts
if (typeof x === "number") {
  // x is number here
}
```

## Common pitfall
`typeof null === "object"`. Always check `value !== null` when working with objects.

## Related
type narrowing
