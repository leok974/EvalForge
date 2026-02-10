---
id: glossary/ts/type-guard
level: intermediate
related:
- codex:glossary/ts/discriminated-union
- codex:glossary/ts/typeof
- codex:glossary/ts/in-operator
tags:
- types
- narrowing
- runtime
world: typescript
---

# Type Guard

## Definition
A **type guard** is a runtime check that tells TypeScript how to narrow a value's type. Built-in guards include `typeof`, `instanceof`, and property checks. You can also write a custom guard using a predicate return type: `value is SomeType`.


## Usage
- Create custom runtime checks that TypeScript recognizes for narrowing.
- Use `value is Type` predicates to tell TypeScript about the refined type.
- Combine with `typeof`, `instanceof`, or property checks for validation.

## Example
```ts
type User = { id: string; email: string };

function isUser(x: unknown): x is User {
  return typeof x === "object" && x !== null
    && "id" in x && "email" in x;
}

function handle(x: unknown) {
  if (isUser(x)) {
    x.email.toLowerCase(); // safe
  }
}
```

## Pitfalls

* A guard must be **correct at runtime**. TypeScript trusts your predicate.
* Property checks on `unknown` require narrowing (`typeof x === "object" && x !== null`).

## Related

* Discriminated Union: discriminants are implicit type guards.
* Typeof: built-in type guard for primitives.
* In Operator: checks property existence for narrowing.