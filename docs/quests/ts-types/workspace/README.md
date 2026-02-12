# TS Types

## Objective
Model a small API payload using TypeScript types and validate it at runtime.

This quest trains:
- `type` aliases and interfaces
- string literal unions
- narrowing via type guards
- returning a value that matches an exact contract

## Requirements
Edit `task.ts` to export:

1) `type Role = "admin" | "user" | "guest"`
2) `type User = { id: number; name: string; role: Role }`
3) `function isUser(value: unknown): value is User`
4) `function parseUser(json: string): User`

### parseUser rules
- Parse the JSON string.
- Validate the shape using `isUser`.
- If valid, return the User.
- If invalid JSON or invalid shape, throw `Error("EF_TS_TYPES_INVALID")`.

## Constraints
- Standard library only.
- No printing.
- Deterministic behavior.

## Success Criteria
Public tests pass.
