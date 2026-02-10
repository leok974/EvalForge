---
id: glossary/ts/type-alias
level: beginner
related:
- codex:glossary/ts/interface
- codex:glossary/ts/union-type
- codex:glossary/ts/generic
tags:
- types
- modeling
world: typescript
---

# Type Alias

## Definition
A **type alias** creates a name for any TypeScript type: primitives, objects, unions, intersections, tuples, and more. It's the most flexible way to model shapes and compose types.


## Usage
- Name complex types for reusability and readability.
- Define union types, object shapes, or function signatures concisely.
- Use with generics to create flexible, composable types.

## Example
```ts
type Id = string;

type User = {
  id: Id;
  email: string;
};

type Status = "idle" | "loading" | "error";
```

## Pitfalls

* Aliases can't be "re-opened" later (interfaces can be merged).
* Very large aliases can hide complexity; consider breaking them up.

## Related

* Interface: alternative way to define object shapes.
* Union Type: type aliases commonly define unions.
* Generic: type aliases can be generic.