# Tutorial — node-http

## What You’re Practicing
- raw Node HTTP routing via `req.method` and `req.url`
- setting status codes and headers correctly
- returning JSON safely

## Implementation Plan
1. Ensure you only handle `GET` requests (everything else can be 404).
2. Route by `req.url`:
   - `/` → text/plain + "Hello World"
   - `/api` → application/json + JSON.stringify({ message: "Hello API" })
   - `/error` → status 500
   - default → 404
3. Call `res.end(body)` exactly once.

## Pitfalls
- forgetting `Content-Type`
- calling `res.end()` before writing body
- returning JSON without `JSON.stringify`
