---
title: collections.Counter
---

# Definition
`collections.Counter` is a built-in subclass of `dict` designed to count hashable objects. It's a powerful tool for frequency analysis and data transformation.

# Why Use It?
Instead of manually writing loops to count items in a list, `Counter` does it in one line.

# Examples
```python
from collections import Counter

# Basics
counts = Counter(['apple', 'orange', 'apple', 'pear', 'apple', 'orange'])
print(counts) # Counter({'apple': 3, 'orange': 2, 'pear': 1})

# Common methods
print(counts.most_common(1)) # [('apple', 3)]

# Mathematical Operations
c = Counter(a=3, b=1)
d = Counter(a=1, b=2)
print(c + d) # Counter({'a': 4, 'b': 3})
```

# In Data Transformations
In quests like `python-dicts-lists-transform`, you can use `Counter` to aggregate quantities across multiple records efficiently.

# Related
- [Dictionary Comprehensions](codex:glossary/python/dict-comprehension)
- [Iteration](codex:glossary/python/iteration)
