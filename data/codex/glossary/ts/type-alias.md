# type alias

## Definition
A type alias gives a name to a type. It’s commonly used for unions or reusable type definitions.

## Tiny example
```ts
type Id = string | number;
```

## Common pitfall
Types help at compile time, not runtime. A `type` won’t convert or validate values when your program runs.

## Related
union type, compiler
