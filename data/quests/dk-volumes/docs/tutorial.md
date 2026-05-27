# Named Volumes in Docker Compose

## Declaring a named volume

Named volumes are declared at the top level of `compose.yaml`:

```yaml
volumes:
  db_data:
```

An empty value (`db_data:`) is valid — Docker uses its default driver.

## Mounting the volume

Under the service definition, add a `volumes:` key listing mounts:

```yaml
services:
  db:
    image: postgres:15-alpine
    volumes:
      - db_data:/var/lib/postgresql/data
```

The format is `<volume-name>:<container-path>`. The volume `db_data` maps to `/var/lib/postgresql/data` inside the container.

## Why named volumes?

Named volumes outlive their container. Even after `docker compose down`, the data remains. Only `docker compose down --volumes` removes them.

Contrast with **bind mounts** which look like `./data:/var/lib/postgresql/data` — those map a host directory directly. Named volumes are managed by Docker and are more portable across machines.

## Complete example

```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```
