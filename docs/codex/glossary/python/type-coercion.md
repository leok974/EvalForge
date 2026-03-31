---
id: glossary/python/type-coercion
title: Type Coercion
world: python
level: beginner
tags: [typing, logic, validation]
related:
  - codex:glossary/python/isinstance
  - codex:glossary/python/normalization
---

## Definition
**Type Coercion** (or Type Casting) is the process of converting a value from one data type to another (e.g., converting a numerical string `"123"` into an integer `123`).

## Usage in Systems
When ingesting data from JSON, CSVs, or CLI arguments, values often arrive as strings even if they represent numbers, booleans, or lists. Coercion is the first line of defense in a **normalization pipeline**.

### Common Coercions
- **Boolean Coercion**: Handling "truthy" strings.
  ```python
  def to_bool(val: str) -> bool:
      return str(val).lower() in ("true", "1", "yes", "on")
  ```
- **Numerical Coercion**: Handling user input.
  ```python
  try:
      count = int(raw_input)
  except ValueError:
      count = 0
  ```

## Best Practices
- **Fail Early**: If a value cannot be coerced (e.g., `"abc"` to `int`), raise an exception or default to a safe value (like `None` or `0`).
- **Use isinstance**: Check the type before attempting expensive coercion.
- **Strip Whitespace**: Always `.strip()` strings before casting to avoid `ValueError`.

## Related
- **isinstance**: used to check current types before coercing.
- **Normalization**: the broader process where coercion is a key step.
