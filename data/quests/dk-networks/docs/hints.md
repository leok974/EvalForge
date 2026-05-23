# Hints

## Hint 1 — Attach a service to a network

Under each service, add:
```yaml
    networks:
      - backend
```

## Hint 2 — Declare the network

At the top level (same indentation as `services:`), add:
```yaml
networks:
  backend:
```

## Hint 3 — Complete solution

```yaml
services:
  api:
    image: python:3.11-slim
    networks:
      - backend

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
    networks:
      - backend

networks:
  backend:
```
