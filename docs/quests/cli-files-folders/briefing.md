# Briefing — CLI Files & Folders

## Objective
Practice safe filesystem operations: create directories, copy files without data loss, and remove a temp directory safely.

## Contract
Running:

```sh
sh task.sh
```

must produce:

* `sandbox/archive/2026/invoice.txt` copied from `fixtures/invoice.txt`
* `sandbox/README.md` copied from `fixtures/readme.md`
* `sandbox/tmp/` must not exist

## Constraints

* Treat `fixtures/` as read-only: do not delete, move, or modify fixture files.
* Use standard shell utilities (`mkdir`, `cp`, `rm`).
* Exit code must be `0`. No extra stdout/stderr.
