---
id: glossary/node/deploy-basics
level: tier1
title: Deploy Basics
type: codex_entry
world: node
world_id: world-node
---

# Deploy Basics

Deploying a Node app means:
- it starts reliably
- it listens on the right port
- it has a health check
- logs explain failures
- configuration comes from env vars

---

## The PORT contract
Most platforms (Docker, Render, Heroku-style) set `PORT`. Your app must use it.

Pattern:
```js
const port = Number(process.env.PORT || "3000");
server.listen(port);
```

---

## “npm start” contract

Production often runs:

```bash
npm start
```

So package.json should define:

```json
{ "scripts": { "start": "node server.js" } }
```

---

## Health checks

A minimal health endpoint:

* returns 200
* returns quickly
* no DB calls unless required

Example:

* `GET /health` → `ok`

---

## Common pitfalls

* binding to the wrong interface
* crashing on missing env vars
* no logs → impossible debugging
* server starts but never responds

---

## EvalForge guidance

Quests often simulate “production readiness” with:

* env vars
* health endpoints
* deterministic startup behavior
  Match the quest contract exactly.

## Pitfalls

- Blocking the event loop with heavy synchronous operations.
- Unhandled promise rejections can crash the process.

## Related

- [[node/event-loop]]
- [[node/modules]]