# HTTP Server (No Framework)

Build a raw HTTP server without Express/Koa/Fastify.

## Objective
Implement simple routing rules in `server.js`.

## Routes
Update `server.js` to handle:

1) `GET /` → `200` text/plain `Hello World`
2) `GET /api` → `200` application/json `{ "message": "Hello API" }`
3) `GET /error` → `500` text/plain (body can be empty or message)
4) All other routes → `404` text/plain (body can be empty or message)

## Constraints
- Only implement routing using `req.method` and `req.url`
- Use `res.statusCode` and `res.setHeader`
- No frameworks
- Deterministic output

## Success Criteria
Public tests pass.
