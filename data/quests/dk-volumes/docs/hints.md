# Hints

## Hint 1 — Volume mount syntax

Under the `db` service, add a `volumes:` block:
```yaml
    volumes:
      - db_data:/var/lib/postgresql/data
```
The format is `<volume-name>:<path-in-container>`.

## Hint 2 — Declare the named volume

At the top level (same indentation as `services:`), add:
```yaml
volumes:
  db_data:
```

## Hint 3 — Complete solution

```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```
