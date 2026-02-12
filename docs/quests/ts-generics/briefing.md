# Briefing — TS Generics

## Objective
Write a type-safe `pick()` helper that selects keys from an object.

## Contract
- Signature: `pick<T, K extends keyof T>(obj: T, keys: readonly K[]): Pick<T, K>`
- Returns a new object containing only the requested keys
- Does not mutate the original object
- Preserves insertion order based on `keys`

## Success Criteria
Public tests pass with no extra output.
