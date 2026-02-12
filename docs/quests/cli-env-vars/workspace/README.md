# Environment Variables

Edit `task.sh` so that running:

```sh
sh task.sh
```

creates `outputs/config.txt` containing **exactly**:

```
MODE=<mode>
PORT=<port>
```

## Rules

* Read `MODE` and `PORT` from environment variables.
* If `MODE` is **unset or empty**, default to `dev`.
* If `PORT` is **unset or empty**, default to `3000`.
* Do not hardcode values (except defaults).
* No extra stdout/stderr output. Exit code must be 0.
