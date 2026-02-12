# Tutorial — Exit Codes

## Concepts
- **Exit Code 0**: Success.
- **Exit Code 1-255**: Failure.
- **Silence**: Automation tools often rely on silent success.

## Checking for file existence
`test -f` or `[ -f ... ]` checks if a file exists.

Example:
```sh
if [ -f "some/file" ]; then
  exit 1
fi
exit 0
```
