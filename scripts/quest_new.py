
import argparse
import os
import json
import sys

def create_quest_scaffold(args):
    # 1. Determine Target Directory
    # Convention: docs/quests/{slug}/quest.json
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_base = os.path.join(root_dir, "docs", "quests", args.slug)
    
    if os.path.exists(target_base):
        print(f"❌ Error: directory {target_base} already exists.")
        sys.exit(1)
        
    os.makedirs(target_base)
    os.makedirs(os.path.join(target_base, "starter"))
    os.makedirs(os.path.join(target_base, "solution"))
    
    # 2. Create Workspace Files
    # Starter
    if args.language == "python":
        starter_entry = "main.py"
    elif args.language == "javascript":
        starter_entry = "main.js"
    else:
        starter_entry = "main.ts"
    with open(os.path.join(target_base, "starter", starter_entry), "w", encoding="utf-8") as f:
        f.write("# Starter Code\n\ndef solution():\n    pass\n")
        
    # Solution
    with open(os.path.join(target_base, "solution", starter_entry), "w", encoding="utf-8") as f:
        f.write("# Solution Code\n\ndef solution():\n    return 42\n")

    # Tests (if applicable)
    if args.kind == "tests" and args.language == "python":
         with open(os.path.join(target_base, "starter", "test_public.py"), "w", encoding="utf-8") as f:
             f.write("import unittest\nfrom main import solution\n\nclass TestPublic(unittest.TestCase):\n    def test_basic(self):\n        self.assertEqual(solution(), 42)\n")

    # 3. Create Tutorial Files (Phase 9.2) & Content Contract (Phase 10)
    if not args.sandbox:
        # 3a. briefing.md (Required)
        briefing_path = os.path.join(target_base, "briefing.md")
        with open(briefing_path, "w", encoding="utf-8") as f:
            f.write(f"""# Briefing

## Objective
Implement a solution that solves the core problem of {args.title}.

## Constraints
- Use standard library only.
- Efficiency matters.

## Success Criteria
- Passes all provided test cases.
- Validates edge cases.
""")

        # 3b. tutorial.md (Required if Tier >= 1, but we default to creating it if requested)
        if args.with_tutorial:
            tut_path = os.path.join(target_base, "tutorial.md")
            with open(tut_path, "w", encoding="utf-8") as f:
                f.write(f"""# Mission Walkthrough
Welcome to {args.title}.

## 1. The Concept
Explain the core concept here.

## 2. Implementation Strategy
How should the agent approach this?

## 3. Pitfalls
Common mistakes to avoid.

## 4. Verification
How to test the solution.
""")
        
        # 3c. hints.md (Required if Tier >= 1)
        if args.tier >= 1:
            hints_path = os.path.join(target_base, "hints.md")
            with open(hints_path, "w", encoding="utf-8") as f:
                f.write(f"""# Hints

## Hint 1
Check the input constraints carefully.

## Hint 2
Consider edge cases like empty input.

## Hint 3
Review the provided examples.
""")

        # 3d. lore.md (Optional, triggered by flag)
        if args.with_lore:
            lore_path = os.path.join(target_base, "lore.md")
            with open(lore_path, "w", encoding="utf-8") as f:
                f.write(f"""# System Log: {args.slug}

> *Establishing secure uplink...*
>
> Target: {args.title}
> Status: Pending Authorization
> User ID: **AUTH_REQUIRED**

The mission parameters are set. 
Initialize the workspace to begin the assignment.
""")

        # 3e. terms.json
        terms = []
        for i in range(args.terms):
            stub_term = f"term-{i+1}"
            terms.append({
                "term": stub_term,
                "definition": "TODO: Add definition.",
                "codex_ref": f"codex:glossary/{args.world}/{stub_term}"
            })
            
        terms_path = os.path.join(target_base, "terms.json")
        with open(terms_path, "w", encoding="utf-8") as f:
            json.dump(terms, f, indent=2)
            
        # 3f. Codex Stubs (Optional)
        if args.codex_stubs:
            codex_dir = os.path.join(root_dir, "data", "codex", "glossary", args.world)
            os.makedirs(codex_dir, exist_ok=True)
            for t in terms:
                # parse ref codex:glossary/{world}/{term}
                ref_parts = t["codex_ref"].replace("codex:glossary/", "").split("/")
                if len(ref_parts) >= 2:
                     fname = ref_parts[-1] + ".md"
                     cpath = os.path.join(codex_dir, fname)
                     if not os.path.exists(cpath):
                         with open(cpath, "w", encoding="utf-8") as cf:
                             cf.write(f"# {t['term']}\n\nDefinition for {t['term']}.\n")
                         print(f"   + Created Codex Stub: {cpath}")

    # 4. Generate Quest JSON
    quest_data = {
        "slug": args.slug,
        "title": args.title,
        "language": args.language,
        "world_id": args.world,
        "track_id": args.track,
        "tutorial_tier": args.tier,
        "order_index": 1, # TODO: auto-detect max + 1
        "short_description": "A generated quest description.",
        "detailed_description": "Use markdown here.\n\n# Objectives\n- Solve the problem.",
        "objectives": [
            {
                "id": "obj_1",
                "description": "Implement the solution.",
                "type": "test_pass" if args.kind == "tests" else "output_match",
                "matcher": ".*" if args.kind == "output" else None
            }
        ],
        "grading": {
            "mode": args.kind
        },
        "workspace": {
            "entrypoint": starter_entry,
            "files_from": "./starter"
        },
        "docs": {
            "briefing_required": True,
            "lore_required": args.with_lore
        },
        "smoke": {
            "solution_workspace_files": []
        }
    }
    
    # Write JSON
    json_path = os.path.join(target_base, "quest.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(quest_data, f, indent=4)
        
    print(f"✅ Quest scaffold created at: {target_base}")
    print(f"   - {json_path}")
    if not args.sandbox:
        print(f"   - briefing.md")
        if args.with_tutorial: print(f"   - tutorial.md")
        if args.tier >= 1: print(f"   - hints.md")
        if args.with_lore: print(f"   - lore.md")
        print(f"   - terms.json")
    print(f"   - starter/{starter_entry}")
    print("👉 Next: Edit the files, then run 'python scripts/dev_validate_all.py' to verify.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new quest")
    parser.add_argument("--world", required=True, help="World ID (e.g. foundry)")
    parser.add_argument("--track", required=True, help="Track ID")
    parser.add_argument("--slug", required=True, help="Quest Slug (unique)")
    parser.add_argument("--title", required=True, help="Quest Title")
    parser.add_argument("--language", default="python", choices=["python", "typescript", "java", "javascript"], help="Language")
    parser.add_argument("--kind", default="tests", choices=["tests", "output"], help="Grading mode")
    parser.add_argument("--tier", type=int, default=1, help="Tutorial Tier (default: 1)")
    
    # New Phase 9.2 Flags
    parser.add_argument("--with-tutorial", action="store_true", default=True, help="Generate tutorial files")
    parser.add_argument("--no-tutorial", action="store_false", dest="with_tutorial", help="Skip tutorial generation")
    parser.add_argument("--with-lore", action="store_true", help="Generate lore files")
    parser.add_argument("--terms", type=int, default=3, help="Number of stub terms")
    parser.add_argument("--codex-stubs", action="store_true", help="Generate stub codex files")
    parser.add_argument("--sandbox", action="store_true", help="Sandbox mode (minimal files)")
    
    args = parser.parse_args()
    create_quest_scaffold(args)
