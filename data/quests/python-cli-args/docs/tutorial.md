# Tutorial: Robust CLI with argparse

The `argparse` module makes it easy to write user-friendly command-line interfaces. The program defines what arguments it requires, and `argparse` will figure out how to parse those out of `sys.argv`.

## Creating a Parser
Start by creating a `ArgumentParser` object.

```python
import argparse

parser = argparse.ArgumentParser(description="My Cool Tool")
```

## Adding Arguments
You can add positional arguments or optional flags.

```python
# A flag (boolean)
parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")

# An optional integer argument
parser.add_argument("--count", type=int, default=1, help="Number of items")
```

## Parsing
Call `parse_args()` to get an object containing the argument values.

```python
args = parser.parse_args()

if args.verbose:
    print("Debug: Verbose mode ON")
```

## Handling Errors
If an argument is invalid (e.g., a string passed to an integer field), `argparse` automatically prints an error and exits. However, for custom logic (like checking if a number is positive), you must handle it manually.

```python
if args.count < 0:
    print("Error: Count cannot be negative")
    sys.exit(1)
```
