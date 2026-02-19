def process_user_data(user: dict) -> dict:
    """
    Take a user dict, validate fields, and return a sanitized dict.
    Required fields: 'name' (str), 'age' (int).
    If invalid, raise ValueError.
    """
    if not isinstance(user, dict):
        raise ValueError("Input must be a dict")
    
    name = user.get("name")
    age = user.get("age")

    if not isinstance(name, str) or not name:
        raise ValueError("Missing or invalid 'name'")
    
    if not isinstance(age, int) or age < 0:
        raise ValueError("Missing or invalid 'age'")

    return {
        "name": name.strip(),
        "age": age,
        "active": True # Default field
    }
