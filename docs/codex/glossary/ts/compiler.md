---
id: glossary/ts/compiler
world: typescript
level: beginner
tags: [tooling, build, typescript]
related:
  - codex:glossary/ts/type-annotation
  - codex:glossary/ts/interface
  - codex:glossary/ts/union-type
---

# Compiler

## Definition
The TypeScript compiler (`tsc`) converts TypeScript into JavaScript and can also perform **type-checking** without running your code. In most projects it's responsible for enforcing compiler options (like `strict`) and producing build output in a `dist/` folder.

## Usage
- Run `tsc` to compile your project and catch type errors before deploy.
- Use `tsc --noEmit` in CI for type-checking without generating output files.
- Configure behavior via `tsconfig.json` (strict mode, module format, output directory).

## Example
```ts
// index.ts
function greet(name: string) {
  return `Hello, ${name}`;
}
console.log(greet("Leo"));
```

```bash
# type-check + emit JS
npx tsc

# type-check only (no output)
npx tsc --noEmit
```

## Pitfalls

* "It compiles" doesn't mean it's correct at runtime — types don't execute.
* Loose settings hide bugs. Prefer `strict: true` and fix errors early.

## Related

* Type Annotation: how you declare types for the compiler to check.
* Interface: common type definition the compiler validates.
* Union Type: compiler validates all branches are handled.
