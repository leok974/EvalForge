# Tutorial — node-env-config

## What You’re Practicing
- `process.env` is always strings (or undefined)
- defaults vs required secrets
- failing fast with clear errors

## Implementation Plan
1. Read `process.env.PORT`
   - if missing/blank → 3000
   - else convert to number
2. Read `process.env.DB_URL`
   - if missing/blank → throw Error
3. Export a `config` object used by `index.js`

## Pitfalls
- forgetting to default PORT
- allowing empty string DB_URL
- treating PORT as a string in output logic
