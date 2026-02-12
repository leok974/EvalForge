# Environment Configuration

Hardcoding secrets (like database URLs) is bad. Use environment variables instead.

## Objective
Load configuration from `process.env` with safe defaults and required validation.

## Goals
Update `config.js` to:
1) Load `PORT` from `process.env`. If missing, default to `3000`.
   - `PORT` should become a number (not a string).
2) Load `DB_URL` from `process.env`. This is required.
   - If missing or blank, throw an Error (or exit with non-zero).

## Running
No dotenv in this quest. Pass variables manually:

```bash
# Linux/Mac
PORT=4000 DB_URL=postgres://localhost node index.js

# Windows (PowerShell)
$env:PORT=4000; $env:DB_URL="postgres://localhost"; node index.js
```

## Success Criteria

Public tests pass.
