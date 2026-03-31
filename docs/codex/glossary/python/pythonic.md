---
title: Pythonic Code
---

# Definition
**Pythonic** describes code that follows the idioms and best practices of the Python community. It prioritizes readability, simplicity, and the use of Python's unique features (like list comprehensions).

# The Zen of Python
Import `this` in any Python REPL to see the guiding principles:
- *Beautiful is better than ugly.*
- *Explicit is better than implicit.*
- *Simple is better than complex.*
- *Readability counts.*

# Examples
### Non-Pythonic (C-style)
```python
i = 0
while i < len(my_list):
    print(my_list[i])
    i += 1
```

### Pythonic
```python
for item in my_list:
    print(item)
```

# Common Idioms
- **List Comprehensions**: `[x*x for x in nums if x > 0]`
- **Unpacking**: `a, b = b, a`
- **Context Managers**: `with open('file.txt') as f:`

# In EvalForge
We reward "Pythonic" solutions—not just code that works, but code that is clean and idiomatic.
