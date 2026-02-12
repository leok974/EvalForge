# Briefing — TS Control

## Objective
Classify a status code using a strict contract and return a typed `StatusClass`.

## Contract
- Input is `unknown`.
- Only integer numbers in range 100–599 are considered.
- 200s → success
- 300s → redirect
- 400s → client_error
- 500s → server_error
- Anything else → invalid

## Success Criteria
All public tests pass with no extra output.
