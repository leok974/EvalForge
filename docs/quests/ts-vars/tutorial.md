# Tutorial — TS Vars

## What You’ll Learn
- Why `const` is the default in TypeScript
- How type annotations prevent “shape drift”
- Literal types: enforcing exact values

## Approach
1. Export `greeting` as a constant string.
2. Define a `Config` type with literal values.
3. Export `config` that matches `Config` exactly.

## Pitfalls
- Using `string` instead of the exact literal in the type
- Returning numbers that don’t match (e.g., 300 instead of 250)
- Misspelling config keys
