---
id: glossary/ts/interface
level: beginner
related:
- codex:glossary/ts/type-alias
- codex:glossary/ts/type-annotation
- codex:glossary/ts/generic
tags:
- types
- objects
- api-design
world: typescript
---

# Interface

## Definition
An **interface** describes the shape of an object (or class) and is commonly used for public APIs and domain models. Interfaces support `extends` and can be merged (declared multiple times) — which can be useful for library augmentation.


## Usage
- Define object shapes for domain models and public APIs.
- Use `extends` to compose interfaces and build type hierarchies.
- Prefer interfaces for object types; use type aliases for unions and primitives.

## Example
```ts
interface User {
  id: string;
  email: string;
}

interface Admin extends User {
  role: "admin";
}
```

## Pitfalls

* Interface merging can be surprising in app code; prefer it for library augmentation.
* Interfaces are structural: extra fields don't necessarily error when assigned from wider types.

## Related

* Type Alias: alternative to interfaces for type definitions.
* Type Annotation: interfaces are commonly used in annotations.
* Generic: interfaces can be generic.