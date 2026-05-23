# Hints: Secrets and Config

**Hint 1** — `env_file` is a list of file paths relative to the Compose file:
```yaml
env_file:
  - .env
```

**Hint 2** — Variables loaded via `env_file` merge with `environment:`. You can keep non-sensitive values like `DB_HOST: db` and `POSTGRES_DB: app` in `environment:`.

**Hint 3** — The grader checks that `env_file` is present on both services. Both `api` and `db` must reference it.

**Hint 4** — You don't need a real `.env` file to pass — the grader validates the YAML structure only.
