# Hints — TS Types

## Hint 1
A type guard is a function returning `value is T` and doing runtime checks.

## Hint 2
Use a small helper pattern:
- `if (!value || typeof value !== "object") return false;`

## Hint 3
Role check can be:
- `role === "admin" || role === "user" || role === "guest"`
