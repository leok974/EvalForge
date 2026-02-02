# interface

## Definition
An interface describes the required shape of an object: which properties exist and their types.

## Tiny example
```ts
interface User { name: string; }
const u: User = { name: "Ada" };
```

## Common pitfall
Interfaces don’t create runtime validation. If you need runtime checks, you must write code to check values.

## Related
type alias
