# TS Ignition

## Objective
Export a typed function that returns a strict “handshake” payload.

This quest trains the TypeScript ignition basics:
- exporting functions from a module
- writing type aliases / literal types
- returning a value that matches an exact contract

## Requirements
Edit `task.ts` to export:
- `type Handshake`
- `function handshake(): Handshake`

The function must return exactly:
- message: "System Online"
- code: 42
- ok: true

## Constraints
- Do not print.
- Do not read files.
- Deterministic return value only.

## Success Criteria
Public tests pass.
