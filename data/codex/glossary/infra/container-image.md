---
title: Container Image
id: infra/container-image
---
# Container Image

Read-only template with application code and dependencies.

## Layers
- Images are built in layers
- Each instruction in Dockerfile creates a layer
- Layers are cached for efficiency

## Best Practices
- Use official base images
- Minimize layers
- Use `.dockerignore`
