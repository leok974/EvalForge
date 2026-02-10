---
id: glossary/ts/type-narrowing
level: beginner
related:
- codex:glossary/ts/type-guard
- codex:glossary/ts/union-type
- codex:glossary/ts/typeof
tags:
- types
- narrowing
- control-flow
world: typescript
---

# Type Narrowing

## Definition
**Type Narrowing** is TypeScript's ability to refine types within conditional branches based on runtime checks. When you check a value's type with `typeof`, `instanceof`, or property tests, TypeScript understands the more specific type in that branch.


## Usage
- Refine types within conditional blocks using runtime checks.
- Use `typeof`, `instanceof`, or custom guards to tell TypeScript about narrowed types.
- Understand that type narrowing is scoped to the block where the check occurs.

## Example
```ts
function process(value: string | number | null) {
  if (value === null) {
    // value: null
    return "empty";
  }
  if (typeof value === "string") {
    // value: string
    return value.toUpperCase();
  }
  // value: number
  return value.toFixed(2);
}
```

## Pitfalls

* Narrowing only works within the scope where the check occurs; reassignment can widen types again.
* Complex control flow can confuse narrowing; keep checks simple and close to usage.

## Related

* Type Guard: explicit functions that perform narrowing.
* Union Type: narrowing is essential for working with unions.
* Typeof: built-in narrowing for primitive types.