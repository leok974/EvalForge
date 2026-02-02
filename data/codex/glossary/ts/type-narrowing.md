# type narrowing

## Definition
Type narrowing is turning a union type (like `string | number`) into a specific type by using runtime checks.

## Tiny example
```ts
function f(x: string | number) {
  if (typeof x === "string") return x.toUpperCase();
  return x.toFixed(2);
}
```

## Common pitfall
Assuming a type without checking. Narrow with `typeof`, `in`, or a discriminant field.

## Related
type guard, discriminated union
