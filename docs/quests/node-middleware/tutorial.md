# Tutorial — node-middleware

## What You’re Practicing
- middleware control flow via `next()`
- stopping the chain safely (don’t call next after ending a response)
- translating errors into consistent HTTP responses

## Implementation Plan
1. `requestLogger`
   - log `${req.method} ${req.url}`
   - call `next()`

2. `authMiddleware`
   - read `req.headers["x-api-key"]`
   - if valid → `next()`
   - if invalid → set `res.statusCode = 401` and `res.end("Unauthorized")`

3. `errorMiddleware`
   - log the error message
   - set `res.statusCode = 500`
   - `res.end("Internal Server Error")`

## Pitfalls
- calling `next()` after you already ended the response
- logging extra text (tests expect exact format)
- forgetting header key is lowercase in Node (`x-api-key`)
