---
title: Docker Volumes
id: infra/volumes
---
# Docker Volumes

Persist data outside container lifecycle.

## Types
- **Named volumes**: Managed by Docker
- **Bind mounts**: Map host directory
- **tmpfs**: Temporary, in-memory

## Usage
```bash
docker run -v mydata:/data myapp
docker volume create mydata
docker volume ls
```
