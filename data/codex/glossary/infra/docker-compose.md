---
title: Docker Compose
id: infra/docker-compose
---
# Docker Compose

Tool for defining and running multi-container Docker applications.

## Usage
```bash
docker-compose up
docker-compose down
docker-compose ps
```

## Example `docker-compose.yml`
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "8080:80"
  db:
    image: postgres:14
```
