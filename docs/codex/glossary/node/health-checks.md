---
id: glossary/node/health-checks
title: Health Checks
world: node
level: beginner
tags: [devops, monitoring, apis]
related:
  - codex:glossary/node/lockfiles
  - codex:glossary/web/html/debug-validate
  - codex:glossary/web/html/metadata-seo
---

# Health Checks

## Definition
Health checks are lightweight endpoints that report whether a service is alive and ready. "Liveness" means the process is running; "readiness" means it can actually serve traffic (DB reachable, migrations complete, deps OK).

## Usage
- Expose `/healthz` (liveness) and `/ready` (readiness).
- Used by reverse proxies, load balancers, containers, and monitors.
- Helps prevent routing traffic to broken instances.

## Example
```js
import express from "express";
const app = express();

app.get("/healthz", (_req, res) => res.status(200).send("ok"));
app.get("/ready", async (_req, res) => {
  // await db.ping()
  res.status(200).json({ ready: true });
});

app.listen(8000);
```

## Pitfalls

* Returning 200 from readiness when DB is down causes "healthy but broken" routing.
* Health checks must be fast; don't do heavy queries.

## Related

* Lockfiles: both are part of production readiness.
* Debug Validate: validation catches errors before deploy.
* Metadata Seo: both involve HTTP responses and standards.