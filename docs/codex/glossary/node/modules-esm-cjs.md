---
id: glossary/node/modules-esm-cjs
level: tier1
title: Modules (ESM vs CommonJS)
type: codex_entry
world: node
world_id: world-node
---

# Modules (ESM vs CommonJS)

Node has two module systems:

- **CommonJS (CJS)**: `require(...)`, `module.exports = ...`
- **ES Modules (ESM)**: `import ... from`, `export ...`

Mixing them incorrectly is a top cause of “it runs but tests fail”.

---

## CommonJS (default in older Node)

```js
// add.js
function add(a, b) { return a + b; }
module.exports = { add };

// main.js
const { add } = require("./add");
console.log(add(1, 2));
```

---

## ES Modules (modern)

```js
// add.js
export function add(a, b) { return a + b; }

// main.js
import { add } from "./add.js";
console.log(add(1, 2));
```

---

## How Node decides ESM vs CJS

Node treats a file as ESM if:

* it ends in `.mjs`, OR
* `package.json` has `"type": "module"`

Node treats a file as CJS if:

* it ends in `.cjs`, OR
* default `.js` behavior when `"type"` not set

---

## Common error messages

### “Cannot use import statement outside a module”

You used `import` but Node thinks the file is CJS.

Fix:

* add `"type": "module"` in package.json **or**
* rename file to `.mjs`

### “require is not defined in ES module scope”

You used `require` but Node thinks it’s ESM.

Fix:

* use `import`, or switch the file to `.cjs`

---

## Path gotcha in ESM

In ESM you don’t get `__dirname` by default.

Pattern:

```js
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
```

---

## EvalForge guidance

In quests, follow the existing project convention:

* if tests use `import`, stay ESM
* if tests use `require`, stay CJS

Don’t change module type unless the quest explicitly asks.

## Pitfalls

- Blocking the event loop with heavy synchronous operations.
- Unhandled promise rejections can crash the process.

## Related

- [[node/event-loop]]
- [[node/modules]]