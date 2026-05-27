## Concept
To find the unique categories, you can use a set comprehension: `categories = {item['category'] for item in items}`.

## Guided
Once you have the unique categories, you can build the final dictionary using a comprehension that sums the quantities:
`{cat: sum(item['qty'] for item in items if item['category'] == cat) for cat in categories}`.

## Full Solution
```python
def transform_inventory(items: list[dict]) -> dict[str, int]:
    categories = {item['category'] for item in items}
    return {
        cat: sum(i['qty'] for i in items if i['category'] == cat)
        for cat in categories
    }
```
Alternatively, using `collections.defaultdict` is often more efficient for large datasets.
