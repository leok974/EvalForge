# Hints

## Hint 1 — ARG syntax

Declare a build argument before WORKDIR:
```
ARG APP_VERSION=1.0
```
The `=1.0` part sets the default value.

## Hint 2 — ENV syntax

After WORKDIR, add two ENV lines:
```
ENV APP_ENV=production
ENV VERSION=$APP_VERSION
```
The `$APP_VERSION` references the ARG declared above.

## Hint 3 — Complete solution

```dockerfile
FROM python:3.11-slim
ARG APP_VERSION=1.0
WORKDIR /app
ENV APP_ENV=production
ENV VERSION=$APP_VERSION
CMD ["python", "-c", "import os; print(os.getenv('APP_ENV', 'not set'))"]
```
