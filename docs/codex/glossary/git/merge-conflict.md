---
title: Merge Conflict
---

# Definition
When Git cannot automatically reconcile differences.

# Why It Matters
Happens when parallel branches modify the same lines.

# Minimal Example
```bash
<<<<<<< HEAD\nA\n=======\nB\n>>>>>>> feature
```

# Common Mistakes
* Committing conflict markers.

# In EvalForge
* Tested in `git-t2-merge-conflict`.
