# Dockerfile Instructions: WORKDIR, COPY, CMD

## WORKDIR

`WORKDIR` sets the current directory inside the container for subsequent instructions and for the running process.

```dockerfile
WORKDIR /app
```

If `/app` does not exist, Docker creates it. After `WORKDIR /app`, a `COPY app.py .` copies the file to `/app/app.py`.

## COPY

`COPY` copies files from the build context (your machine) into the image.

```dockerfile
COPY app.py .
```

The first argument is the source path (relative to the build context). The second is the destination inside the image. `.` means "current working directory" — which is `/app` because of the WORKDIR instruction above.

## CMD

`CMD` sets the default command. Exec form:

```dockerfile
CMD ["python", "app.py"]
```

## Putting it together

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

When you run the container it executes `python /app/app.py`.
