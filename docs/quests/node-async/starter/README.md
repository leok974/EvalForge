# Async Patterns

Handling errors in async code is critical. 

## Goals
Implement `getUserName(id)` in `src/users.js`:
1. Use `await loadUser(id)` to get the user object.
2. Return the `name` property.
3. **Handle Errors**: If `loadUser` fails (throws), return `"Guest"` instead of crashing.

## Testing
Run `node index.js`.
- `ID 1` should print `User1`
- `ID -1` should print `Guest` (because ID -1 throws)
