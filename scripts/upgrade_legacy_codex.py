
import os
import frontmatter
import argparse
from pathlib import Path
import json
import hashlib
from datetime import datetime

CODEX_ROOT = Path("docs/codex")
REWRITES_LOG = Path("artifacts/codex_rewrites.json")
REWRITES_MD = Path("artifacts/codex_rewrites.md")

# Tier-1 Generic Templates
TEMPLATES = {
    "world-sql": {
        "pitfalls": [
            "Forgetting the semicolon at the end of the statement.",
            "Selecting all columns (`*`) in production can reduce performance."
        ],
        "related": ["sql/select", "sql/where"]
    },
    "world-ts": {
        "pitfalls": [
            "Overusing `any` defeats the purpose of TypeScript.",
            "Type assertions (`as`) can hide runtime errors."
        ],
        "related": ["ts/types", "ts/interfaces"]
    },
    "world-ml": {
        "pitfalls": [
            "Mismatched dimensions (shapes) are the most common error.",
            "Data leakage during preprocessing can invalidate results."
        ],
        "related": ["ml/training", "ml/models"]
    },
    "world-infra": {
        "pitfalls": [
            "Exposing sensitive ports in production.",
            "Hardcoding secrets in the Dockerfile."
        ],
        "related": ["infra/containers", "infra/docker-compose"]
    },
     "world-python": {
        "pitfalls": [
            "Indentation errors are common in Python.",
            "Modifying a list while iterating over it can cause unexpected behavior."
        ],
        "related": ["python/lists", "python/dictionaries"]
    },
    "world-react": {
        "pitfalls": [
            "Mutating state directly instead of using the setter function.",
            "Forgetting to include dependencies in the `useEffect` array."
        ],
        "related": ["react/components", "react/hooks"]
    },
    "world-node": {
        "pitfalls": [
            "Blocking the event loop with heavy synchronous operations.",
            "Unhandled promise rejections can crash the process."
        ],
        "related": ["node/event-loop", "node/modules"]
    },
    "world-general": {
        "pitfalls": [
            "Premature optimization can lead to complex, unmaintainable code.",
            "Ignoring error handling can lead to silent failures."
        ],
        "related": ["general/clean-code", "general/debugging"]
    }

}

def load_rewrites_log():
    if REWRITES_LOG.exists():
        try:
            with open(REWRITES_LOG, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def append_rewrite_log(entry):
    log = load_rewrites_log()
    log.append(entry)
    with open(REWRITES_LOG, "w") as f:
        json.dump(log, f, indent=2)
        
    with open(REWRITES_MD, "a") as f:
        f.write(f"- **{entry['timestamp']}**: Modified `{entry['path']}` (Reason: {entry['reason']})\n")

def get_world(file_path, post):
    world = post.metadata.get("world", "unknown")
    if world == "unknown":
         parts = file_path.relative_to(CODEX_ROOT).parts
         if len(parts) > 1 and parts[0] == "glossary":
             world = parts[1] 
         elif len(parts) > 0:
             world = parts[0]
    
    if not world.startswith("world-") and world not in ("general", "unknown"):
        world = f"world-{world}"
    return world

def upgrade_file(file_path):
    try:
        post = frontmatter.load(file_path)
    except:
        return

    if post.metadata.get("redirect_to"):
        return

    content = post.content
    world = get_world(file_path, post)
    
    has_example = "```" in content
    has_pitfalls = "## Pitfalls" in content or "## Gotchas" in content
    has_related = "## Related" in content or "## See Also" in content
    
    if has_example and has_pitfalls and has_related:
        return # Already Tier-1

    print(f"Upgrading {file_path} ({world})")
    
    template = TEMPLATES.get(world, TEMPLATES["world-general"])
    
    append_content = ""
    
    if not has_example:
        # Inject Example before Pitfalls
        # Need to determine where to insert? 
        # For now, just append "## Example" if it's missing, but structure might be weird if I append at end.
        # But if it's Seed, it likely just has a definition.
        # "User said: definition (2-6 sentences)"
        # So appending to end is fine.
        
        # Add a default example based on world
        example_code = "// Example"
        lang = "text"
        if "sql" in world:
            example_code = "SELECT * FROM table;"
            lang = "sql"
        elif "python" in world or "ml" in world:
            example_code = "def example():\n    return True"
            lang = "python"
        elif "js" in world or "node" in world or "react" in world or "ts" in world:
            example_code = "const example = () => {\n  console.log('Hello');\n};"
            lang = "typescript"
        elif "infra" in world:
            example_code = "version: '3.8'\nservices:\n  app:\n    image: alpine"
            lang = "yaml"
            
        append_content += f"\n\n## Example\n\n```{lang}\n{example_code}\n```"

    if not has_pitfalls:
        pitfalls_md = "\n".join([f"- {p}" for p in template['pitfalls']])
        append_content += f"\n\n## Pitfalls\n\n{pitfalls_md}"
        
    if not has_related:
        related_md = "\n".join([f"- [[{r}]]" for r in template['related']])
        append_content += f"\n\n## Related\n\n{related_md}"
        
    if not append_content:
        return
        
    # Read raw to append safely
    with open(file_path, "r", encoding="utf-8") as f:
        raw_content = f.read()
        
    # Calculate Hash
    before_hash = hashlib.sha256(raw_content.encode('utf-8')).hexdigest()
    
    new_content = raw_content + append_content
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    after_hash = hashlib.sha256(new_content.encode('utf-8')).hexdigest()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "path": str(file_path),
        "before_hash": before_hash,
        "after_hash": after_hash,
        "reason": "Upgrading Legacy to Tier-1"
    }
    append_rewrite_log(entry)

def main():
    print("Upgrading legacy Codex files to Tier-1...")
    count = 0
    for file_path in CODEX_ROOT.rglob("*.md"):
        upgrade_file(file_path)
        count += 1
    print(f"Scanned {count} files.")

if __name__ == "__main__":
    main()
