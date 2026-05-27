## Concept
Use `isinstance(user.get('name'), str)` and `isinstance(user.get('age'), int)` to validate the inputs. Also check that `age >= 0`.

## Guided
Extract each field with `.get()`. If either is `None`, the wrong type, or `age` is negative, raise `ValueError`. Then strip the name and build the return dict.

## Full Solution
```python
def process_user_data(user: dict) -> dict:
    name = user.get("name")
    age = user.get("age")

    if not isinstance(name, str) or not name:
        raise ValueError("Missing or invalid 'name'")
    if not isinstance(age, int) or age < 0:
        raise ValueError("Missing or invalid 'age'")

    return {
        "name": name.strip(),
        "age": age,
        "active": True,
    }
```

Note: `name.strip()` removes whitespace — `" Alice "` becomes `"Alice"`. The `"active": True` field is always included in the returned dict.
