# Hints — Environment Variables

## Hint 1
Look up POSIX shell “parameter expansion” for default values.

## Hint 2
Write two lines with:
- `>` then `>>`

## Hint 3 (Near-solution)
```

mode="${MODE:-dev}"
port="${PORT:-3000}"

```
Then write:
- `MODE=$mode`
- `PORT=$port`
