---
title: "Environment Variables"
world_id: world-node
type: codex_entry
level: tier1
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
