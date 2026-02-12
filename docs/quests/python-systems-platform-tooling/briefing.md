# Briefing — Internal Tooling & DX

## Objective
Execute a tool request from a fixture file and print a structured JSON result.

## What This Trains
- Tool boundaries: parse input → run tool → return JSON
- Deterministic behavior: stable formatting and ordering
- Defensive validation with clear error codes

## Success Criteria
- Output JSON deep-equals expected.
- No extra stdout beyond the one JSON line.
- Core logic is pure (no IO).
