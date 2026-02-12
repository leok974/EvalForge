# Briefing — Exit Codes

## Objective
Write a script that detects failure conditions and signals them via exit codes.

## Success Criteria
When running `sh task.sh`:
- If `fixtures/error.flag` exists:
  - Exit with code `1`
- If `fixtures/error.flag` does NOT exist:
  - Exit with code `0`

## Constraints
- **No stdout/stderr output**.
- Exit codes must be precise.
