
import os
import sys
import json
import frontmatter
import argparse
import re
from pathlib import Path
from collections import defaultdict

# Configuration
CODEX_ROOT = Path("docs/codex")
QUESTS_ROOT = Path("docs/quests")
MINIMUMS_FILE = Path("configs/codex_world_minimums.json")

PLACEHOLDER_PHRASES = [
    "fundamental concept in general",
    "usage in general",
    "profound_example.py"
]

def get_all_codex_files():
    return list(CODEX_ROOT.rglob("*.md"))

def load_minimums():
    if MINIMUMS_FILE.exists():
        try:
            with open(MINIMUMS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load world minimums: {e}")
    return {}

def check_quality(file_path, post):
    """Analyze quality of a Codex entry."""
    if post.metadata.get("redirect_to"):
        return "redirect", []

    content = post.content
    issues = []
    
    # 1. Definition (Heuristic: > 50 characters in first non-header paragraph?)
    # Or just presence of text.
    # User said: "Definition (2-6 sentences)" -> Hard to enforce strictly via regex without NLP.
    # We'll check for reasonable content length (> 100 chars?).
    has_def = len(content.strip()) > 100
    
    # 2. Example (Fenced code block) - allow optional space after backticks
    has_example = bool(re.search(r"```\s*[a-z]+", content))
    
    # 3. Pitfalls / Gotchas
    has_pitfalls = bool(re.search(r"(?i)##\s*(pitfalls|gotchas|common errors)", content))
    
    # 4. Related
    has_related = bool(re.search(r"(?i)##\s*(related|see also)", content))
    
    # Bucketing
    if has_def and has_example and has_pitfalls and has_related:
        tier = "excellent"
    elif has_def and has_example:
        tier = "good"
    elif has_def:
        tier = "seed"
    else:
        tier = "empty"
        
    # Missing failures for strict mode
    missing = []
    if not has_def: missing.append("Definition")
    if not has_example: missing.append("Example")
    if not has_pitfalls: missing.append("Pitfalls")
    if not has_related: missing.append("Related")
    
    return tier, missing

def check_placeholders(file_path, post):
    """Check for placeholder content in non-redirect files."""
    if post.metadata.get("redirect_to"):
        return []
    
    issues = []
    content = post.content.lower()
    for phrase in PLACEHOLDER_PHRASES:
        if phrase in content:
            issues.append({
                "type": "placeholder",
                "file": str(file_path),
                "message": f"Placeholder phrase found in {file_path}: '{phrase}'"
            })
    return issues

def build_codex_map(files):
    """Build a map of ID -> FilePath and check for duplicates."""
    codex_map = {}
    redirects = {}
    issues = []
    
    # Stats
    world_stats = defaultdict(lambda: defaultdict(int))

    for file_path in files:
        try:
            post = frontmatter.load(file_path)
            
            # Determine ID
            if "id" in post.metadata:
                entry_id = post.metadata["id"]
            else:
                rel_path = file_path.relative_to(CODEX_ROOT)
                entry_id = str(rel_path.with_suffix("")).replace(os.sep, "/")
            
            # Normalize ID
            entry_id = entry_id.replace("codex:", "")
            
            # Determine World
            world = post.metadata.get("world", "unknown")
            # If world is unknown, try to guess from path
            if world == "unknown":
                 parts = file_path.relative_to(CODEX_ROOT).parts
                 if len(parts) > 1 and parts[0] == "glossary":
                     world = parts[1] 
                 elif len(parts) > 0:
                     world = parts[0]
            
            # Normalize world name (e.g. infra -> world-infra)
            # Config uses world-*, metadata might use short name
            if not world.startswith("world-") and world not in ("general", "unknown"):
                world = f"world-{world}"

            # Check for redirect
            if post.metadata.get("redirect_to"):
                target = post.metadata["redirect_to"].replace("codex:", "")
                redirects[entry_id] = target
                world_stats[world]["redirect"] += 1
            else:
                # Canonical Entry
                if entry_id in codex_map:
                    issues.append({
                        "type": "duplicate_id",
                        "id": entry_id,
                        "files": [str(file_path), str(codex_map[entry_id])],
                        "message": f"Duplicate Canonical ID: {entry_id} in {file_path} and {codex_map[entry_id]}"
                    })
                else:
                    codex_map[entry_id] = file_path
                    
                # Quality Check
                tier, missing = check_quality(file_path, post)
                world_stats[world][tier] += 1
                
                # We can store quality issues here if we want to report them individually
                # But mostly we care about aggregates unless --fail-on-low-quality is set
                if missing:
                    issues.append({
                        "type": "quality",
                        "subtype": "missing_tier1",
                        "file": str(file_path),
                        "tier": tier,
                        "missing": missing,
                        "message": f"Low Quality ({tier}): {file_path} missing {missing}"
                    })

        except Exception as e:
            issues.append({
                "type": "parse_error",
                "file": str(file_path),
                "message": f"Failed to parse {file_path}: {e}"
            })
            
    return codex_map, redirects, issues, world_stats

def validate_redirects(redirects, codex_map):
    """Ensure redirects point to existing canonical entries and check loops."""
    issues = []
    
    for src, target in redirects.items():
        # Check if target exists
        if target not in codex_map and target not in redirects:
             issues.append({
                 "type": "broken_redirect",
                 "source": src,
                 "target": target,
                 "message": f"Broken Redirect: {src} -> {target} (Target not found)"
             })
             continue
        
        # Check for loops
        visited = {src}
        curr = target
        path = [src]
        
        for _ in range(10): # Max depth
            if curr in codex_map:
                break # Found canonical
            if curr in redirects:
                if curr in visited:
                    issues.append({
                        "type": "redirect_loop",
                        "path": path + [curr],
                        "message": f"Circular Redirect: {' -> '.join(path)} -> {curr}"
                    })
                    break
                visited.add(curr)
                path.append(curr)
                curr = redirects[curr]
            else:
                break 
        else:
             issues.append({
                 "type": "redirect_depth",
                 "source": src,
                 "message": f"Redirect depth exceeded: {src}"
             })

    return issues

def check_quest_refs(codex_map, redirects):
    """Check that all codex referenced in quests resolve."""
    issues = []
    broken_links = []
    
    for term_file in QUESTS_ROOT.rglob("terms.json"):
        try:
            with open(term_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            refs = []
            if isinstance(data, dict):
                refs = data.get("codex_references", [])
            elif isinstance(data, list):
                for item in data:
                    if "codex_ref" in item:
                        refs.append(item["codex_ref"])
            
            for ref in refs:
                if not ref.startswith("codex:"):
                    continue
                
                term_id = ref.replace("codex:", "")
                
                # Resolve
                curr = term_id
                resolved = False
                for _ in range(10):
                    if curr in codex_map:
                        resolved = True
                        break
                    if curr in redirects:
                        curr = redirects[curr]
                    else:
                        break
                
                if not resolved:
                     quest_slug = term_file.parent.name
                     issue = {
                         "type": "broken_quest_link",
                         "file": str(term_file),
                         "quest_slug": quest_slug,
                         "ref": ref,
                         "message": f"Broken Quest Link: {quest_slug} -> {ref}"
                     }
                     issues.append(issue)
                     broken_links.append({
                         "ref": ref,
                         "quest_slug": quest_slug,
                         "source_file": str(term_file),
                         "field": "codex_references"
                     })
                     
        except Exception as e:
             issues.append({
                 "type": "parse_error",
                 "file": str(term_file),
                 "message": f"Failed to parse quest terms: {e}"
             })
             
    return issues, broken_links

def main():
    parser = argparse.ArgumentParser(description="Audit Codex Consistency and Exports Broken Links")
    parser.add_argument("--emit", help="Path to export broken links JSON")
    parser.add_argument("--fail-on-broken", action="store_true", help="Exit 1 if broken links found")
    parser.add_argument("--fail-on-placeholders", action="store_true", help="Exit 1 if placeholders found")
    parser.add_argument("--tier", type=int, help="Check for quality tier (1=Excellent)", default=0)
    parser.add_argument("--fail-on-low-quality", action="store_true", help="Exit 1 if pages don't meet tier requirements")
    parser.add_argument("--source", choices=["disk"], default="disk", help="Source of truth (default: disk)")
    
    args = parser.parse_args()
    
    print("Auditing Codex Consistency...")
    files = get_all_codex_files()
    codex_map, redirects, issues, world_stats = build_codex_map(files)
    
    # Check Placeholders
    for file_path in files:
        try:
            post = frontmatter.load(file_path)
            issues.extend(check_placeholders(file_path, post))
        except:
            pass
            
    # Validate Redirects
    issues.extend(validate_redirects(redirects, codex_map))
    
    # Check Quest Refs
    quest_issues, broken_links = check_quest_refs(codex_map, redirects)
    issues.extend(quest_issues)
    
    # Check World Minimums
    minimums = load_minimums()
    min_failures = []
    
    print("\n--- World Stats ---")
    for world, stats in world_stats.items():
        # "world-python" vs "python" normaliztion might be needed?
        # Assuming metadata 'world' matches config keys.
        
        good_plus = stats.get("good", 0) + stats.get("excellent", 0)
        total = sum(stats.values())
        print(f"[{world}] Total: {total} | Excellent: {stats['excellent']} | Good: {stats['good']} | Seed: {stats['seed']} | Redirect: {stats['redirect']}")
        
        # Check against config
        required = minimums.get(world)
        if hasattr(required, 'get'): # It's a dict
             required_good = required.get("min_good", 0)
             if good_plus < required_good:
                 msg = f"World '{world}' failed minimum quality. Found {good_plus} good/excellent, needed {required_good}."
                 min_failures.append(msg)
                 issues.append({
                     "type": "world_minimum_failure",
                     "world": world,
                     "message": msg
                 })

    # Emit JSON
    if args.emit:
        output_path = Path(args.emit)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(broken_links, f, indent=2)
        print(f"\nExported {len(broken_links)} broken links to {output_path}")

    # Reporting
    broken_count = len([i for i in issues if i["type"] == "broken_quest_link"])
    placeholder_count = len([i for i in issues if i["type"] == "placeholder"])
    low_quality_count = len([i for i in issues if i["type"] == "quality"])
    
    if issues:
        print(f"\nFound {len(issues)} issues:")
        # Print critical/broken first
        for issue in issues:
            if issue['type'] in ['broken_quest_link', 'placeholder', 'world_minimum_failure']:
                print(f"  - [{issue['type'].upper()}] {issue['message']}")
        
        if args.fail_on_low_quality and low_quality_count > 0:
             print(f"  - [QUALITY] {low_quality_count} files failed Tier-1 quality checks (use --tier 1 to enforce).")
            
    success = True
    if args.fail_on_broken and broken_count > 0:
        print("FAIL: Broken links detected.")
        success = False
    if args.fail_on_placeholders and placeholder_count > 0:
        print("FAIL: Placeholders detected.")
        success = False
    if args.fail_on_low_quality and low_quality_count > 0:
         # Only fail if --fail-on-low-quality matches the issue type "quality" which comes from build_codex_map logic
         # But wait, build_codex_map always adds them?
         # I modified build_codex_map to add "quality" type issues regardless of flag?
         # Yes. So here we check count.
         print("FAIL: Low quality content detected.")
         success = False
    
    if min_failures:
        print("FAIL: World minimums not met.")
        for msg in min_failures:
            print(f"  - {msg}")
        success = False

    critical_issues = [i for i in issues if i['type'] not in ('broken_quest_link', 'placeholder', 'quality', 'world_minimum_failure')]
    if critical_issues:
        print("FAIL: Critical structural issues found (loops, duplicates, parse errors).")
        for i in critical_issues:
             print(f"  - {i['message']}")
        sys.exit(1)
        
    if not success:
        sys.exit(1)
        
    print(f"Codex is consistent (or ignored according to flags). Scanned {len(files)} files.")
    sys.exit(0)

if __name__ == "__main__":
    main()
