# npm: Packages, Scripts, and Lockfiles

## Objective
Fix npm scripts and implement a lockfile checker for reproducible installs.

This quest trains:
- npm scripts (`npm test`, `npm run start`)
- why lockfiles matter
- basic Node filesystem + JSON parsing

## Goals
1) Fix `package.json` scripts so these commands work:
   - `npm test`
   - `npm run start`
   - `npm run check-lockfile`

2) Implement `scripts/check-lockfile.js` so it:
   - fails if `package-lock.json` is missing
   - parses the lockfile JSON
   - ensures `lockfileVersion >= 2`
   - ensures lockfile `name` matches `package.json` `name` (if lockfile has a name)
   - prints `Lockfile OK` on success (exact text, case-insensitive accepted by tests)

## Constraints
- Standard library only.
- Do not modify public tests.
- Deterministic output.

## Success Criteria
All public tests pass.
