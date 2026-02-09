---
id: glossary/node/http-basics
level: tier1
title: HTTP Basics
type: codex_entry
world: node
world_id: world-node
---

# HTTP Basics

HTTP is request/response:
- client sends a request (method + path + headers + optional body)
- server responds (status code + headers + body)

---

## Methods (common)
- `GET`: fetch data
- `POST`: create
- `PUT/PATCH`: update
- `DELETE`: remove

---

## Status codes
- `200 OK` success
- `201 Created` created something
- `400 Bad Request` client error
- `401/403` auth errors
- `404 Not Found`
- `500` server error

---

## Node http server (minimal)

```js
import http from "node:http";

const server = http.createServer((req, res) => {
  if (req.url === "/health") {
    res.statusCode = 200;
    res.end("ok");
    return;
  }
  res.statusCode = 404;
  res.end("not found");
});

server.listen(3000);
```

---

## Body parsing (conceptual)

Raw `http` does not auto-parse JSON. Frameworks/middleware do.

In quests, you may:

* only need query/path handling
* or parse a simple JSON body

---

## EvalForge guidance

If tests check:

* exact status code
* exact response body
  match them exactly (no extra whitespace/logging).

## Pitfalls

- Blocking the event loop with heavy synchronous operations.
- Unhandled promise rejections can crash the process.

## Related

- [[node/event-loop]]
- [[node/modules]]