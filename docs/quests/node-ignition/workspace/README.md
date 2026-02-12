# Node Ignition

You are building a tiny CLI greeting program.

## Objective
Implement a reusable `greet(name)` function and wire it into a Node CLI.

## Requirements

### greet(name)
Implement `greet(name)` in `src/greet.js`.

Rules:
- Accept a string.
- Trim whitespace.
- If the trimmed name is empty, throw an Error.
- Otherwise return exactly: `Hello, <name>!`

### CLI behavior (index.js)
Running:
- `node index.js Leo` prints to stdout:
  `Hello, Leo!`
- `node index.js` prints a usage message to **stderr** and exits with code **2**:
  `Usage: node index.js <name>`

Notes:
- Treat whitespace-only names as missing (same behavior as no arg).
- Keep output formatting exact.

## Success Criteria
All public tests pass.
