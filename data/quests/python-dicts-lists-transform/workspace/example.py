def transform_inventory(items: list[dict]) -> dict[str, int]:
    """Sum quantities by category using a dict comprehension."""
    categories = {item["category"] for item in items}
    return {cat: sum(i["qty"] for i in items if i["category"] == cat) for cat in categories}
