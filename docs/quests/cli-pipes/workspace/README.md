# Pipes

Edit `task.sh` so it reads `fixtures/names.txt` and produces `outputs/top.txt`.

## Output
`outputs/top.txt` must contain exactly 2 lines:
`name count`

Example:
leo 3

## Rules
- Case-sensitive (treat "Leo" and "leo" as different).
- Determine the top 2 most frequent names.
- Deterministic ordering:
  1) sort by count descending
  2) tie-break by name ascending
- Use pipes (`|`) to chain commands.
- Do not use temporary files.
- No extra stdout/stderr. Exit code must be 0.
