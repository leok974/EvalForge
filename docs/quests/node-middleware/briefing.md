# Briefing — node-middleware

## Objective
Implement a middleware pipeline that:
- logs requests
- blocks unauthorized calls
- converts errors into a 500 response

## Contract
- Logger prints: `METHOD URL`
- Auth requires `x-api-key: secret123` or returns 401 Unauthorized
- Errors become: 500 Internal Server Error

## Success Criteria
Public tests pass.
