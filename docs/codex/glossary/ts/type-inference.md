---
id: glossary/ts/type-inference
level: beginner
related:
- codex:glossary/ts/type-annotation
- codex:glossary/ts/generic
- codex:glossary/ts/compiler
tags:
- types
- inference
- compiler
world: typescript
---

# Type Inference

## Definition
**Type Inference** is TypeScript's ability to automatically determine types without explicit annotations. The compiler infers variable types from their initial values, function return types from their bodies, and generic type parameters from arguments.


## Usage
- Let TypeScript figure out types from context (values, return statements, etc.).
- Rely on inference for local variables to reduce annotation noise.
- Add explicit annotations at API boundaries even if inference works.

## Example
```ts
let count = 0;           // inferred as number
let name = "Leo";        // inferred as string

function add(a: number, b: number) {
  return a + b;          // return type inferred as number
}

const items = [1, 2, 3]; // inferred as number[]
```

## Pitfalls

* Inference can be too narrow (literal types) or too wide (`any`) — annotate when needed.
* Complex expressions may infer types you didn't expect; explicit annotations clarify intent.

## Related

* Type Annotation: explicit alternative to inference.
* Generic: TypeScript infers generic type parameters.
* Compiler: the compiler performs all type inference.