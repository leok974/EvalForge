# CLI Files & Folders

Edit `task.sh`.

After running:

```sh
sh task.sh
```

You must have:

* `sandbox/archive/2026/invoice.txt` (copied from `fixtures/invoice.txt`)
* `sandbox/README.md` (copied + renamed from `fixtures/readme.md`)
* `sandbox/tmp/` does not exist

## Rules

* Treat `fixtures/` as **read-only**: do NOT delete, move, or modify `fixtures/*.txt` or `fixtures/*.md`.
* Copy invoice and readme (do not move).
* Exit code must be `0` on success.
* No extra stdout/stderr.
