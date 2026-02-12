# Node Modules — ESM vs CommonJS

This project uses modern ESM `import/export`, but Node is loading files as CommonJS.

## Objective
Make the program run successfully under ESM.

## Goal
This command must work:
- `node src/app.js`

Expected stdout:
- `Result: 6`

## Requirements
- Configure the project so Node treats `.js` files as ESM.
- Do not change the program’s behavior or output formatting.
- No extra stdout/stderr.

## Hint
The easiest fix is usually in `package.json`.

## Success Criteria
Public tests pass.
