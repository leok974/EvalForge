## Outcome
By the end of this quest you will:
- Define a generic **Result<T, E>** type for safe error handling
- Create `ok(...)` and `err(...)` helper functions
- Implement `mapResult(...)` to transform successful values without losing error types
- Understand what a **type parameter** is and why generics reduce duplication

## Concept in 30 seconds
Throwing errors can be messy. A `Result<T, E>` makes success/failure explicit:

- Success: `{ ok: true, value: T }`
- Failure: `{ ok: false, error: E }`

Generics (`<T, E>`) let you reuse the same pattern for different value types (numbers, strings, objects) without rewriting everything.

**Mental model:**  
Result is a typed “either”:
- either a value (T)
- or an error (E)

## Key terms
- **generic** — reusable type/function parameterized by types
- **type parameter** — the `T` and `E` in `Result<T, E>`
- **Result type** — explicit success/failure container
- **type inference** — TypeScript figures out types from usage
- **never** — a type meaning “this can’t happen” (useful for helpers)

## Walkthrough
1) Open `main.ts`.
2) Implement `Result<T, E>` as a discriminated union.
3) Implement helpers:
   - `ok(value)` returns a success Result
   - `err(error)` returns a failure Result
4) Implement `parseIntStrict(input)`:
   - Trim input
   - Parse base 10 integer
   - Return `ok(n)` or `err("invalid integer")`
5) Implement `mapResult(res, fn)`:
   - If res is ok, apply fn to value and return ok(newValue)
   - If res is err, return the same error
6) Run and confirm demo output.
7) Submit when tests pass.

## Example implementation
```ts
export type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export function ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

export function err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

export function parseIntStrict(input: string): Result<number, string> {
  const trimmed = input.trim();
  const n = Number.parseInt(trimmed, 10);
  return Number.isNaN(n) ? err("invalid integer") : ok(n);
}

export function mapResult<T, U, E>(
  res: Result<T, E>,
  fn: (value: T) => U
): Result<U, E> {
  return res.ok ? ok(fn(res.value)) : res;
}
```

## Common mistakes

* **Returning mixed shapes**

  * Result variants must be consistent: ok has `value`, err has `error`.
* **Forgetting base 10 parsing**

  * Always pass `10` to `parseInt` unless you intentionally want different bases.
* **Throwing instead of returning Result**

  * This quest is about explicit success/failure values, not exceptions.
* **Losing the error type in mapResult**

  * `mapResult` should preserve the original `E`.

## Check yourself

1. Why is `Result<T, E>` safer than returning `null`?
2. What do `T` and `E` represent?
3. What should `mapResult` do when `res.ok` is false?
