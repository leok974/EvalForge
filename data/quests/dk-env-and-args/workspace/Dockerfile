FROM python:3.11-slim
WORKDIR /app
# TODO: Declare a build argument ARG APP_VERSION with a default of 1.0
# TODO: Set an environment variable ENV APP_ENV=production
# TODO: Set an environment variable ENV VERSION that derives its value from $APP_VERSION
CMD ["python", "-c", "import os; print(os.getenv('APP_ENV', 'not set'))"]
