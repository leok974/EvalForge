# Briefing — TS Types

## Objective
Implement a `User` type model and a runtime-safe parser.

## Contract
- `Role` is a union of: "admin" | "user" | "guest"
- `User` has: { id: number; name: string; role: Role }
- `isUser(unknown)` returns true only for valid User shapes.
- `parseUser(json)` returns a User if valid, otherwise throws `Error("EF_TS_TYPES_INVALID")`.

## Success Criteria
All public tests pass with no extra output.
