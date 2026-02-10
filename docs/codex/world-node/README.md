---
title: "World Node — Codex"
world_id: world-node
type: codex_landing
version: 1
---

# World Node — Codex (Server Foundations)

This Codex is your **reference hub** for Node.js in EvalForge.  
Node quests are about building reliable server-side habits: async correctness, environment configuration, file I/O, HTTP handling, testing, and production readiness.

If you ever get stuck, this page is your **map + debugger**.

---

## How to use this Codex

- **Learning mode:** skim “Core Model” once, then follow the Quest Map in order.
- **Stuck mode:** jump to the concept you’re using (env vars, modules, HTTP, middleware).
- **Debug mode:** use the Diagnostics Checklist (it covers the most common Node failure modes).

> Rule of thumb: If code “runs” but tests fail, it’s usually **async timing**, **wrong module type**, **env var behavior**, or **not closing resources**.

---

## The Core Model (the 80/20)

### 1) Node runs on an event loop
Node is single-threaded for JS execution; it handles I/O by scheduling work and running callbacks/promises later.
- Learn when work happens “now” vs “later”.
- Learn how async flows affect tests.

Read: **[event-loop](./event-loop.md)**

### 2) Modules define how code loads
In Node you’ll encounter:
- CommonJS (`require`, `module.exports`)
- ESM (`import`, `export`)
Tests and tooling can break if you mix these incorrectly.

Read: **[modules](./modules.md)**

### 3) Configuration comes from environment
In production, you don’t hardcode ports/secrets. You read env vars and provide safe defaults.
Read: **[env-vars](./env-vars.md)**

### 4) Servers are I/O pipelines
Requests flow through handlers/middleware; errors must be handled intentionally.
Read: **[http-basics](./http-basics.md)** and **[middleware](./middleware.md)**

### 5) Testing is your contract
Node quests should be:
- deterministic
- resource-clean (no hanging handles)
- explicit about inputs/outputs

Read: **[node-test](./node-test.md)**

---

## Quick Links (most-used concepts)

### Runtime & async
- **[event-loop](./event-loop.md)** — what runs when, why timers/promises behave differently
- **[async-await](./async-await.md)** — promises, awaiting, concurrency patterns

### Loading & packaging
- **[modules](./modules.md)** — ESM vs CJS, import/export vs require
- **[npm](./npm.md)** — package.json scripts, dependencies, version habits

### I/O & servers
- **[file-system](./file-system.md)** — read/write files, paths, safe defaults
- **[http-basics](./http-basics.md)** — request/response, routing, status codes
- **[middleware](./middleware.md)** — pipeline mental model (auth/logging/validation)

### Correctness & reliability
- **[error-handling](./error-handling.md)** — sync vs async errors, safe patterns
- **[observability](./observability.md)** — logs/metrics/tracing basics (what to instrument first)

### Production basics
- **[deploy-basics](./deploy-basics.md)** — PORT, npm start, health checks, “works locally” pitfalls

---

## Node Quest Map (by concept)

> This maps typical Tier-1 Node quests to the concepts you’ll use.

### Boot + runtime fundamentals
- **node-ignition** → modules + npm + “what runs where”  
  Read: [modules](./modules.md), [npm](./npm.md)

### Modules & packages
- **node-modules** → export/import, “type”: module, path resolution  
  Read: [modules](./modules.md)
- **node-npm** → scripts, dependencies, running tasks  
  Read: [npm](./npm.md)

### Configuration
- **node-env** → PORT defaults, MODE flags, config output  
  Read: [env-vars](./env-vars.md)

### Async patterns
- **node-async** → async/await, promise control flow  
  Read: [async-await](./async-await.md), [event-loop](./event-loop.md)

### File system
- **node-fs** → reading fixtures, writing outputs, safe paths  
  Read: [file-system](./file-system.md)

### HTTP & middleware
- **node-http** → handlers, status codes, request parsing  
  Read: [http-basics](./http-basics.md)
- **node-middleware** → auth/logging pipeline patterns  
  Read: [middleware](./middleware.md), [error-handling](./error-handling.md)

### Testing
- **node-testing** → node:test patterns, deterministic tests, cleanup  
  Read: [node-test](./node-test.md), [async-await](./async-await.md)

### Deploy readiness
- **node-deploy-basics** → npm start, PORT, health checks, logs  
  Read: [deploy-basics](./deploy-basics.md), [observability](./observability.md)

---

## Common Pitfalls (and fixes)

### A) “Tests hang forever”
Usually means an open handle:
- server still listening
- timer still running
- file handle not closed
Fix:
- close servers in teardown
- clear timers
- await async work
Read: [node-test](./node-test.md), [event-loop](./event-loop.md)

### B) “It works locally but fails in Docker/CI”
Common causes:
- binding to localhost only (not 0.0.0.0 when needed)
- missing env vars / wrong defaults
- path assumptions (`C:\...` style)
Read: [env-vars](./env-vars.md), [deploy-basics](./deploy-basics.md)

### C) “Syntax error: Cannot use import statement outside a module”
You’re mixing ESM/CJS, or package.json `"type"` is wrong.
Read: [modules](./modules.md)

### D) “UnhandledPromiseRejection” / silent async failures
You didn’t await a promise or forgot try/catch around awaited calls.
Read: [async-await](./async-await.md), [error-handling](./error-handling.md)

### E) “My middleware doesn’t run / order is wrong”
Middleware is order-dependent; early returns skip later steps.
Read: [middleware](./middleware.md)

---

## Diagnostics Checklist (when tests fail)

### 1) Module sanity
- Are you using ESM or CJS consistently?
- Does package.json declare `"type": "module"` if using ESM?
- Are imports pointing to correct paths?

### 2) Async correctness
- Did you `await` everything you should?
- Are you returning promises from functions that tests expect?
- Are you accidentally firing-and-forgetting?

### 3) Resource cleanup
- Any server still listening?
- Any timers still active?
- Any file streams left open?

### 4) Environment config
- Do env vars have safe defaults?
- Are you reading `PORT` and using it?
- Are empty strings treated as missing where required?

### 5) HTTP behavior
- Correct status codes?
- Correct headers/body shape?
- Correct route handling?

### 6) Observability
- Are logs clear enough to see which branch ran?
- Are errors surfaced (not swallowed)?

---

## Tiny Patterns (copy/paste friendly)

### Read env vars with defaults (and empty-safe)
```js
const MODE = process.env.MODE?.trim() || "dev";
const PORT = Number(process.env.PORT?.trim() || "3000");
```

### Minimal node:test pattern

```js
import test from "node:test";
import assert from "node:assert/strict";

test("works", () => {
  assert.equal(1 + 1, 2);
});
```

### Safe async test

```js
test("async works", async () => {
  const value = await Promise.resolve(42);
  assert.equal(value, 42);
});
```

### Basic HTTP server pattern (close it!)

```js
import http from "node:http";

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.end("ok");
});

server.listen(0, () => {
  // server.address().port is chosen automatically
});

// later: server.close()
```

### Middleware mental model (pipeline)

* validate → auth → handler → error mapping
  Read: [middleware](./middleware.md), [error-handling](./error-handling.md)

---

## Next expansions (future-proof hooks)

Tier-2 Node can add:

* streaming and backpressure
* AbortController for fetch
* robust logging formats (JSON logs)
* metrics basics (counters/timers)
* deployment concepts (Docker, reverse proxy, health checks)

But Tier-1 should master: **modules + env + async + fs + HTTP + tests**.

---

### Tip: Use Codex while solving

If you’re stuck, open the concept page, copy the tiny pattern, then adapt it to the quest contract.


## Pitfalls

- Blocking the event loop with heavy synchronous operations.
- Unhandled promise rejections can crash the process.

## Related

- [[node/event-loop]]
- [[node/modules]]