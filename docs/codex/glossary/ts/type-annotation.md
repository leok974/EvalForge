---
id: glossary/ts/type-annotation
level: beginner
related:
- codex:glossary/ts/type-inference
- codex:glossary/ts/type-alias
- codex:glossary/ts/interface
tags:
- types
- syntax
world: typescript
---

# Type Annotation

## Definition
A **type annotation** explicitly tells TypeScript the type of a variable, parameter, or return value. Often TypeScript can infer types automatically, but annotations are useful at API boundaries and for readability.


## Usage
- Explicitly declare types at API boundaries (parameters, return values).
- Use when inference is unclear or when you want to enforce a specific type.
- Add to variables when the initial value doesn't reveal the intended type.

## Example
```ts
let count: number = 0;

function add(a: number, b: number): number {
  return a + b;
}

const user: { id: string; email: string } = { id: "1", email: "a@b.com" };
```

## Pitfalls

* Over-annotating can add noise; rely on inference when obvious.
* Incorrect annotations can force bad assumptions and hide real issues.

## Related

* Type Inference: TypeScript often infers types without annotations.
* Type Alias: annotations commonly use type aliases.
* Interface: interfaces are used in annotations.