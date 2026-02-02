# type parameter

## Definition
A type parameter is a placeholder type name (like `T` or `E`) used in generics.

## Tiny example
```ts
type Box<T> = { value: T };
```

## Common pitfall
Confusing a type parameter with a runtime value. Type parameters exist at compile time only.

## Related
generic
