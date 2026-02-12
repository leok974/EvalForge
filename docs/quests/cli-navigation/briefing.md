# Briefing — CLI Navigation

## Objective
Prove you can navigate a repo safely: move into a target directory, capture its absolute path, list its files, and return home.

## Contract
Running:

```sh
sh task.sh
```

must create:

* `outputs/location.txt` → absolute path to `fixtures/site/pages` (you must `cd` there first)
* `outputs/pages.txt` → filenames in `fixtures/site/pages`, one per line
* `outputs/back.txt` → absolute path to the workspace directory (after you `cd` back)

Exit code must be **0**. No extra stdout/stderr.
