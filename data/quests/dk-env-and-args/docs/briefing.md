# ENV and ARG

Docker has two ways to pass values into a build:

- **`ARG`** — a build-time variable. Available during `docker build`, but **not** at container runtime.
- **`ENV`** — an environment variable. Baked into the image and available at runtime inside the container.

## Your Task

Update the Dockerfile to:

1. Declare a build argument `ARG APP_VERSION=1.0` (default `1.0`)
2. Set `ENV APP_ENV=production`
3. Set `ENV VERSION=$APP_VERSION` — derive the runtime variable from the build argument

The CMD already reads `APP_ENV` at runtime using `os.getenv()`. After your changes, running the container should print `production`.
