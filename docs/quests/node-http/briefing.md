# Briefing — node-http

## Objective
Implement a framework-free HTTP server with correct routing and status codes.

## Contract
- `GET /` → 200 + `Hello World`
- `GET /api` → 200 + JSON `{ "message": "Hello API" }`
- `GET /error` → 500
- everything else → 404

## Success Criteria
Public tests pass.
