# world-node — Server Foundations (Student Guide)

Welcome to the Node.js world in [oaicite:0]{index=0}.

Node quests focus on **reliable server-side habits**:
- **Async correctness**: Handling promises and event loops correctly.
- **Environment configuration**: Reading config from env vars safely.
- **Resource management**: Opening/closing servers and file handles cleanly.
- **Testing**: Writing deterministic tests.

This guide helps you avoid common pitfalls like hanging tests, unhandled rejections, and "works on my machine" issues.

---

## How Node quests work (EvalForge style)

### What you edit
Each quest focuses on specific files in `workspace/`.
Common examples:
- `workspace/server.js` (or `index.js`)
- `workspace/lib/...`
- `workspace/test/...`

**Rule:** Only change what the quest tells you to change.

### What the grader checks
- **Correct Output/Behavior**: Does the server respond correctly? Are files written correctly?
- **Resource Cleanup**: Does the server stop when asked? Are handles closed?
- **Async Handling**: Are promises awaited? are errors caught?
- **Configuration**: Does it respect `PORT` and other env vars?

### Your job
Make the server/script:
- **stateless** (where pertinent)
- **configurable** via environment
- **robust** (error handling)
- **testable**

---

## The 80/20 Node mental model

### 1) The Event Loop is King
Node is single-threaded. Blocking the loop stops everything.
- **Don't block**: Use async I/O (`fs.promises`, `await`).
- **Scheduling**: Understand `process.nextTick`, `setImmediate`, and Promise microtasks.

### 2) Modules matter (ESM vs CJS)
Know which system you are in.
- **ESM (`import`)**: The modern standard. `package.json` usually has `"type": "module"`.
- **CJS (`require`)**: Legacy but common.
- **Don't mix dynamically**: Be consistent.

### 3) Configuration is external
Never hardcode secrets or ports.
- **Read**: `process.env.PORT`
- **Default**: `|| 3000`
- **Validate**: Ensure required vars exist.

### 4) Resources must be managed
In long-running processes (servers), leaks kill.
- **Close** servers on shutdown signals.
- **Close** file handles.
- **Clear** intervals/timeouts.

---

## Common pitfalls (and fixes)

### “Tests run but never finish”
You have an **open handle**.
- Did you call `server.close()`?
- Is a `setInterval` still ticking?
- Did an async operation fail to return/resolve?

### “UnhandledPromiseRejectionWarning”
You ignored a promise error.
- Use `try/catch` with `await`.
- Or `.catch()` chains.
- Never "fire and forget" critical logic without an error handler.

### “It works locally but fails in CI”
- **Binding**: Did you listen on `127.0.0.1` instead of `0.0.0.0`? (Docker needs `0.0.0.0`).
- **Paths**: Did you hardcode a Windows/Mac path? Use `path.join()`.
- **Env**: Did you assume an env var exists without checking?

### “Undefined is not a function” (Imports)
- You might be importing a named export as default (or vice versa).
- Check `module.exports = ...` vs `export default ...`.

---

## Debugging checklist

### 1) Check connection/ports
- Is the server actually listening?
- Is it on the right port?

### 2) Trace async flow
- Add logs *before* and *after* await calls.
- Ensure the promise actually settles.

### 3) Check Env Vars
- Log `process.env.MY_VAR` at startup (mask secrets!).
- Verify defaults are applying.

### 4) Verify Cleanup
- In tests, are you using `after()` or `teardown` hooks to close resources?

---

## Tiny patterns (copy/paste friendly)

### Robust Server Start
```javascript
const server = app.listen(PORT, '0.0.0.0', () => {
  console.log(`Listening on ${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  server.close(() => console.log('Process terminated'));
});
```

### Safe Async Wrapper
```javascript
const safeAsync = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};
```

### Reading Config
```javascript
const config = {
  port: parseInt(process.env.PORT, 10) || 3000,
  dbUrl: process.env.DATABASE_URL || exit('Missing DATABASE_URL'),
};
```

---

## Where the Codex fits
Stuck on **streams**, **http**, or **modules**?
Open `docs/codex/world-node/README.md`.

---

## Next Steps
After mastering Node, you're ready for:
1. **world-infra**: Dockerizing these Node apps.
2. **world-sql**: Connecting them to real databases.
