# Async Patterns

Handling errors in async code is critical.

## Objective
Implement `getUserName(id)` so it returns a user name on success and a safe fallback on failure.

## Goals
Implement `getUserName(id)` in `src/users.js`:

1) Use `await loadUser(id)` to get the user object.
2) Return the `name` property.
3) Handle errors: if `loadUser` throws, return `"Guest"` instead of crashing.

## Local Check
Run:
```bash
node index.js
```

Expected output:

* `ID 1: User1`
* `ID -1: Guest`

## Constraints

* Do not change `db.js`
* No extra logging
* Deterministic behavior

## Success Criteria

Public tests pass.
