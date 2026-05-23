# ARG vs ENV in Dockerfiles

## ARG — Build-time variable

```dockerfile
ARG APP_VERSION=1.0
```

`ARG` declares a variable that can be passed at build time:
```bash
docker build --build-arg APP_VERSION=2.5 .
```

If not passed, the default value (`1.0`) is used. **Important:** ARG values are NOT available inside the running container — they only exist during the build.

## ENV — Runtime environment variable

```dockerfile
ENV APP_ENV=production
```

`ENV` sets a variable that is baked into the image and available in every container created from it. The value is readable via `os.getenv("APP_ENV")` in Python, `process.env.APP_ENV` in Node, etc.

## Deriving ENV from ARG

You can set an `ENV` using the value of an `ARG`:

```dockerfile
ARG APP_VERSION=1.0
ENV VERSION=$APP_VERSION
```

This captures the build-time value into a runtime variable. When you run the container, `VERSION` will be `1.0` (or whatever was passed via `--build-arg`).

## Scope rules

- `ARG` must be declared BEFORE it is referenced
- `ENV` persists to all subsequent layers and to the running container
- `ARG` does NOT persist past its build stage
