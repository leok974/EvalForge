# Hints: Boss Microservice Stack

**Hint 1** — Add the `nginx` service after the existing ones. Use `image: nginx:alpine` and map `"80:80"`.

**Hint 2** — Declare a top-level `networks` key and assign all services to it:
```yaml
networks:
  app_net:
```
Each service needs:
```yaml
networks:
  - app_net
```

**Hint 3** — Named volumes need a top-level `volumes` declaration AND a mount path on the service:
```yaml
volumes:
  db_data:   # top-level declaration

services:
  db:
    volumes:
      - db_data:/var/lib/postgresql/data
```

**Hint 4** — Use long-form `depends_on` with `condition: service_healthy` to create the dependency chain: nginx → api → db.

**Hint 5** — The API healthcheck uses `curl`. Make sure your Dockerfile installs it (or use a minimal check command that's already in the image).
