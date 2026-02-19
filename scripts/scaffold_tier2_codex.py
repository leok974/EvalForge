
import os
from pathlib import Path

CODEX_ROOT = Path("docs/codex/glossary")

TERMS = [
    # Python
    {
        "track": "python",
        "slug": "argparse",
        "title": "Argparse",
        "definition": "A standard library module for parsing command-line arguments.",
        "why": "Allows scripts to accept inputs from the terminal, making them flexible.",
        "example": "import argparse\\nparser = argparse.ArgumentParser()",
        "mistake": "Forgetting to call `parse_args()`.",
        "evalforge": "Used in CLI-based quests."
    },
    {
        "track": "python",
        "slug": "exception",
        "title": "Exception",
        "definition": "An error detected during execution.",
        "why": "Allows programs to handle errors gracefully instead of crashing.",
        "example": "try:\\n    x = 1/0\\nexcept ZeroDivisionError:\\n    print('Oops')",
        "mistake": "Catching generic `Exception` without logging.",
        "evalforge": "Key for writing robust logic."
    },
    {
        "track": "python",
        "slug": "file-io",
        "title": "File I/O",
        "definition": "Reading from and writing to files.",
        "why": "Essential for data persistence.",
        "example": "with open('data.txt', 'r') as f:\\n    content = f.read()",
        "mistake": "Forgetting to close files (use `with` statement).",
        "evalforge": "Used in data processing quests."
    },
    {
        "track": "python",
        "slug": "dict-comprehension",
        "title": "Dict Comprehension",
        "definition": "A concise way to create dictionaries.",
        "why": "More readable and faster than loops for simple transforms.",
        "example": "{k: v*2 for k, v in data.items()}",
        "mistake": "Using it for complex logic (hard to read).",
        "evalforge": "Common in data transformation tasks."
    },
    {
        "track": "python",
        "slug": "class-method",
        "title": "Class Method",
        "definition": "A method bound to the class, not the instance.",
        "why": "Used for factory methods or modifying class state.",
        "example": "@classmethod\\ndef create(cls): ...",
        "mistake": "Confusing with static methods.",
        "evalforge": "Used in OOP quests."
    },
    {
        "track": "python",
        "slug": "typing",
        "title": "Typing (Hints)",
        "definition": "Annotations indicating variable types.",
        "why": "Improves code clarity and enables static analysis.",
        "example": "def greet(name: str) -> str:",
        "mistake": "Thinking they enforce types at runtime (they don't).",
        "evalforge": "Required for contract-based quests."
    },

    # Git
    {
        "track": "git",
        "slug": "merge-conflict",
        "title": "Merge Conflict",
        "definition": "When Git cannot automatically reconcile differences.",
        "why": "Happens when parallel branches modify the same lines.",
        "example": "<<<<<<< HEAD\\nA\\n=======\\nB\\n>>>>>>> feature",
        "mistake": "Committing conflict markers.",
        "evalforge": "Tested in `git-t2-merge-conflict`."
    },
    {
        "track": "git",
        "slug": "rebase",
        "title": "Rebase",
        "definition": "Reapplying commits on top of another base tip.",
        "why": "Keeps history linear.",
        "example": "git rebase main",
        "mistake": "Rebasing public history (rewrites history).",
        "evalforge": "Tested in `git-t2-rebase`."
    },
    {
        "track": "git",
        "slug": "fast-forward",
        "title": "Fast-Forward",
        "definition": "Moving the branch pointer forward without a merge commit.",
        "why": "Possible when no divergent history exists.",
        "example": "git merge feature # (Fast-forward if linear)",
        "mistake": "Assuming it always happens (use `--no-ff` to force merge commit).",
        "evalforge": "Concept in branching quests."
    },
    {
        "track": "git",
        "slug": "detached-head",
        "title": "Detached HEAD",
        "definition": "Checking out a commit directly, not a branch.",
        "why": "Useful for inspecting history.",
        "example": "git checkout <commit-hash>",
        "mistake": "Committing in detached state (commits will be lost).",
        "evalforge": "Simulation scenario."
    },
    {
        "track": "git",
        "slug": "annotated-tag",
        "title": "Annotated Tag",
        "definition": "A tag stored as a full object with message and author.",
        "why": "Used for releases.",
        "example": "git tag -a v1.0 -m 'Release'",
        "mistake": "Using lightweight tags for releases.",
        "evalforge": "Tested in `git-t2-release`."
    },
    {
        "track": "git",
        "slug": "release-notes",
        "title": "Release Notes",
        "definition": "Documentation of changes in a release.",
        "why": "Communicates updates to users.",
        "example": "## v1.0\\n- Added feature X",
        "mistake": "Reviewing only commit logs.",
        "evalforge": "Part of the Release workflow."
    },

    # SQL
    {
        "track": "sql",
        "slug": "group-by",
        "title": "GROUP BY",
        "definition": "Groups rows sharing a property so aggregate functions apply to each group.",
        "why": "Essential for reporting.",
        "example": "SELECT cat, COUNT(*) FROM prod GROUP BY cat",
        "mistake": "Selecting non-aggregated columns not in GROUP BY.",
        "evalforge": "Tested in `sql-t2-groupby-having`."
    },
    {
        "track": "sql",
        "slug": "having",
        "title": "HAVING",
        "definition": "Filters groups created by GROUP BY.",
        "why": "WHERE filters rows; HAVING filters groups.",
        "example": "HAVING COUNT(*) > 5",
        "mistake": "Using HAVING without GROUP BY.",
        "evalforge": "Tested in `sql-t2-groupby-having`."
    },
    {
        "track": "sql",
        "slug": "cte-with",
        "title": "CTE (Common Table Expression)",
        "definition": "A temporary result set defined within the execution of a statement.",
        "why": "Improves readability and allows recursion.",
        "example": "WITH ActiveUsers AS (...)",
        "mistake": "Assuming it persists like a temp table.",
        "evalforge": "Tested in `sql-t2-analytics-pack`."
    }
]

def main():
    for t in TERMS:
        track_dir = CODEX_ROOT / t["track"]
        track_dir.mkdir(parents=True, exist_ok=True)
        
        path = track_dir / f"{t['slug']}.md"
        
        content = f"""---
title: {t['title']}
---

# Definition
{t['definition']}

# Why It Matters
{t['why']}

# Minimal Example
```python
{t['example']}
```

# Common Mistakes
* {t['mistake']}

# In EvalForge
* {t['evalforge']}
"""
        # Fix language for non-python
        if t["track"] == "sql":
            content = content.replace("```python", "```sql")
        elif t["track"] == "git":
            content = content.replace("```python", "```bash")

        path.write_text(content, encoding="utf-8")
        print(f"Created {path}")

if __name__ == "__main__":
    main()
