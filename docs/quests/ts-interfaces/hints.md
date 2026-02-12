# Hints — TS Interfaces

## Hint 1
Use the `type` field to narrow:
`e.type === "user.login" || e.type === "user.logout"`

## Hint 2
Build the string incrementally:
start → append user → append ip

## Hint 3
Only append ip if it’s a non-empty string.
