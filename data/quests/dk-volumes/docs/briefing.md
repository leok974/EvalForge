# Volumes

Containers are ephemeral — when a container stops, everything written to its filesystem is lost. **Volumes** solve this by mounting persistent storage into the container.

Docker Compose supports two volume types:
- **Named volumes** — managed by Docker, survive container restarts and recreation
- **Bind mounts** — map a host path directly into the container

Named volumes are the recommended approach for database data and other persistent state.

## Your Task

Update `compose.yaml` so that:

1. The `db` service mounts the named volume `db_data` at `/var/lib/postgresql/data` (the default Postgres data directory)
2. The `db_data` named volume is declared at the top level under `volumes:`

This ensures Postgres data persists across `docker compose down` / `docker compose up` cycles.
