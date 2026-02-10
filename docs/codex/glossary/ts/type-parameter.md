---
id: glossary/ts/type-parameter
level: intermediate
related:
- codex:glossary/ts/generic
- codex:glossary/ts/type-inference
- codex:glossary/ts/type-alias
tags:
- types
- generics
- parameters
world: typescript
---

# Type Parameter

## Definition
A **Type Parameter** is a placeholder for a type that will be provided later when using a generic function, class, or type alias. Conventionally named `T`, `U`, `K`, `V`, etc., type parameters let you write code that works with many types while maintaining type safety.


## Usage
- Define generic functions, classes, or types with type parameters like `<T>`.
- Let TypeScript infer type parameters from arguments to reduce verbosity.
- Add constraints (`<T extends SomeType>`) to limit allowed types.

## Example
```ts
function identity<T>(value: T): T {
  return value;
}

identity<number>(42);     // T = number
identity("hello");        // T inferred as string

type Box<T> = { value: T };
const numBox: Box<number> = { value: 10 };
```

## Pitfalls

* Too many type parameters make signatures hard to read; limit to 2-3 when possible.
* Type parameters without constraints are effectively `unknown`; add constraints to improve type safety.

## Related

* Generic: type parameters enable generic programming.
* Type Inference: TypeScript often infers type parameters from arguments.
* Type Alias: type aliases can be generic with type parameters.