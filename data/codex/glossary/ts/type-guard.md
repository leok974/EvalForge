# type guard

## Definition
A type guard is a function that returns a predicate like `value is X`. If it returns true, TypeScript treats the value as type X.

## Tiny example
```ts
function isString(v: unknown): v is string {
  return typeof v === "string";
}
```

## Common pitfall
Using `as X` instead of writing checks. `as` can hide real bugs.

## Related
type narrowing
