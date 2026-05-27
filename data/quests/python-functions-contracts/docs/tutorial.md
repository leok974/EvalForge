# Enforcing Data Contracts

Validating input is the first line of defense in automation.

### Checking Types
The `isinstance()` function is the standard way to check if a variable matches a type.

```python
val = "hello"
if not isinstance(val, str):
    raise ValueError("Expected a string")
```

### Checking Dictionary Keys
Using `in` is safer than direct access if you aren't sure a key exists.

```python
data = {"status": "ok"}
if "status" not in data:
    raise ValueError("Missing status")
```

### The "Fail Fast" Pattern
Don't wait until the end of the function to validate. Check each requirement at the top and raise exceptions immediately. This keeps your core logic clean and focused on valid data.

### Building the Return Dict

After validation, strip the name and include the required `"active"` field:

```python
return {
    "name": name.strip(),
    "age": age,
    "active": True,
}
```

`name.strip()` removes leading and trailing whitespace — `" Alice "` becomes `"Alice"`.

### Your Task
Implement the validation logic in `task.py`. Ensure you check the **existence**, **type**, and **value** (non-negative age) of each required field, then return all three keys.
