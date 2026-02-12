# Tutorial — Node Modules (ESM vs CommonJS)

## What You’re Practicing
- Why `import/export` can fail in Node
- How Node decides whether `.js` files are ESM or CommonJS
- The `package.json` switch that controls default module mode

## Implementation Plan
1. Open `package.json`.
2. Ensure it includes `"type": "module"`.
3. Re-run tests.

## Pitfalls
- Adding `"type": "module"` in the wrong directory
- Editing code to “work around” module mode instead of fixing config
- Printing debug output (tests expect clean stdout/stderr)
