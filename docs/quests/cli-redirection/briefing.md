# Briefing — Redirection

## Objective
Generate `outputs/report.txt` by composing:
- a header line
- the contents of `fixtures/data.txt`
- a footer line

## Success Criteria
After running:
```sh
sh task.sh
```

`outputs/report.txt` matches the contract exactly and the script exits 0.

## Constraints

* Preserve the data lines exactly.
* Use `>` and `>>` redirection (no temp files).
* No extra stdout/stderr output.
