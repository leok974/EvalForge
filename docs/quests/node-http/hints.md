# Hints — node-http

## Hint 1
Check both method and path:
`if (req.method !== "GET") { ... }`

## Hint 2
For JSON:
`res.setHeader("Content-Type", "application/json")`
and
`res.end(JSON.stringify({ message: "Hello API" }))`
