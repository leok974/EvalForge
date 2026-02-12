# Hints — node-deploy-basics

## Hint 1
Port default pattern:
`const PORT = process.env.PORT ? Number(process.env.PORT) : 3000`

## Hint 2
Health route:
- set `res.statusCode = 200`
- `res.end("OK")`
