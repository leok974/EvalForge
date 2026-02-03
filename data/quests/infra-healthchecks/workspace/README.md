# Healthchecks & Readiness

Implement `/health` and `/ready` in `server.js`:

* `/health` → `200 ok`
* `/ready` → `200 ready` only if `fixtures/ready.flag` exists, else `503 not_ready`
* On start, print `PORT <port>`
