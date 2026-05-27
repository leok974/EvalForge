# Stage 1: Build Frontend
FROM node:22-alpine as frontend-build
WORKDIR /app/web
# Copy package files from apps/web
COPY apps/web/package*.json ./
COPY bust_cache.txt* ./
RUN npm install
# Copy source code
COPY apps/web/ ./
RUN npm run build

# Stage 2: Python Backend
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    docker.io \
    docker-cli \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 (required for JavaScript quest execution)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js packages for quest execution
# react + react-dom: react_core quest tests import from workspace/task.mjs
# react-test-renderer: react_core public tests use react_test_helpers.mjs which imports it
# tsx: TypeScript runner uses `node --import tsx` to execute .ts test files
# Installing at /app/node_modules so Node ESM resolution walks up and finds them
RUN npm install --prefix /app react react-dom react-test-renderer tsx

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY arcade_app /app/arcade_app
# Copy runtimes (Selenium helpers, step logger, etc.)
COPY runtimes /app/runtimes
# Copy docs (ladder specs, codex, etc.)
COPY docs /app/docs
# Copy data/config if needed (assuming data dir exists)
# COPY data /app/data

# Copy built frontend assets from Stage 1
COPY --from=frontend-build /app/web/dist /app/static

# Baked-in env defaults (non-secret, non-environment-specific values only)
# EVALFORGE_MOCK_GRADING and EVALFORGE_AUTH_MODE must NOT be set here —
# they must be injected at runtime via docker-compose / deployment config
# so that production vs dev behaviour is controlled without rebuilding the image.
ENV PORT=8092
ENV WEB_DIST=/app/static
ENV EVALFORGE_ENV=prod

# Run command
CMD ["python", "-m", "uvicorn", "arcade_app.agent:app", "--host", "0.0.0.0", "--port", "8092"]
