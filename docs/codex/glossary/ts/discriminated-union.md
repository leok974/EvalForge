---
id: glossary/ts/discriminated-union
level: intermediate
related:
- codex:glossary/ts/union-type
- codex:glossary/ts/type-guard
- codex:glossary/ts/never
tags:
- types
- unions
- narrowing
world: typescript
---

# Discriminated Union

## Definition
A **discriminated union** is a union of object types that share a common literal field (the "discriminant"), like `kind: "ok" | "err"`. TypeScript can use that field to safely **narrow** the type in conditionals.


## Usage
- Model states or variants with a shared discriminant field (like `kind` or `type`).
- Use `switch` or `if` statements on the discriminant to narrow types safely.
- Ensure exhaustiveness checks with `never` to catch missing cases.

## Example
```ts
type Ok = { kind: "ok"; value: number };
type Err = { kind: "err"; message: string };
type Result = Ok | Err;

function print(r: Result) {
  if (r.kind === "ok") {
    console.log(r.value);
  } else {
    console.error(r.message);
  }
}
```

## Pitfalls

* The discriminant must be a **literal** type (not `string`).
* Don't mix unrelated shapes without a clear discriminant — narrowing gets messy.

## Related

* Union Type: discriminated unions are a special case of unions.
* Type Guard: the discriminant acts as a type guard.
* Never: used for exhaustiveness checking with discriminated unions.