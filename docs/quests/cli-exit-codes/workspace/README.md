# Exit Codes

Edit `task.sh`.

## Rules
- If `fixtures/error.flag` exists, exit with code `1`.
- Otherwise exit with code `0`.
- Do not print anything to stdout or stderr.
- Exit codes must be exact and deterministic.
