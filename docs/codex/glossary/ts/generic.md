---
id: glossary/ts/generic
level: beginner
related:
- codex:glossary/ts/type-parameter
- codex:glossary/ts/type-inference
- codex:glossary/ts/type-alias
tags:
- types
- generics
- api-design
world: typescript
---

# Generic

## Definition
A **generic** is a type parameter that lets you write reusable code while preserving type information. Instead of using `any`, you use `T` (or similar) so TypeScript can infer the type from inputs and keep it consistent across the function.


## Usage
- Write reusable functions that work with multiple types while preserving type safety.
- Avoid `any` by using generic type parameters (`<T>`) that preserve type information.
- Let TypeScript infer the type parameter from arguments when possible.

## Example
```ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const n = first([1, 2, 3]);       // n: number | undefined
const s = first(["a", "b"]);      // s: string | undefined
```

## Pitfalls

* Over-generic APIs can become unreadable. Add constraints when needed.
* If inference fails, callers may have to specify `<T>` manually.

## Related

* Type Parameter: the `T` in a generic is a type parameter.
* Type Inference: TypeScript infers generic types from usage.
* Type Alias: generics work with type aliases too.