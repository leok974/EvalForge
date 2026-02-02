# generic

## Definition
A generic is a reusable type or function that works with multiple types using placeholders like `<T>`.

## Tiny example
```ts
function first<T>(items: T[]): T {
  return items[0];
}
```

## Common pitfall
Overusing generics can reduce readability. Use them when they remove duplication and preserve type safety.

## Related
type parameter, type inference
