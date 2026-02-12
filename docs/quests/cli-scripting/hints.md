# Hints — Bash Scripting

## Hint 1
Use `$1` to access the name argument.

## Hint 2
Check if `$1` is empty using `[ -z "$1" ]`.

## Hint 3 (Near-solution)
```sh
if [ -z "${1:-}" ]; then
  echo "Usage: task.sh <name>"
  exit 1
fi
echo "Hello, $1!"
```
