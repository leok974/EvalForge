# Docker Compose Basics

Fill `docker-compose.yml` so it defines:

* service `db` using `postgres:16-alpine`
* named volume `db_data` mounted to `/var/lib/postgresql/data`
* service `api` with `depends_on: [db]`
* `api` env includes `DATABASE_URL` with host `db` (not localhost)
