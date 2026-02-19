---
title: Fast-Forward
---

# Definition
Moving the branch pointer forward without a merge commit.

# Why It Matters
Possible when no divergent history exists.

# Minimal Example
```bash
git merge feature # (Fast-forward if linear)
```

# Common Mistakes
* Assuming it always happens (use `--no-ff` to force merge commit).

# In EvalForge
* Concept in branching quests.
