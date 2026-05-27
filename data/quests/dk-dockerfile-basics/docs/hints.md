# Hints

## Hint 1 — WORKDIR

After `FROM`, add:
```
WORKDIR /app
```
This makes `/app` the working directory for all following instructions.

## Hint 2 — COPY and CMD

```
COPY app.py .
CMD ["python", "app.py"]
```
`COPY app.py .` copies your file to `/app/app.py` (because WORKDIR is `/app`).

## Hint 3 — Complete solution

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```
