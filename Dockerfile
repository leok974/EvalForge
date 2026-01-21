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
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY arcade_app /app/arcade_app
# Copy docs (ladder specs, codex, etc.)
COPY docs /app/docs
# Copy data/config if needed (assuming data dir exists)
# COPY data /app/data

# Copy built frontend assets from Stage 1
COPY --from=frontend-build /app/web/dist /app/static

# Env vars for production
ENV PORT=8092
ENV EVALFORGE_MOCK_GRADING=1
ENV WEB_DIST=/app/static
ENV EVALFORGE_ENV=prod

# Run command
CMD ["python", "-m", "uvicorn", "arcade_app.agent:app", "--host", "0.0.0.0", "--port", "8092"]
