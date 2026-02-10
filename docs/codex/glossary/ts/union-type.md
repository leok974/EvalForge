---
id: glossary/ts/union-type
level: beginner
related:
- codex:glossary/ts/type-guard
- codex:glossary/ts/type-narrowing
- codex:glossary/ts/discriminated-union
tags:
- types
- safety
world: typescript
---

# Union Type

## Definition
**Union Types** allow a value to be one of several types. Use `|` to combine types. This is essential for functions that accept multiple input types or return different types based on conditions.


## Usage
- Model values that can be one of several types (e.g., `string | number`).
- Narrow unions with type guards before accessing type-specific properties.
- Keep unions focused; overly broad unions reduce type safety.

## Example
```ts
function format(value: string | number): string {
  if (typeof value === "number") {
    return value.toFixed(2);
  }
  return value.toUpperCase();
}

format(42);      // "42.00"
format("hello"); // "HELLO"
```

## Pitfalls

* Accessing properties without narrowing causes errors; use type guards to safely access type-specific members.
* Overly broad unions (e.g., `string | number | boolean | null | undefined`) reduce type safety; keep unions focused.

## Related

* Type Guard: narrow unions to specific types at runtime.
* Type Narrowing: the process of refining union types.
* Discriminated Union: a special pattern for unions with a common field.