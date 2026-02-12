# Briefing — TS Vars

## Objective
Export a constant greeting and a typed configuration object that match an exact contract.

## Contract
- `greeting` must be exactly: "System Online"
- `config` must equal:
  { retryLimit: 3, timeoutMs: 250, env: "dev" }

## Constraints
- No printing
- No IO
- Deterministic values only

## Success Criteria
Public tests pass.
