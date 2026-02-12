# Hints — node-middleware

## Hint 1
Logger must output exactly:
`GET /`

## Hint 2
Auth should stop the chain:
return after `res.end("Unauthorized")`

## Hint 3
For error middleware:
use `err.message` (not the whole Error object)
