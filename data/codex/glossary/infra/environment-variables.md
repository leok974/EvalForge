---
title: Environment Variables
id: infra/environment-variables
---
# Environment Variables

Configuration values passed to applications at runtime.

## Docker Usage
```bash
docker run -e DB_HOST=localhost myapp
```

## Compose File
```yaml
services:
  web:
    environment:
      - NODE_ENV=production
```

## Best Practices
- Never commit secrets
- Use `.env` files for local dev
