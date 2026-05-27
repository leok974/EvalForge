## Concept
Use `isinstance(user.get('name'), str)` and `isinstance(user.get('age'), int)` to validate the inputs.

## Guided
Start by extracting the fields with `.get()`. If either is `None` or of the wrong type, raise `ValueError`. Then, return a new dictionary: `{"name": name.capitalize(), "age": age}`.

## Full Solution
```python
def process_user_data(user: dict) -> dict:
    name = user.get("name")
    age = user.get("age")
    
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    if not isinstance(age, int):
        raise ValueError("age must be an integer")
        
    return {
        "name": name.capitalize(),
        "age": age
    }
```
Observe how we validate both presence and type before doing any work.
