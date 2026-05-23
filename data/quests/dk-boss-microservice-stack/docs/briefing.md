# Boss: Microservice Stack

This is the final challenge for the Docker Systems track.

You have a stub Compose file with just an `api` and `db`. Your mission is to build a production-ready three-tier stack from it.

## Architecture Target

```
Internet → nginx (port 80) → api (port 5000) → db (Postgres)
```

## Requirements

| Requirement | Detail |
|---|---|
| nginx service | Reverse proxy on port 80; proxies to api |
| Named network | All three services on a shared network |
| Named volume | `db_data` mounted at `/var/lib/postgresql/data` |
| db healthcheck | `pg_isready -U postgres` |
| api healthcheck | `curl -f http://localhost:5000/health` |
| Restart policies | `unless-stopped` on all services |
| depends_on chain | nginx waits for api healthy; api waits for db healthy |

The grader validates the `compose.yaml` structure. Get all 7 objectives green to complete the boss.
