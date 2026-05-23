# Layers and Cache

Docker builds images in **layers**. Each instruction in a Dockerfile creates a new layer. Docker caches each layer — if the inputs to a layer haven't changed, Docker reuses the cached result instead of rebuilding it.

## The Problem with the Starter

The current Dockerfile does this:
```dockerfile
COPY . .          # copies ALL source files
COPY package.json .
RUN npm install
```

Every time you change `app.js`, Docker invalidates the `COPY . .` layer — which means `npm install` also re-runs, even though `package.json` hasn't changed. On a real project this wastes minutes per build.

## The Fix

Separate dependency installation from source copy:
1. Copy only `package.json` first
2. Run `npm install` (cached as long as `package.json` doesn't change)
3. Copy the rest of the source

Your task: fix the Dockerfile so `package.json` is copied and `npm install` runs **before** `COPY . .`.
