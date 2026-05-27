# Dockerfile Fundamentals

## FROM

Every Dockerfile must begin with a `FROM` instruction. It sets the base image — the starting point for your new image.

```dockerfile
FROM alpine:3.18
```

`alpine` is a minimal Linux distribution (~5 MB). The `3.18` tag pins the version so your build is reproducible.

Other common bases:
- `python:3.11-slim` — Python runtime, slim variant
- `node:20-slim` — Node.js runtime
- `ubuntu:22.04` — Full Ubuntu

## CMD

`CMD` sets the default command that runs when the container starts.

### Exec form (recommended)

```dockerfile
CMD ["echo", "Hello from inside the container"]
```

The exec form is a JSON array. The first element is the executable, the rest are arguments. No shell is involved — the process runs directly.

### Shell form (avoid)

```dockerfile
CMD echo Hello from inside the container
```

Shell form wraps the command in `/bin/sh -c "..."`. It adds a shell process layer and can behave differently across images (e.g. Alpine uses `sh`, not `bash`).

## Minimal Dockerfile

```dockerfile
FROM alpine:3.18
CMD ["echo", "Hello from inside the container"]
```

That's two lines and a working container image.
