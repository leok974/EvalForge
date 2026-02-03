# Middleware

Middleware functions run before your final route handler. They are great for logging, auth, and parsing.

## Goal
Implement functions in `middleware.js`:
1.  **requestLogger**: `console.log` the `${req.method} ${req.url}`. Call `next()`.
2.  **authMiddleware**: Check `req.headers['x-api-key']`.
    *   If it equals `"secret123"`, call `next()`.
    *   Otherwise, set `res.statusCode = 401`, call `res.end("Unauthorized")`, and **stop** (don't call next).

## Testing
`node app.js` runs the server.
- `curl -H "x-api-key: secret123" localhost:3000` -> 200 OK
- `curl localhost:3000` -> 401 Unauthorized
