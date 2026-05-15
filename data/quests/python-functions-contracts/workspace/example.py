def process_user_data(user: dict) -> dict:
    """Validate and sanitize a user dict."""
    if not isinstance(user.get("name"), str):
        raise ValueError("name must be a string")
    if not isinstance(user.get("age"), int):
        raise ValueError("age must be an integer")
    return {"name": user["name"].strip(), "age": user["age"]}
