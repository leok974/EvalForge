# Reshaping Python Data

When you need to aggregate data, Python offers several powerful patterns. While you could use a standard `for` loop, "Pythonic" automation often uses more concise and expressive tools.

### Dictionary Comprehensions
You can create a new dictionary by iterating over a list:

```python
# Example: Convert a list of names to a map of name lengths
names = ["Alice", "Bob", "Charlie"]
name_lengths = {name: len(name) for name in names}
# Result: {'Alice': 5, 'Bob': 3, 'Charlie': 7}
```

### Aggregation with Counter or set
To sum values by category, a common pattern is to first identify unique categories:

```python
items = [{"id": 1, "val": 10}, {"id": 2, "val": 5}]
unique_ids = {i["id"] for i in items}
```

### Your Task
In `task.py`, take the `items` list and return a dictionary mapped as `{category: total_qty}`. 
Try to use a comprehension if you can, or a clean `for` loop if that feels more robust for this stage.
