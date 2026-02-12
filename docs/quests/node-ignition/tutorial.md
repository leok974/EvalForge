# Tutorial — Node Ignition

## What You’re Practicing
- ESM modules (`import` / `export`)
- CLI args via `process.argv`
- stderr vs stdout
- exit codes and “usage” contracts

## Implementation Plan
1. Implement `greet(name)`:
   - trim
   - throw on blank
   - return exact string
2. Implement CLI:
   - read `process.argv[2]`
   - if missing/blank: `console.error(usage)` + `process.exit(2)`
   - else: print greeting to stdout

## Pitfalls
- Printing usage to stdout instead of stderr
- Exiting with code 0/1 instead of 2 for usage
- Forgetting to treat whitespace-only as “missing”
