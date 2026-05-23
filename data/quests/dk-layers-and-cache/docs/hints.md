# Hints

## Hint 1 — The bug

The `COPY . .` is in the wrong place. It should come AFTER `npm install`, not before.

## Hint 2 — Correct order

```dockerfile
COPY package.json .
RUN npm install
COPY . .
```

Copy only `package.json` first, run the install, then copy everything else.

## Hint 3 — Complete solution

```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD ["node", "app.js"]
```
