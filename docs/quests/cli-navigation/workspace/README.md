# CLI Navigation

Edit `task.sh`.

When you run:

```sh
sh task.sh
```

it must create these files:

1. `outputs/location.txt`

   * contains the absolute path of the `fixtures/site/pages` directory
   * you must `cd` into that directory before writing

2. `outputs/pages.txt`

   * contains the filenames in `fixtures/site/pages`, one per line
   * only the files in that directory (no paths)

3. `outputs/back.txt`

   * contains the absolute path of the workspace directory
   * you must `cd` back before writing

## Rules

* Create `outputs/` if missing.
* Output must be deterministic.
* Exit code must be `0` on success.
* No extra stdout/stderr.
