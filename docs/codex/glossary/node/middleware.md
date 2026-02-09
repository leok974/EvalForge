---
id: glossary/node/middleware
level: tier1
title: Middleware
type: codex_entry
world: node
world_id: world-node
---

# Middleware

Middleware is a **pipeline** of functions that run in order for a request.

Mental model:
> request → [log] → [auth] → [validate] → [handler] → response

Middleware is order-dependent: earlier steps can block later steps.

---

## Why it matters
Middleware is how you build:
- logging
- authentication
- request validation
- error mapping

---

## Minimal pseudo-pattern
Frameworks differ, but the idea is consistent:

```js
function log(req, next) { next(); }
function auth(req, next) { next(); }
function handler(req) { return "ok"; }
```

---

## Common pitfalls

* forgetting to call `next()` (pipeline stops)
* returning early without a response
* putting auth after handler (too late)

---

## Error handling in middleware

Good systems catch errors and map them to responses:

* 400 for validation
* 401/403 for auth
* 500 for unexpected

See: [error-handling](./error-handling.md)

## Pitfalls

- Blocking the event loop with heavy synchronous operations.
- Unhandled promise rejections can crash the process.

## Related

- [[node/event-loop]]
- [[node/modules]]