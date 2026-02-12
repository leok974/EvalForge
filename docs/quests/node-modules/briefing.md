# Briefing — Node Modules (ESM vs CommonJS)

## Objective
Make Node treat this project as ESM so imports work.

## Contract
- `node src/app.js` prints exactly: `Result: 6`
- No stderr output
- `package.json` must include: `"type": "module"`

## Success Criteria
Public tests pass.
