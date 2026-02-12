# Briefing — node-npm

## Objective
Make npm scripts work and enforce a lockfile contract.

## Contract
- `npm test` runs node:test and passes
- `npm run start` prints `OK`
- `npm run check-lockfile`:
  - fails if package-lock.json missing
  - parses JSON
  - lockfileVersion >= 2
  - if lockfile has `name`, it must equal package.json `name`
  - prints `Lockfile OK` on success

## Success Criteria
All public tests pass.
