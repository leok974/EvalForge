# Briefing — Globs & Search

## Objective
Search across multiple log files to extract:
1) how many error lines exist
2) which files contain errors

## Contract
Running:

```sh
sh task.sh
```

must create:

* `outputs/error_count.txt` → `3`
* `outputs/error_files.txt` → exactly:

  ```
  app.log
  db.log
  ```

## Constraints

* Only consider `fixtures/*.log`.
* Match `ERROR` exactly (case-sensitive).
* Output must be deterministic (sorted basenames).
* No extra stdout/stderr. Exit code `0`.
