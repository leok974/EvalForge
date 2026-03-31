---
title: Typing (Python Type Hints)
---

# Definition
**Type Hints** (introduced in Python 3.5 via PEP 484) are formal annotations that suggest the data type of variables, function parameters, and return values.

# Why It Matters
Python is dynamic, but as systems grow, it becomes hard to track what `data` actually contains. Type hints:
- Enable **IDE Autocomplete** and static analysis.
- Serve as **In-code Documentation** for other developers.
- Catch "TypeErrors" *before* you run the code using tools like `mypy`.

# Deep Dive Example
```python
from typing import List, Dict, Optional

def get_user_scores(user_id: int) -> Optional[List[int]]:
    """Returns a list of scores for a user, or None if not found."""
    db: Dict[int, List[int]] = {
        1: [10, 20, 30],
        2: [5, 15]
    }
    return db.get(user_id)

scores = get_user_scores(1)
if scores:
    print(sum(scores))
```

# Common Mistakes
- **Runtime Enforcement**: Type hints **do not** stop you from passing the wrong type at runtime. Python will still run `greet(123)` even if it's hinted as `str`.
- **Over-typing**: Only hint where it adds value. Local variables often don't need hints if their origin is clear.

# In EvalForge
We use type hints to define **Data Contracts** in our System Engineering tracks.
