# Hints: Multi-Stage Builds

**Hint 1** — Add `AS builder` to the first FROM line: `FROM node:18 AS builder`

**Hint 2** — The second FROM should use a slim image to keep the runtime small: `FROM node:18-slim`

**Hint 3** — Copy artefacts from the builder stage using the `--from` flag:
```dockerfile
COPY --from=builder /app/dist ./dist
```

**Hint 4** — The runtime stage only needs what's required to *run* the app — not to build it. Don't copy source files or dev dependencies.
