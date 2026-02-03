# Environment Configuration

Hardcoding secrets (like database URLs) is bad. Use environment variables instead.

## Goals
Update `config.js` to:
1. Load `PORT` from `process.env`. If missing, default to `3000`.
2. Load `DB_URL` from `process.env`. **This is required.** If missing, throw an error or exit.

## Running
We don't use a `.env` file loader here (like dotenv) to keep it simple, but you can pass variables manually:

```bash
# Linux/Mac
PORT=4000 DB_URL=postgres://localhost node index.js

# Windows (PowerShell)
$env:PORT=4000; $env:DB_URL="postgres://localhost"; node index.js
```
