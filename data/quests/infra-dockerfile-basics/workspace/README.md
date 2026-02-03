# Dockerfile Basics

Create a `Dockerfile` that satisfies these constraints **in order**:

1. `FROM node:20-alpine` (exact)
2. `WORKDIR /app`
3. Copy package manifests first
4. `RUN npm ci`
5. Copy rest of files
6. `EXPOSE 8000`
7. `CMD ["node","server.js"]`
