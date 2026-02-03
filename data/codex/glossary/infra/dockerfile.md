---
title: Dockerfile
id: infra/dockerfile
---
# Dockerfile

Text file containing instructions to build a Docker image.

## Common Instructions
- `FROM`: Base image
- `COPY`: Copy files
- `RUN`: Execute commands
- `CMD`: Default command
- `EXPOSE`: Document ports

## Example
```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
```
