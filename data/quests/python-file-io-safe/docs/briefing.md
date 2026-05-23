# Briefing: Safe File I/O

## The Mission
Reading configuration files is a standard task, but in production, things go wrong. Files get deleted, permissions change, or the data itself is corrupted. A robust system must handle these "edge cases" without crashing.

Your mission is to build a safe configuration loader that reads `key=value` pairs from a text file and handles missing files gracefully.

## Objectives
- Implement `read_config(path_str)`:
  - If the file exists: Read its contents, find lines formatted as `key=value`, and return them as a dictionary.
  - If the file is missing: **Print 'CONFIG_MISSING'** and return an empty dictionary.
- Coercion:
  - Ensure keys and values are stripped of leading/trailing whitespace.
- Safety:
  - Your function should not raise a `FileNotFoundError` to the caller.

## Constraints
- Use the `pathlib` module for file path operations.
- Catch specifically `FileNotFoundError` rather than a generic `Exception`.
