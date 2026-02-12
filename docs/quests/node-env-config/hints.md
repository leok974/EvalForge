# Hints — node-env-config

## Hint 1
`process.env.PORT` is a string. Convert it with `Number()`.

## Hint 2
Treat `""` the same as missing:
`if (!raw || !raw.trim()) ...`
