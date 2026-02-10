---
id: glossary/ts/never
level: intermediate
related:
- codex:glossary/ts/discriminated-union
- codex:glossary/ts/union-type
- codex:glossary/ts/type-guard
tags:
- types
- narrowing
- exhaustiveness
world: typescript
---

# `never`

## Definition
`never` represents values that **cannot happen**. It appears when TypeScript can prove a code path is unreachable, and it's commonly used to enforce **exhaustive** handling of discriminated unions.


## Usage
- Use in `switch` exhaustiveness checks to catch unhandled cases.
- Appears naturally when all possibilities are eliminated in control flow.
- Signals to TypeScript (and future readers) that a code path is unreachable.

## Example
```ts
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "square"; s: number };

function area(x: Shape) {
  switch (x.kind) {
    case "circle": return Math.PI * x.r * x.r;
    case "square": return x.s * x.s;
    default: {
      const _exhaustive: never = x;
      return _exhaustive;
    }
  }
}
```

## Pitfalls

* If the union isn't discriminated well, `never` won't help.
* Don't use `never` as a "generic error type" — it has a specific meaning.

## Related

* Discriminated Union: `never` enforces exhaustive checks.
* Union Type: `never` appears in union narrowing.
* Type Guard: guards narrow types, sometimes to `never`.