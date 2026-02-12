# Tutorial — Environment Variables

## Reading env vars in sh
Environment variables are just shell variables that may or may not be set.

### Safe default pattern (POSIX sh)
Use parameter expansion:

- `${MODE:-dev}` → if MODE is unset or empty, use `dev`
- `${PORT:-3000}` → if PORT is unset or empty, use `3000`

## Writing the file
Use `>` for the first line (create/overwrite) and `>>` for additional lines.
