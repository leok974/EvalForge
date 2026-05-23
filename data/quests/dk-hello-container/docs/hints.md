# Hints

## Hint 1 — FROM syntax

Every Dockerfile starts with `FROM`. The format is `FROM <image>:<tag>`. Try:
```
FROM alpine:3.18
```

## Hint 2 — CMD forms

There are two ways to write CMD. The exec form uses a JSON array:
```
CMD ["executable", "arg1", "arg2"]
```
The shell form is just a string. Prefer the exec form.

## Hint 3 — Full structure

Your complete Dockerfile needs exactly two lines:
```dockerfile
FROM alpine:3.18
CMD ["echo", "Hello from inside the container"]
```
