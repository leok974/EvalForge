# Hints — CLI Files & Folders

## Hint 1 (Concept)
Use `mkdir -p` so your script works whether or not the folder exists.

## Hint 2 (Guided)
Fixtures are read-only. If you use `mv`, your tests will fail because the source disappears.

## Hint 3 (Near-solution)
Commands you need:
- `mkdir -p sandbox/archive/2026`
- `cp fixtures/invoice.txt sandbox/archive/2026/invoice.txt`
- `cp fixtures/readme.md sandbox/README.md`
- `rm -rf sandbox/tmp`
