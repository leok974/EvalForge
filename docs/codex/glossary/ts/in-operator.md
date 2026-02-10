---
id: glossary/ts/in-operator
level: intermediate
related:
- codex:glossary/ts/type-guard
- codex:glossary/ts/typeof
- codex:glossary/ts/discriminated-union
tags:
- narrowing
- runtime
- types
world: typescript
---

# `in` Operator

## Definition
The `in` operator checks whether an object has a property key. In TypeScript, it can also **narrow** union types when each union member has distinct properties.


## Usage
- Check for property existence in objects at runtime.
- Narrow union types based on distinct properties.
- Combine with nullish checks to safely access object properties.

## Example
```ts
type A = { a: number };
type B = { b: string };
type AorB = A | B;

function f(x: AorB) {
  if ("a" in x) {
    x.a; // number
  } else {
    x.b; // string
  }
}
```

## Pitfalls

* `in` works on objects; guard `null` and primitives first.
* It checks property existence, not type correctness.

## Related

* Type Guard: `in` operator is a type guard.
* Typeof: use for primitive type guards.
* Discriminated Union: `in` can narrow discriminated unions.