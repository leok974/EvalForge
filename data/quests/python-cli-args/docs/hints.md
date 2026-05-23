# Hints: Robust CLI Args

## Hint 1 — Concept
Start by importing `argparse` and `sys`. You'll need `sys.exit()` to handle validation failures and exit with a non-zero code.

## Hint 2 — Guided
Use `action="store_true"` for the `--verbose` flag so it acts as a boolean. For `--count`, define it with `type=int` and a `default=1`.

## Hint 3 — The Solution
The `--help` flag is handled automatically by `argparse` as long as you've configured your parser correctly. Just run `python task.py --help` to see it in action!
