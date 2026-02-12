# Briefing — Node Ignition

## Objective
Build a tiny Node CLI greeting tool with a strict contract.

## Contract
- `greet(name)` trims input and returns `Hello, <name>!`
- `greet` throws on empty/whitespace-only
- CLI:
  - `node index.js Leo` → stdout `Hello, Leo!`
  - `node index.js` or whitespace arg → stderr usage + exit code 2

## Success Criteria
All public tests pass with exact output formatting.
