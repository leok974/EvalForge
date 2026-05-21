## Hint 1
Use `const` for values that never change. The grader checks your source code for the
`const` keyword — a variable declared with `let` or `var` will fail that objective.

## Hint 2
When to use each:
- `const` — values you won't reassign (preferred for most bindings)
- `let` — values you need to reassign (counters, accumulators)
- `var` — avoid in modern JS; function-scoped and hoisted in surprising ways
