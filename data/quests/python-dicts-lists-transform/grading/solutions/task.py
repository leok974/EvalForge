def transform_inventory(items: list[dict]) -> dict[str, int]:
    """
    Input: [{'category': 'A', 'qty': 5}, {'category': 'A', 'qty': 2}, ...]
    Output: {'A': 7, ...} (Sum qty by category)
    Must use comprehensions or functional style.
    """
    categories = {item['category'] for item in items}
    return {
        cat: sum(item['qty'] for item in items if item['category'] == cat)
        for cat in categories
    }
