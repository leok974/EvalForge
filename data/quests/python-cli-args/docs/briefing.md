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

## Constraints
- Do not manually parse `sys.argv`. Use the `argparse` library.
- The entrypoint must be structured correctly with an `if __name__ == "__main__":` block.
