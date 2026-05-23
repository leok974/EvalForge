# Hints

## Hint 1 — Image name typo

Look at the `FROM` line. Is `pyhon` a valid Docker image name?

## Hint 2 — Instruction typo

Look at the second line. Is `WORKIR` a valid Dockerfile instruction?

## Hint 3 — CMD form

The `CMD` uses shell form. Change it to exec form (JSON array):
```dockerfile
CMD ["python", "app.py"]
```

## Full corrected Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```
