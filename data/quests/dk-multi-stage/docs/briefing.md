# Briefing: Multi-Stage Builds

The current Dockerfile is a single-stage build. It works, but the final image contains Node.js dev dependencies, source files, and build tooling — bloat you don't need in production.

## Mission

Refactor the Dockerfile into two stages:

1. **builder** (`FROM node:18 AS builder`) — install dependencies and build
2. **runtime** (`FROM node:18-slim`) — copy only the compiled output from the builder

## Key instruction

```dockerfile
COPY --from=builder /app/dist ./dist
```

This tells Docker to pull files from the `builder` stage into the current stage, leaving all the dev cruft behind.
