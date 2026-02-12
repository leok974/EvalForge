# Briefing — node-env-config

## Objective
Load runtime config from environment variables with safe defaults.

## Contract
- `PORT`:
  - if set → use it
  - if missing/blank → default to 3000
- `DB_URL`:
  - required (missing/blank must fail)

## Success Criteria
Public tests pass.
