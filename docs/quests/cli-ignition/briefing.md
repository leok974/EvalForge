# Briefing — CLI Ignition

## Objective
Produce **exact**, testable CLI output based on the current directory and fixture contents.

## Contract
Running:

```sh
sh task.sh
```

prints **exactly**:

1. `CWD=<basename of current directory>`
2. `FILES=3` (count regular files directly under `fixtures/`)
3. `OK`

Exit code must be **0** and you must not print extra lines.

## Success Criteria

Public tests pass and your output formatting is exact.
