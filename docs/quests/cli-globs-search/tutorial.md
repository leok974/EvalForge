# Tutorial — Globs & Search

## Mental model
You’re doing two passes over the same file set:

1) **Count matching lines**
2) **Identify which files contain at least one match**

## Useful tools
- `grep "ERROR" fixtures/*.log` searches across many files
- `grep -c "ERROR" file.log` counts matches per file
- `grep -l "ERROR" fixtures/*.log` prints filenames that contain a match
- `sort` makes output deterministic
- `basename` strips directories (or use `sed`)

## Plan
1) Count total ERROR lines across all `fixtures/*.log` and write the number to `outputs/error_count.txt`.
2) Produce a sorted list of basenames of the `.log` files that contain at least one `ERROR`, one per line, to `outputs/error_files.txt`.

## Pitfalls
- Counting files instead of lines (you need **lines**)
- Matching lowercase `error` (must match `ERROR` only)
- Forgetting to sort filenames
- Printing full paths instead of basenames
- Adding debug prints that break grading
