# Hints — Redirection

## Hint 1 (Concept)
Use `>` once to create the file, and `>>` to append additional lines.

## Hint 2 (Guided)
To insert all lines from a file, use `cat`.

## Hint 3 (Near-solution)
A typical structure is:
- `echo HEADER > outputs/report.txt`
- `cat fixtures/data.txt >> outputs/report.txt`
- `echo FOOTER >> outputs/report.txt`
