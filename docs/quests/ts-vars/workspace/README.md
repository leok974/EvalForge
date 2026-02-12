# TS Vars

## Objective
Export two values:
- a constant greeting string
- a typed configuration object

This quest trains:
- `const` vs `let`
- basic type annotations
- returning/declaring values that match an exact contract

## Requirements
Edit `task.ts` to export:

1) `const greeting`
- must be exactly: "System Online"

2) `type Config` and `const config: Config`
Config must contain:
- `retryLimit`: 3
- `timeoutMs`: 250
- `env`: "dev"

## Constraints
- Do not print.
- No IO.
- Deterministic values only.

## Success Criteria
Public tests pass.
