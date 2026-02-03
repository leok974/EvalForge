# Node Modules: ESM vs CommonJS

This project uses modern ESM `import/export`, but Node is currently loading it incorrectly.

## Goal
Make this command work:
- `node src/app.js`

Expected output:
- `Result: 6`

## Hint
The easiest fix is usually in `package.json`.
