---
id: glossary/node/env-and-config
level: tier1
title: Environment Variables
type: codex_entry
world: node
world_id: world-node
---

# Environment Variables

Environment variables are the standard way to configure Node apps without hardcoding values.

Use cases:
- `PORT`
- `MODE` / `NODE_ENV`
- API keys (never commit these)

---

## Reading env vars
```js
const MODE = process.env.MODE || "dev";
const PORT = Number(process.env.PORT || "3000");
```

### Empty string gotcha

In some quests, empty should behave like “missing”.

Pattern:

```js
const raw = (process.env.MODE || "").trim();
const MODE = raw ? raw : "dev";
```

---

## Setting env vars

### Linux/macOS

```bash
MODE=prod PORT=8080 node server.js
```

### Windows PowerShell

```powershell
$env:MODE="prod"; $env:PORT="8080"; node server.js
```

---

## Production contract (common)

* bind to `PORT` if provided
* default to 3000 (or quest-defined default)
* never crash on missing optional vars

---

## EvalForge guidance

If a quest checks output files for config:

* match the exact format
* treat unset/empty as specified
* don’t print extra logs unless asked

## Pitfalls

- Blocking the event loop with heavy synchronous operations.
- Unhandled promise rejections can crash the process.

## Related

- [[node/event-loop]]
- [[node/modules]]