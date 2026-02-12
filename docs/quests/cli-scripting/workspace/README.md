# Bash Scripting

Edit `task.sh` to accept arguments and output an exact format.

## Rules
- Accept a name as the first argument.
- If missing OR whitespace-only:
  - Print `Usage: task.sh <name>`
  - Exit `1`
- Otherwise:
  - Print `Hello, <name>!`
  - Exit `0`
- Output must be exact (single line). No extra logging.
