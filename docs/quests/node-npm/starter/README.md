# npm: Packages, Scripts, and Lockfiles

This repo is meant to support:
- `npm test`
- `npm run start`
- `npm run check-lockfile`

Right now the scripts are broken.

## Goals
1) Fix package.json scripts so npm commands work.
2) Implement `scripts/check-lockfile.js` so it:
   - fails if package-lock.json is missing
   - parses JSON
   - ensures lockfileVersion >= 2
   - ensures lockfile name matches package.json name (if present)
