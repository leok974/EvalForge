# Hints — node-npm

## Hint 1
Use `fs.existsSync` before reading the lockfile.

## Hint 2
On failure: print an error and `process.exit(1)`.

## Hint 3
Only enforce name matching if `package-lock.json` includes a `name` field.
