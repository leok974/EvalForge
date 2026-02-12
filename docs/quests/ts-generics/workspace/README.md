# TS Generics

## Objective
Implement a reusable generic helper that selects keys from an object.

This quest trains:
- generic type parameters
- `keyof` + constraints
- returning `Pick<T, K>`
- safe object iteration

## Requirements
Edit `task.ts` to export:

1) `function pick<T extends object, K extends keyof T>(obj: T, keys: readonly K[]): Pick<T, K>`

### pick rules
- Return a new object containing only the requested keys from `obj`.
- Do not mutate `obj`.
- Keys are guaranteed by the type system to exist (K extends keyof T).
- Output should include keys in the same order as the keys array (as inserted properties).

## Constraints
- Standard library only.
- No printing.
- Deterministic behavior.

## Success Criteria
Public tests pass.
