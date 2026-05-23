# Briefing: Secrets and Config

The current Compose file has `secret123` hardcoded in plain text. Anyone with access to the repo can see your database password.

## Mission

Replace the hardcoded credentials with `env_file` references. Docker Compose will load variables from `.env` at runtime — the file stays on the host and out of source control.

```yaml
env_file:
  - .env
```

Apply `env_file` to **both** the `api` and `db` services. Remove the hardcoded password values from `environment:`. Non-sensitive config (like `DB_HOST` and `POSTGRES_DB`) can stay in `environment:`.

## Rule of thumb

If a value would be dangerous in a leaked Git commit, it belongs in `.env`.
