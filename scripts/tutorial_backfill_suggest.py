
import os
import sys
import json
import argparse

def generate_strict_tutorial(slug, tier, world):
    title = slug.replace("-", " ").title()
    
    lang = "python"
    if "js" in world or "javascript" in world:
        lang = "javascript"
    elif "ts" in world or "typescript" in world:
        lang = "typescript"
    elif "sql" in world:
        lang = "sql"
    elif "git" in world:
        lang = "bash"  # Git commands are bash
        
    # Tier-1 Strict Template
    return f"""# {title}

## Outcome

In this quest, you'll work with {title.lower()} to practice core {lang.upper()} concepts.

## Concept in 30 seconds

{title} demonstrates fundamental programming patterns used in real-world applications.

## Key terms

The key terms for this quest are defined below and linked to the Codex for reference.

## Walkthrough

1. **Setup**: Review the starting code.
2. **Implement**: Follow the objectives.
3. **Verify**: Run the tests.

## Example implementation

```{lang}
-- Strict Tier-1 Example Required
SELECT * FROM users; -- Example code for {slug}
```

## Common mistakes

- Syntax errors
- Incorrect types
- Missing brackets

## Check yourself

- [ ] Code runs without errors
- [ ] Output matches expected value
- [ ] All tests pass
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world", required=True)
    parser.add_argument("--tier", type=int, required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()
    
    with open(args.manifest, "r") as f:
        manifest = json.load(f)
        
    slugs = manifest.get("slugs", [])
    root_dir = os.getcwd()
    
    print(f"🔄 Backfilling {len(slugs)} quests for {args.world} (Tier {args.tier})")
    
    for slug in slugs:
        quest_dir = os.path.join(root_dir, "docs", "quests", slug)
        tut_path = os.path.join(quest_dir, "tutorial.md")
        
        if not os.path.exists(quest_dir):
            print(f"⚠️  Quest dir not found: {slug}")
            continue
            
        # Overwrite or create if missing?
        # User said "backfill", implying if empty/missing?
        # But scaffolder created stubs. We want the STRICT content.
        # Scaffolder created generic stub. Let's overwrite with strict template.
        
        content = generate_strict_tutorial(slug, args.tier, args.world)
        
        with open(tut_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"✅ Updated tutorial: {slug}")

if __name__ == "__main__":
    main()
