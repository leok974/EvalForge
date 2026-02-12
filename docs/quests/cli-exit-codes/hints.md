# Hints — Exit Codes

## Hint 1
Use `if [ -f "fixtures/error.flag" ]; then ... fi`.

## Hint 2
Remember to `exit 1` inside the if block.

## Hint 3 (Near-solution)
```sh
if [ -f "fixtures/error.flag" ]; then
  exit 1
fi
exit 0
```
