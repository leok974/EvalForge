# Hints: Health Checks and Restart Policies

**Hint 1** — `healthcheck.test` must be a YAML list. CMD-SHELL runs the command in a shell:
```yaml
test: ["CMD-SHELL", "pg_isready -U postgres"]
```

**Hint 2** — `restart: unless-stopped` goes at the same indentation level as `image:`.

**Hint 3** — The long-form `depends_on` syntax uses a dict instead of a list:
```yaml
depends_on:
  db:
    condition: service_healthy
```
Without this change, `condition: service_healthy` has no effect.
