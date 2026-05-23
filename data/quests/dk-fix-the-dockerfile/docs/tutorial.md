# Common Dockerfile Mistakes

## Typo in the image name

```dockerfile
FROM pyhon:3.11-slim   # WRONG: "pyhon" is not an image
FROM python:3.11-slim  # CORRECT
```

Docker pulls images from registries by exact name. A typo causes a `pull access denied` or `image not found` error.

## Typo in an instruction

```dockerfile
WORKIR /app   # WRONG: "WORKIR" is not a Dockerfile instruction
WORKDIR /app  # CORRECT
```

Dockerfile instructions are specific keywords. Unrecognised words cause a parse error.

## CMD shell form vs exec form

```dockerfile
CMD python app.py              # Shell form — uses /bin/sh -c
CMD ["python", "app.py"]       # Exec form — recommended
```

Shell form invokes a shell process. Exec form (JSON array) runs the process directly. Exec form is best practice because:
- No shell startup overhead
- Signals (SIGTERM) are delivered directly to your process
- Behaviour is consistent across images (not all have `/bin/sh`)
