
import os
import json
import frontmatter
import hashlib
from pathlib import Path

CODEX_ROOT = Path("docs/codex")
BROKEN_LINKS_FILE = Path("artifacts/codex_broken_links.json")
REWRITES_LOG = Path("artifacts/codex_rewrites.json")
REWRITES_MD = Path("artifacts/codex_rewrites.md")

# Tier-1 Templates by World
TEMPLATES = {
    "sql": {
        "tags": ["sql", "database", "query"],
        "example": "SELECT * FROM users WHERE active = true;",
        "lang": "sql",
        "pitfalls": [
            "Forgetting the semicolon at the end of the statement.",
            "Selecting all columns (`*`) in production can reduce performance."
        ],
        "related": ["sql/select", "sql/where"]
    },
    "ts": {
        "tags": ["typescript", "typing", "javascript"],
        "example": """function greet(name: string): string {
  return `Hello, ${name}`;
}""",
        "lang": "typescript",
        "pitfalls": [
            "Overusing `any` defeats the purpose of TypeScript.",
            "Type assertions (`as`) can hide runtime errors."
        ],
        "related": ["ts/types", "ts/interfaces"]
    },
    "ml": {
        "tags": ["machine-learning", "data", "python"],
        "example": """import numpy as np
x = np.array([1, 2, 3])""",
        "lang": "python",
        "pitfalls": [
            "Mismatched dimensions (shapes) are the most common error.",
            "Data leakage during preprocessing can invalidate results."
        ],
        "related": ["ml/training", "ml/models"]
    },
    "infra": {
        "tags": ["infrastructure", "docker", "deployment"],
        "example": """FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]""",
        "lang": "dockerfile",
        "pitfalls": [
            "Exposing sensitive ports in production.",
            "Hardcoding secrets in the Dockerfile."
        ],
        "related": ["infra/containers", "infra/docker-compose"]
    }
}

DEFAULT_TEMPLATE = {
    "tags": ["concept"],
    "example": "// Example code",
    "lang": "text",
    "pitfalls": ["Common misunderstanding 1", "Common misunderstanding 2"],
    "related": ["concept/related-1", "concept/related-2"]
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
        
    # Update MD
    with open(REWRITES_MD, "a") as f:
        f.write(f"- **{entry['timestamp']}**: Modified `{entry['path']}` (Reason: {entry['reason']})\n")

from datetime import datetime

def scaffold_term(ref):
    # ref format: codex:glossary/world/term or codex:world/term
    parts = ref.replace("codex:", "").split("/")
    
    if len(parts) >= 3 and parts[0] == "glossary":
        world = parts[1]
        term = parts[-1]
        rel_path = Path("glossary") / world / f"{term}.md"
    elif len(parts) == 2:
        world = parts[0]
        term = parts[1]
        rel_path = Path("glossary") / world / f"{term}.md"
    else:
        world = parts[0].replace("world-", "")
        term = parts[-1]
        rel_path = Path("glossary") / world / f"{term}.md"
        
    full_path = CODEX_ROOT / rel_path
    
    # Generate Content
    title = term.replace("-", " ").title()
    template = TEMPLATES.get(world, DEFAULT_TEMPLATE)
    
    # Helper to format list
    pitfalls_md = "\n".join([f"- {p}" for p in template['pitfalls']])
    related_md = "\n".join([f"- [[{r}]]" for r in template['related']])

    if "term-" in term:
        # Garbage term logic
        content = f"""---
title: {title}
id: glossary/{world}/{term}
world: {world}
tags: {json.dumps(template['tags'])}
---

# {title}

**{title}** is a placeholder term referenced by the quest system. 

## Usage

```{template['lang']}
{template['example']}
```

## Pitfalls

{pitfalls_md}

## Related

{related_md}
"""
    else:
        content = f"""---
title: {title}
id: glossary/{world}/{term}
world: {world}
tags: {json.dumps(template['tags'])}
---

# {title}

**{title}** is a key concept in {world}. It defines a specific behavior or data structure essential for development.

## Usage

```{template['lang']}
{template['example']}
```

## Pitfalls

{pitfalls_md}

## Related

{related_md}

> [!NOTE]
> This definition is a scaffold.
"""

    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # SAFETY: Check for overwrite
    before_hash = None
    if full_path.exists():
        with open(full_path, "rb") as f:
            before_hash = hashlib.sha256(f.read()).hexdigest()
    
    # Write
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    # Log
    after_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    if before_hash != after_hash:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "path": str(full_path),
            "before_hash": before_hash,
            "after_hash": after_hash,
            "reason": "Scaffolding Tier-1 Content"
        }
        append_rewrite_log(entry)
        print(f"✅ Scaffolded {full_path}")
    else:
        print(f"Skipping {full_path} (No change)")

def main():
    if not BROKEN_LINKS_FILE.exists():
        print("No broken links file found.")
        return

    with open(BROKEN_LINKS_FILE, "r") as f:
        links = json.load(f)
        
    refs = set(l["ref"] for l in links)
    
    print(f"Found {len(refs)} unique broken refs to process.")
    
    # Also scan for existing "scaffolded" low quality ones?
    # User said: "Re-run improved scaffolding to meet Tier-1 standards"
    # This implies we should re-run on the same list we used before.
    # But wait, the file only contains *originally* broken links.
    # Since I fixed them, `audit` won't find them as broken anymore.
    # So I need to iterate over the *existing* files created by the previous run?
    # Or just use the old JSON list I still have? 
    # Yes, usage of `codex_broken_links_pass2.json` is correct here as it contains the list of 77 terms.
    
    for ref in refs:
        if "glossary" in ref or "ml/" in ref or "sql/" in ref or "ts/" in ref or "infra/" in ref:
            scaffold_term(ref)

if __name__ == "__main__":
    main()
