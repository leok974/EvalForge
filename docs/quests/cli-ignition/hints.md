# Hints — CLI Ignition

## Hint 1 (Concept)
You can compute the current folder name with:
`basename "$(pwd)"`

## Hint 2 (Guided)
To count only direct regular files:
`find fixtures -maxdepth 1 -type f | wc -l`

If `wc -l` prints leading spaces, strip them with:
`tr -d ' '`

## Hint 3 (Near-solution)
Store values in variables, then print exactly:
- `echo "CWD=$CWD"`
- `echo "FILES=$FILES"`
- `echo "OK"`
