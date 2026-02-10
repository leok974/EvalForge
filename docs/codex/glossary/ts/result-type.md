---
id: glossary/ts/result-type
level: intermediate
related:
- codex:glossary/ts/discriminated-union
- codex:glossary/ts/type-guard
- codex:glossary/ts/generic
tags:
- patterns
- errors
- unions
world: typescript
---

# Result Type

## Definition
A **Result type** is a pattern for representing success or failure as a value instead of throwing exceptions. In TypeScript it's typically modeled as a discriminated union like `{ ok: true, value } | { ok: false, error }`.


## Usage
- Replace exceptions with explicit success/failure values for error handling.
- Use discriminated unions (`ok: true | false`) to model outcomes.
- Force callers to handle errors explicitly instead of relying on try/catch.

## Example
```ts
type Ok<T> = { ok: true; value: T };
type Err<E> = { ok: false; error: E };
type Result<T, E> = Ok<T> | Err<E>;

function parseIntSafe(s: string): Result<number, string> {
  const n = Number(s);
  return Number.isFinite(n) ? { ok: true, value: n } : { ok: false, error: "NaN" };
}

const r = parseIntSafe("42");
if (r.ok) console.log(r.value);
else console.error(r.error);
```

## Pitfalls

* Don't mix thrown exceptions and Result returns for the same API.
* Keep the discriminant consistent (`ok` or `kind`) to preserve narrowing.

## Related

* Discriminated Union: Result is a discriminated union.
* Type Guard: discriminant acts as a type guard.
* Generic: Result types are typically generic.