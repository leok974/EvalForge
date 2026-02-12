# Tutorial — node-npm

## What You’re Practicing
- npm scripts as developer UX
- lockfiles for reproducibility
- minimal Node scripting: fs + JSON parsing + exit codes

## Implementation Plan
1. Fix scripts in `package.json`:
   - test → `node --test`
   - start → `node index.js`
   - check-lockfile → `node scripts/check-lockfile.js`
2. Implement `check-lockfile.js`:
   - ensure file exists
   - JSON.parse and validate fields
   - print success message

## Pitfalls
- printing success to stderr
- exiting 0 on failure
- forgetting to enforce lockfileVersion >= 2
