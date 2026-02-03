---
title: Docker
id: infra/docker
---
# Docker

Platform for developing, shipping, and running applications in containers.

## Key Concepts
- **Image**: Blueprint for a container
- **Container**: Running instance of an image
- **Dockerfile**: Instructions to build an image

## Basic Commands
```bash
docker build -t myapp .
docker run -p 8080:80 myapp
docker ps
```
