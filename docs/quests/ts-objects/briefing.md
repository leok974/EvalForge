# Briefing — TS Objects

## Objective
Normalize an unknown input into a safe `Config` object with defaults.

## Contract
- Invalid input → defaults
- retries: integer clamped to 0..10
- timeoutMs: integer clamped to 50..5000
- baseUrl: trimmed non-empty string else default
- headers: lowercase keys, trimmed values, drop empty entries

## Success Criteria
Public tests pass with no extra output.
