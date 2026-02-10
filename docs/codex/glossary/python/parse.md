---
id: glossary/python/parse
title: Parse
world: python
level: beginner
tags: [data, strings, processing]
related:
  - codex:glossary/python/csv
  - codex:glossary/python/dictionary
  - codex:glossary/python/data-pipeline
---

## Definition
**Parsing** is the process of analyzing text or data to extract structured information. In Python, parsing turns strings into usable data structures like dicts, lists, or domain objects.

## Usage
- Parse JSON with `json.loads()`.
- Parse CSV with the `csv` module.
- Parse dates with `datetime.strptime()`.
- Parse custom formats with regex or string methods.

## Example
```python
import json
from datetime import datetime

# Parse JSON
json_str = '{"name": "Alice", "age": 30}'
data = json.loads(json_str)
print(data['name'])  # "Alice"

# Parse dates
date_str = "2024-01-15"
date_obj = datetime.strptime(date_str, "%Y-%m-%d")
print(date_obj.year)  # 2024

# Parse custom format
log_line = "2024-01-15 ERROR: Connection failed"
parts = log_line.split(" ", 2)  # Split into date, level, message
print(parts[1])  # "ERROR:"
```

## Pitfalls

* Parsing untrusted input without validation can cause security issues (injection attacks).
* Assuming a fixed format breaks when data varies; handle edge cases.

## Related

* CSV: CSV parsing is a common parsing task.
* Dictionary: parsing often produces dictionaries.
* Data Pipeline: parsing is the first step in data pipelines.