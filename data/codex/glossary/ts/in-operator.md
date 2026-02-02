# in operator

## Definition
`"prop" in obj` checks whether an object has a property. It’s often used to narrow object unions safely.

## Tiny example
```ts
if ("email" in x) {
  // x likely has email here
}
```

## Common pitfall
`in` only works on non-null objects. Check `typeof x === "object" && x !== null` first.

## Related
type guard, type narrowing
