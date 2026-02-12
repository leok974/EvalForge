# Briefing — TS Ignition

## Objective
Export a `handshake()` function that returns a payload matching an exact TypeScript contract.

## Contract
Return exactly:
- message: "System Online"
- code: 42
- ok: true

## Constraints
- No printing
- No IO
- Deterministic return value only

## Success Criteria
- Public tests pass
- Returned object matches the literal-type contract
