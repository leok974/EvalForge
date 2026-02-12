# Tutorial — TS Generics

## What You’re Practicing
- Generic type parameters (`<T, K>`)
- Key constraints (`K extends keyof T`)
- Returning `Pick<T, K>`

## Implementation Plan
1. Create an output object typed as `Pick<T, K>`.
2. Loop through `keys`.
3. Assign `out[k] = obj[k]`.
4. Return the output.

## Pitfalls
- Forgetting `K extends keyof T` (you lose safe indexing)
- Mutating `obj` instead of creating a new object
- Returning `{}` without the right type
