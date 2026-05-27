# Hints: Safe File I/O

## Hint 1 — Concept
Use `Path(path_str).exists()` or a `try-except FileNotFoundError` block. The briefing specifically asks for a print statement (`'CONFIG_MISSING'`) if the file is gone.

## Hint 2 — Guided
When reading lines, skip empty lines or lines that don't contain an `=`. Use `strip()` to clean up whitespace around keys and values.

## Hint 3 — The Solution
Use `line.strip().split("=", 1)` to handle cases where a value might contain an `=` sign. This ensures you only split on the first occurrence.
