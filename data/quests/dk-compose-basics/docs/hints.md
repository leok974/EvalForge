# Hints: Compose Basics

**Hint 1** — Service definitions are children of the `services` key. Match the indentation of the existing `db` block.

**Hint 2** — Port mapping syntax is `"HOST:CONTAINER"`. To map host 8080 → container 8080: `- "8080:8080"`.

**Hint 3** — `depends_on` takes a list of service names:
```yaml
depends_on:
  - db
```
