---
title: Container Networking
id: infra/container-networking
---
# Container Networking

Enables communication between containers and external systems.

## Network Types
- **Bridge**: Default, isolated network
- **Host**: Uses host's network stack
- **None**: No networking

## Commands
```bash
docker network create mynet
docker run --network=mynet myapp
```
