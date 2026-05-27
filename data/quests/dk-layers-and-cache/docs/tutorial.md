# Docker Layer Caching

## How layers work

Each Dockerfile instruction creates a read-only layer. Docker caches the result:

```
Layer 1: FROM node:20-slim         (cached from registry pull)
Layer 2: WORKDIR /app              (cached — never changes)
Layer 3: COPY package.json .       (cached until package.json changes)
Layer 4: RUN npm install           (cached until layer 3 changes)
Layer 5: COPY . .                  (invalidated when ANY source file changes)
Layer 6: CMD ["node", "app.js"]    (metadata only)
```

When layer 5 is invalidated (you edit `app.js`), only layers 5 and 6 are rebuilt. Layers 3 and 4 stay cached, so `npm install` does not run again.

## Cache invalidation rule

A layer is invalidated if:
- The instruction text changed, OR
- Any file referenced by `COPY` or `ADD` changed, OR
- A parent layer was invalidated

## The pattern

```dockerfile
# Dependencies first
COPY package.json .
RUN npm install

# Source last (changes often)
COPY . .
```

This pattern applies equally to Python (`requirements.txt`), Ruby (`Gemfile`), and any package manager.
