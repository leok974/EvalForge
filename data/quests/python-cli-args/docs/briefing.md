# Briefing: Robust CLI Args

## The Mission
CLI tools are the backbone of automation. However, a tool that is hard to use or lacks proper "help" documentation is a liability. Your team needs a standard template for building robust Python search utilities.

Your mission is to implement a command-line interface using the `argparse` module that supports core configuration flags.

## Objectives
- Use `argparse` to handle the following arguments:
  - `--verbose` (Optional Flag): If present, the tool should output extra debug information.
  - `--count` (Optional Integer): The number of items to process. Default to `1`.
- Validation:
  - If `--count` is less than `0`, print an error message and exit with code `1`.
- Help:
  - Ensure that running the script with `--help` prints the standard auto-generated usage message.

## Output Contract

| Scenario | Output |
|---|---|
| No arguments | prints `Hello World` once to stdout |
| `--count 3` | prints `Hello World` three times to stdout |
| `--verbose --count 2` | prints `Processing 1/2...` then `Hello World`, then `Processing 2/2...` then `Hello World` |
| `--count -1` | prints `Count cannot be negative` to **stderr**, exits with code `1` |
| `--help` | prints auto-generated usage to stdout, exits with code `0` |

The error message must go to **stderr** (use `print(..., file=sys.stderr)`).

## Constraints
- Do not manually parse `sys.argv`. Use the `argparse` library.
- The entrypoint must be structured correctly with an `if __name__ == "__main__":` block.
