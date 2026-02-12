# TS Arrays

## Objective
Implement a small data-cleaning pipeline using arrays.

This quest trains:
- iterating arrays
- filtering + mapping
- sorting deterministically
- returning a typed result

## Requirements
Edit `task.ts` to export:

1) `function cleanScores(input: unknown): number[]`

### cleanScores rules
Given an unknown input, return a cleaned array of scores:
- If input is not an array, return []
- Keep only finite numbers (reject NaN, Infinity, -Infinity)
- Round each score to the nearest integer
- Keep only scores in range 0..100 (inclusive)
- Remove duplicates
- Sort ascending

## Constraints
- Standard library only.
- No printing.
- Deterministic behavior.

## Success Criteria
Public tests pass.
