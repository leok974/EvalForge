# Briefing — Environment Variables

## Objective
Write a config file using environment variables with safe defaults.

## Success Criteria
After running `sh task.sh`, `outputs/config.txt` must equal:

- `MODE=<mode>` (default `dev`)
- `PORT=<port>` (default `3000`)

## Constraints
- Use env vars (`MODE`, `PORT`) and default if missing.
- No extra stdout/stderr output. Exit code 0.
