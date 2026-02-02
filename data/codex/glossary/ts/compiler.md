# compiler

## Definition
The TypeScript compiler checks your code for type errors and reports them before runtime. Even when Bun runs TS directly, “type checking” is still the concept: you want errors early.

## Tiny example
If you write:
```ts
let x: number = "oops";
```
the compiler/type-checker should complain.

## Common pitfall
Assuming “it ran” means “it’s typed correctly.” Some runtimes may execute without strict type checks unless configured.

## Related
type annotation
