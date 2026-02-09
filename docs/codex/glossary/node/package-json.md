---
id: glossary/node/package-json
level: tier1
title: npm & package.json
type: codex_entry
world: node
world_id: world-node
---

# npm & package.json

npm is Node’s package manager. `package.json` is the project manifest:
- dependencies
- scripts
- metadata (including module type)

---

## The three commands you’ll use most

### Install dependencies
```bash
npm install
```

### Run scripts

```bash
npm run test
npm run dev
npm start
```

### Add a dependency

```bash
npm install express
npm install -D eslint
```

---

## package.json scripts

Example:

```json
{
  "scripts": {
    "test": "node --test",
    "start": "node server.js"
  }
}
```

Run them:

```bash
npm run test
npm start
```

---

## Dependencies vs devDependencies

* `dependencies`: needed at runtime
* `devDependencies`: needed for development/testing

In many quest workspaces, everything is local and minimal — follow the quest instructions.

---

## Versioning rule of thumb

If you want reproducibility, use a lockfile:

* `package-lock.json` (npm)

EvalForge environments usually install deterministically — don’t delete lockfiles unless instructed.

## Pitfalls

- Blocking the event loop with heavy synchronous operations.
- Unhandled promise rejections can crash the process.

## Related

- [[node/event-loop]]
- [[node/modules]]