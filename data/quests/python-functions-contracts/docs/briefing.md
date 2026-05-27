# Mission: Function Contracts (Core)

In any robust pipeline, functions act as a "contract." They promise to return a specific output IF the input meets certain criteria. If the input is garbage, the function should fail fast and loudly rather than propagating bad data.

### The Sanitization Problem
You are building an intake gate for a user database. Data arrives as raw dictionaries. If a mandatory field like `name` is missing or `age` is not a number, your pipeline will crash later on. You need to enforce a strict contract at the entry point.

### Your Objective
Implement `process_user_data` in `task.py`.

Your code must:
1. Verify that `name` exists and is a string. Raise `ValueError` if not.
2. Verify that `age` exists, is an integer, and is **non-negative** (`age >= 0`). Raise `ValueError` if not.
3. Return a clean dictionary with exactly **three** fields:
   - `"name"`: the name string **stripped** of leading/trailing whitespace
   - `"age"`: the age integer unchanged
   - `"active"`: always `True`
4. Raise a `ValueError` with a descriptive message if any contract is violated.

### Example

```python
process_user_data({"name": " Alice ", "age": 30})
# → {"name": "Alice", "age": 30, "active": True}

process_user_data({"name": "Bob", "age": -5})
# → raises ValueError

process_user_data({"age": 30})
# → raises ValueError  (missing name)
```
