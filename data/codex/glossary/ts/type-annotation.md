# type annotation

## Definition
A type annotation attaches a type to a variable, parameter, or return value (e.g., `name: string`).

## Tiny example
```ts
function shout(msg: string): string {
  return msg.toUpperCase();
}
```

## Common pitfall
Using `String` instead of `string`. Prefer primitives: `string`, `number`, `boolean`.

## Related
interface, type alias
