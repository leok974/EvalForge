---
id: glossary/ts/typeof
level: beginner
related:
- codex:glossary/ts/type-guard
- codex:glossary/ts/type-narrowing
- codex:glossary/ts/in-operator
tags:
- narrowing
- runtime
- types
world: typescript
---

# `typeof`

## Definition
The `typeof` operator checks the JavaScript runtime type of a value. In TypeScript, it acts as a **type guard** that narrows union types to specific primitive types like `string`, `number`, `boolean`, `undefined`, `object`, or `function`.


## Usage
- Check primitive types at runtime (`string`, `number`, `boolean`, etc.).
- Use as a type guard to narrow unions in conditionals.
- Remember `typeof null === 'object'` — guard against null explicitly.

## Example
```ts
function double(value: string | number) {
  if (typeof value === "number") {
    // value: number
    return value * 2;
  }
  // value: string
  return value + value;
}

double(21);       // 42
double("hello");  // "hellohello"
```

## Pitfalls

* `typeof null` returns `"object"` — a JavaScript quirk you must account for.
* `typeof` only distinguishes primitive types; use `instanceof` or custom guards for objects.

## Related

* Type Guard: `typeof` is a built-in type guard.
* Type Narrowing: `typeof` enables control-flow-based narrowing.
* In Operator: use for object property checks.