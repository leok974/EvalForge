# HTTP Server

Build a raw HTTP server without frameworks.

## Goals
Update `server.js` to handle:
1.  `GET /` returns 200 "Hello World"
2.  `GET /api` returns 200 JSON `{ "message": "Hello API" }`
3.  `GET /error` returns 500
4.  All other routes return 404

## Hint
Use `req.url` and `req.method`.
Set headers using `res.setHeader("Content-Type", ...)`
Set status using `res.statusCode = ...`
