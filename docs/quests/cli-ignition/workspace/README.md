# CLI Ignition

Edit `task.sh` so running:

```sh
sh task.sh
```

prints **exactly 3 lines**:

```
CWD=workspace
FILES=3
OK
```

## Rules

* `CWD` must be the **basename of the current working directory**.
* `FILES` must count **only regular files directly under `fixtures/`** (ignore subdirectories).
* Do **not** hardcode the number; compute it.
* Exit code must be **0** on success.
* No extra output (no debug prints).
