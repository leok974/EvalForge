# Tutorial — Bash Scripting

## Arguments
- `$1`: The first argument passed to the script.
- `$#`: The number of arguments passed.

## Conditional Checks
Check if a variable is empty:
```sh
if [ -z "$1" ]; then
  echo "Missing argument"
  exit 1
fi
```

## Printing
`echo` prints to stdout by default.
