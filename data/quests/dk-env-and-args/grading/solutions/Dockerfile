FROM python:3.11-slim
ARG APP_VERSION=1.0
WORKDIR /app
ENV APP_ENV=production
ENV VERSION=$APP_VERSION
CMD ["python", "-c", "import os; print(os.getenv('APP_ENV', 'not set'))"]
