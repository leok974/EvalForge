---
title: Container Registry
id: infra/container-registry
---
# Container Registry

Service for storing and distributing container images.

## Popular Registries
- Docker Hub
- GitHub Container Registry (GHCR)
- Google Container Registry (GCR)
- AWS ECR

## Usage
```bash
docker tag myapp:latest user/myapp:v1
docker push user/myapp:v1
docker pull user/myapp:v1
```
