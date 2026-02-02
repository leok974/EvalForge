# discriminated union

## Definition
A discriminated union is a union where each variant has a shared field (like `kind`) with different literal values. This makes narrowing reliable.

## Tiny example
```ts
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "square"; s: number };

function area(x: Shape) {
  if (x.kind === "circle") return Math.PI * x.r * x.r;
  return x.s * x.s;
}
```

## Common pitfall
Using optional fields instead of a discriminant leads to ambiguous narrowing.

## Related
type narrowing, union type
