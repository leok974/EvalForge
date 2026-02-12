# Middleware

Middleware functions run before your final route handler. They are great for logging, auth, and parsing.

## Objective
Implement middleware functions that:
- log the request
- enforce an API key
- convert thrown errors into a 500 response

## Tasks
Implement functions in `middleware.js`:

1) `requestLogger(req, res, next)`
- `console.log` exactly: `${req.method} ${req.url}`
- then call `next()`

2) `authMiddleware(req, res, next)`
- read `req.headers["x-api-key"]`
- if it equals `"secret123"`, call `next()`
- otherwise: set `res.statusCode = 401`, call `res.end("Unauthorized")`, and DO NOT call `next()`

3) `errorMiddleware(err, req, res, next)`
- `console.log` the error message
- set `res.statusCode = 500`
- `res.end("Internal Server Error")`
- DO NOT call `next()` after ending the response

## Local Check
Run:
```bash
node app.js
```

Then:

* `curl -H "x-api-key: secret123" localhost:3000` → 200 `Hello Secure World`
* `curl localhost:3000` → 401 `Unauthorized`
* `curl -H "x-api-key: secret123" localhost:3000/error` → 500 `Internal Server Error`

## Success Criteria

Public tests pass.
