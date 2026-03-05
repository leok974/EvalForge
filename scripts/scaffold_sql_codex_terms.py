import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CODEX_DIR = REPO_ROOT / "docs" / "codex" / "glossary" / "sql"

terms = [
    "alias", "query-planning"
]

def titleize(slug):
    words = slug.split("-")
    return " ".join([w.capitalize() for w in words])

def main():
    os.makedirs(CODEX_DIR, exist_ok=True)
    for term in terms:
        file_path = CODEX_DIR / f"{term}.md"
        content = f"""---
title: "{titleize(term)}"
tags: ["sql", "intermediate"]
---

# {titleize(term)}

This entry describes the concept of **{titleize(term)}** in SQL.

## Usage

Example goes here...
"""
        file_path.write_text(content, encoding="utf-8")
        print(f"Created/Updated {file_path}")

if __name__ == "__main__":
    main()
