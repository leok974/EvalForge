# world-infra — Toolchain Foundations (Student Guide)

Infra is about building confidence that your software runs the same way:
- on your machine
- in CI
- in production

The goal of this world is not “memorize Docker commands.”
It’s: **stop guessing** and learn a reliable debugging loop.

---

## The mental model you need

### Build vs Run
- Build → produces an image (template)
- Run → starts a container (a process with config)

### Host vs Container
“localhost” is contextual:
- inside a container, `localhost` means the container itself
- to reach another service, you use its service name on the shared network

### Ports
If a process listens on 8000 *inside* a container, you still may need:
- `-p 8000:8000` (host mapping)
- or a reverse proxy to route traffic

---

## Safe workflow (recommended)

1) Start with one service, get it healthy.
2) Add one dependency (DB, cache), validate.
3) Add a reverse proxy only after services are stable.
4) Lock config defaults + add health checks.

---

## Common pitfalls (and fixes)

### “Connection refused”
Usually means:
- process isn’t running, or
- service is listening on a different port/interface, or
- you’re hitting host localhost from inside a container

Fix: check listening ports and mappings.

### “Works locally but not in CI”
Usually means:
- missing env vars
- reliance on local files not present in CI
- timing/health readiness

Fix: add readiness checks and fail fast on missing config.

### “My data disappeared”
You used an ephemeral container filesystem.
Fix: volumes.

---

## Debug loop (copy/paste mindset)

1) Identify the environment (host vs container)
2) Confirm process is running
3) Confirm port is listening
4) Confirm network + routing
5) Confirm config
6) Confirm readiness
7) Read logs around the error

Open the Codex hub:
`docs/codex/world-infra/README.md`
