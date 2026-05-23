# Named Networks in Docker Compose

## Declaring a network

At the top level of `compose.yaml`:

```yaml
networks:
  backend:
```

An empty value uses the default bridge driver, which is usually what you want.

## Attaching a service to a network

Under each service:

```yaml
services:
  api:
    image: python:3.11-slim
    networks:
      - backend
```

A service can be on multiple networks simultaneously:

```yaml
    networks:
      - frontend
      - backend
```

## Service discovery

Services on the same network can reach each other using the service name as the hostname. If `api` and `db` are both on `backend`, the Python app can connect to Postgres at `db:5432`.

## Complete example

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
