# Hints — Globs & Search

## Hint 1 (Concept)
Use a glob like `fixtures/*.log` so you don’t hardcode filenames.

## Hint 2 (Guided)
To list files containing matches, `grep -l "ERROR" fixtures/*.log` is the fastest route. You may need to strip `fixtures/`.

## Hint 3 (Near-solution)
- Count lines:
  - `grep -h "ERROR" fixtures/*.log | wc -l`
- Get basenames + sort:
  - `grep -l "ERROR" fixtures/*.log | xargs -n1 basename | sort`
Write the outputs to the two files in `outputs/`.
