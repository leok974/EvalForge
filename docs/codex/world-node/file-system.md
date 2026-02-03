---
title: "File System (fs)"
world_id: world-node
type: codex_entry
level: tier1
---

# File System (fs)

Node’s `fs` module lets you read and write files. In quests, you’ll often:
- read fixture files
- write outputs to a required path
- ensure directories exist

---

## Sync vs async APIs

Sync (simple, fine for small fixtures):
```js
import fs from "node:fs";

const text = fs.readFileSync("fixtures/input.txt", "utf8");
fs.writeFileSync("outputs/result.txt", text);
```

Async (non-blocking):

```js
import { promises as fsp } from "node:fs";

const text = await fsp.readFile("fixtures/input.txt", "utf8");
await fsp.writeFile("outputs/result.txt", text);
```

---

## Directories

Create dirs before writing files:

```js
import fs from "node:fs";
fs.mkdirSync("outputs", { recursive: true });
```

---

## Paths

Prefer `path.join` for portability:

```js
import path from "node:path";
const p = path.join("outputs", "result.txt");
```

---

## Common pitfalls

* forgetting encoding (`utf8`) → you get a Buffer
* writing to wrong relative path (cwd matters)
* not creating directories

---

## EvalForge guidance

Most quests run from a workspace root directory.
Assume relative paths are from that root unless stated otherwise.
