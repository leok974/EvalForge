# Tutorial: Data Normalization

Normalization is the process of organizing data to ensure consistency and minimize redundancy. In Python, this often involves cleaning dictionary keys and coercing values into their correct types.

## Key Concept: Coercing Types
When dealing with "messy" data, you cannot assume a field like `is_active` is a boolean. It might be `'true'`, `1`, or `True`.

```python
def to_bool(value):
    if isinstance(value, bool):
        return value
    if str(value).lower() in ("true", "1", "yes"):
        return True
    return False
```

## Cleaning Strings
Standardizing strings involves stripping whitespace and handling case sensitivity.

```python
name = raw_name.strip().title() if raw_name else "Unknown"
```

## Handling Lists
Sometimes "tags" arrive as a comma-separated string instead of a list.

```python
def normalize_tags(val):
    if isinstance(val, list):
        return [t.strip() for t in val]
    if isinstance(val, str):
        return [t.strip() for t in val.split(",") if t.strip()]
    return []
```

## Sorting with itemgetter
After processing, sort your records to maintain a deterministic output order.

```python
from operator import itemgetter
records.sort(key=itemgetter("id"))
```
