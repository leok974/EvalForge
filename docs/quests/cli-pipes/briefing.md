# Briefing — Pipes

## Objective
Compute name frequencies from `fixtures/names.txt` and write the top 2 results to `outputs/top.txt`.

## Contract
Running:
```sh
sh task.sh
```

must create `outputs/top.txt` with exactly:

```
leo 3
maya 2
```

## Constraints

* Case-sensitive.
* Use pipes (`|`) and no temporary files.
* Deterministic ordering: count desc, then name asc.
* No extra stdout/stderr. Exit code 0.
