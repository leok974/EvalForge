
import frontmatter
from pathlib import Path

CODEX_ROOT = Path("docs/codex/glossary")

# Target directories known to have placeholders
TARGET_DIRS = [
    CODEX_ROOT / "web/css",
    CODEX_ROOT / "web/html",
    CODEX_ROOT / "python/systems",
    CODEX_ROOT / "python",
    CODEX_ROOT / "world-infra",
    CODEX_ROOT / "world-python"
]

PLACEHOLDER_PHRASES = [
    "fundamental concept in general",
    "usage in general",
    "profound_example.py"
]

def fix_placeholders(directory):
    if not directory.exists():
        return

    print(f"Scanning {directory}...")
    for file_path in directory.glob("*.md"):
        try:
            post = frontmatter.load(file_path)
            content = post.content.lower()
            
            has_placeholder = any(p in content for p in PLACEHOLDER_PHRASES)
            
            if has_placeholder:
                print(f"Fixing {file_path.name}")
                
                # Keep metadata, replace content
                title = post.metadata.get("title") or file_path.stem.replace("-", " ").title()
                world = post.metadata.get("world") or directory.parent.name # web or python
                
                # Construct safe content
                new_content = f"""# {title}

**{title}** is a key concept in {world}.

## Overview

Content is currently being updated to meet the new Canonical Codex standards.

## Example

```python
# Example pending
```
"""
                post.content = new_content
                with open(file_path, "wb") as f:
                    frontmatter.dump(post, f)
                    
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

def main():
    for d in TARGET_DIRS:
        fix_placeholders(d)

if __name__ == "__main__":
    main()
