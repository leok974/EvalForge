#!/usr/bin/env python3
"""
Codex Coverage Audit Tool

Scans all quests and reports missing Codex glossary entries.
"""

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict

import requests
import frontmatter


# ==================== CONFIGURATION ====================

CODEX_DIR = Path("data/codex")
ARTIFACTS_DIR = Path("artifacts")

# Starter quests that must meet strict coverage requirements
STARTER_QUESTS = [
    "python-ignition",
    "ts-first-contact",
    "js-hello-prism",
    "sql-select-basics",
    "git-init-commit",
]

# Policy: Minimum requirements for starter quests
STARTER_POLICY = {
    "require_tutorial": True,
    "min_tutorial_length": 100,
    "min_terms": 2,
    "require_all_terms_linked": True,
    "min_coverage_score": 70,
}


# ==================== REFERENCE RESOLVER ====================

def codex_ref_to_path(ref: str) -> Optional[str]:
    """
    Resolve a codex reference to a file path.
    
    Resolution Strategy:
    1. **Path format (preferred)**: "glossary/python/interpreter"
       Maps to: "data/codex/glossary/python/interpreter.md"
       This mirrors the nested directory structure.
    
    2. **Flat format (legacy)**: "glossary-python-interpreter"
       Maps to: "data/codex/glossary-python-interpreter.md"
       Only supported if file exists at this exact path.
    
    3. **Frontmatter ID lookup**: If neither path exists, searches all
       Codex files for a matching `id` field in YAML frontmatter.
    
    Args:
        ref: Codex reference (with or without "codex:" prefix)
    
    Returns:
        Resolved file path or None if invalid/unresolvable
    
    Warning:
        Flat format is NOT recommended for new entries. Use path format
        with explicit frontmatter `id` for flexibility.
    """
    if not ref:
        return None
    
    # Remove "codex:" prefix if present
    if ref.startswith("codex:"):
        ref = ref[6:]
    
    # Skip special refs
    if ref in ["home", ""]:
        return None
    
    # Validate characters (alphanumeric, /, -, _)
    if not re.match(r'^[a-zA-Z0-9/_\-]+$', ref):
        return None
    
    # Check for path format (contains /)
    if "/" in ref:
        path = CODEX_DIR / f"{ref}.md"
        return str(path)
    
    # Check for flat format (contains -)
    if "-" in ref:
        path = CODEX_DIR / f"{ref}.md"
        return str(path)
    
    # Single word ref
    path = CODEX_DIR / f"{ref}.md"
    return str(path)


def find_codex_file_by_id(ref_id: str) -> Optional[str]:
    """
    Find a Codex file by checking frontmatter 'id' field.
    This handles cases where files are named differently than their IDs.
    """
    ref_id_clean = ref_id.replace("codex:", "")
    
    for root, _, files in os.walk(CODEX_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    post = frontmatter.load(path)
                    if post.metadata.get("id") == ref_id_clean:
                        return path
                except:
                    continue
    return None


def check_ref_exists(ref: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a codex reference exists.
    Returns (exists: bool, resolved_path: Optional[str])
    """
    # Try direct path resolution
    path = codex_ref_to_path(ref)
    if path and os.path.exists(path):
        return True, path
    
    # Try frontmatter ID lookup
    path = find_codex_file_by_id(ref)
    if path:
        return True, path
    
    return False, path


# ==================== API CLIENT ====================

class QuestAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
    
    def fetch_quests(self) -> List[Dict]:
        """Fetch all quests from /api/quests endpoint."""
        try:
            resp = requests.get(f"{self.base_url}/api/quests", timeout=60)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"  ❌ Error fetching quests: {e}")
            return []
    
    def fetch_quest_detail(self, slug: str) -> Optional[Dict]:
        """Fetch full quest details from /api/quests/{slug}."""
        try:
            resp = requests.get(f"{self.base_url}/api/quests/{slug}", timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"  ⚠️  Error fetching quest {slug}: {e}")
            return None


# ==================== DISK CLIENT ====================

class DiskClient:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        
    def fetch_quests(self) -> List[Dict]:
        """Scan docs/quests and data/questpacks (simulated API response)."""
        quests = []
        
        # 1. Scan docs/quests (Authoring source of truth)
        docs_dir = os.path.join(self.root_dir, "docs", "quests")
        if os.path.exists(docs_dir):
            for slug in os.listdir(docs_dir):
                q_path = os.path.join(docs_dir, slug, "quest.json")
                if os.path.exists(q_path):
                    try:
                        with open(q_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            # Ensure slug is set
                            if "slug" not in data: data["slug"] = slug
                            quests.append(data)
                    except: pass
                    
        return quests

    def fetch_quest_detail(self, slug: str) -> Optional[Dict]:
        """Load full quest details from disk."""
        # 1. Try docs/quests/{slug}
        q_dir = os.path.join(self.root_dir, "docs", "quests", slug)
        q_json = os.path.join(q_dir, "quest.json")
        
        if not os.path.exists(q_json):
            return None
            
        try:
            with open(q_json, "r", encoding="utf-8") as f:
                quest = json.load(f)
        except:
            return None
            
        # Hydrate text files
        tut_path = os.path.join(q_dir, "tutorial.md")
        if os.path.exists(tut_path):
            with open(tut_path, "r", encoding="utf-8") as f:
                quest["tutorial_md"] = f.read()
                
        terms_path = os.path.join(q_dir, "terms.json")
        if os.path.exists(terms_path):
             with open(terms_path, "r", encoding="utf-8") as f:
                 quest["key_terms"] = json.load(f)
                 
        return quest


# ==================== REFERENCE COLLECTOR ====================

def extract_codex_refs(quest: Dict) -> Set[str]:
    """Extract all codex references from a quest."""
    refs = set()
    
    # key_terms[].codex_ref
    for term in quest.get("key_terms", []):
        if term.get("codex_ref"):
            refs.add(term["codex_ref"])
    
    # codex_references[]
    for ref in quest.get("codex_references", []):
        if ref:
            refs.add(ref)
    
    # tutorial_md inline refs (codex:...)
    tutorial_md = quest.get("tutorial_md", "")
    if tutorial_md:
        matches = re.findall(r'codex:([a-zA-Z0-9/_\-]+)', tutorial_md)
        for match in matches:
            refs.add(f"codex:{match}")
    
    return refs


# ==================== AUDIT ENGINE ====================

def calculate_coverage(quest: Dict, refs: Set[str]) -> Dict:
    """Calculate coverage metrics for a single quest."""
    tutorial_md = quest.get("tutorial_md", "")
    key_terms = quest.get("key_terms", [])
    codex_references = quest.get("codex_references", [])
    
    has_tutorial = bool(tutorial_md and len(tutorial_md.strip()) > 0)
    tutorial_length = len(tutorial_md) if tutorial_md else 0
    has_terms = len(key_terms) > 0
    terms_total = len(key_terms)
    terms_with_codex_ref = sum(1 for t in key_terms if t.get("codex_ref"))
    codex_refs_total = len(refs)
    unique_codex_refs = len(refs)
    
    # Calculate coverage score (0-100)
    # Factors: has tutorial (30%), has terms (20%), term linkage (50%)
    score = 0.0
    if has_tutorial:
        score += 30.0
    if has_terms:
        score += 20.0
    if terms_total > 0:
        score += 50.0 * (terms_with_codex_ref / terms_total)
    
    return {
        "has_tutorial": has_tutorial,
        "tutorial_length": tutorial_length,
        "has_terms": has_terms,
        "terms_total": terms_total,
        "terms_with_codex_ref": terms_with_codex_ref,
        "codex_refs_total": codex_refs_total,
        "unique_codex_refs": unique_codex_refs,
        "coverage_score": round(score, 1)
    }


def validate_quest_policy(slug: str, quest: Dict, coverage: Dict) -> List[str]:
    """Validate quest against policy requirements.
    
    Args:
        slug: Quest slug
        quest: Quest data
        coverage: Coverage metrics from calculate_coverage()
    
    Returns:
        List of policy violation messages (empty if compliant)
    """
    violations = []
    is_starter = slug in STARTER_QUESTS
    
    if not is_starter:
        return violations  # Only enforce on starters for now
    
    policy = STARTER_POLICY
    
    # Check tutorial requirements
    if policy["require_tutorial"] and not coverage["has_tutorial"]:
        violations.append(f"Missing tutorial (required for starters)")
    elif coverage["tutorial_length"] < policy["min_tutorial_length"]:
        violations.append(f"Tutorial too short: {coverage['tutorial_length']} chars (min: {policy['min_tutorial_length']})")
    
    # Check terms requirements
    if coverage["terms_total"] < policy["min_terms"]:
        violations.append(f"Too few terms: {coverage['terms_total']} (min: {policy['min_terms']})")
    
    # Check term linkage
    if policy["require_all_terms_linked"] and coverage["terms_total"] > 0:
        if coverage["terms_with_codex_ref"] < coverage["terms_total"]:
            violations.append(f"Not all terms linked: {coverage['terms_with_codex_ref']}/{coverage['terms_total']} have codex_ref")
    
    # Check coverage score
    if coverage["coverage_score"] < policy["min_coverage_score"]:
        violations.append(f"Coverage score too low: {coverage['coverage_score']}/100 (min: {policy['min_coverage_score']})")
    
    return violations


def audit_quests(base_url: str, world_id: Optional[str] = None, source: str = "api", root_dir: str = None) -> Dict:
    """Main audit logic.
    
    Args:
        base_url: API base URL
        world_id: Optional world ID to filter quests (e.g., 'world-python')
        source: 'api' or 'disk'
    """
    if source == "disk":
        print(f"💾 Using Disk Client (Root: {root_dir})")
        client = DiskClient(root_dir)
    else:
        print(f"🌐 Using API Client ({base_url})")
        client = QuestAPIClient(base_url)
    
    print("📊 Fetching quest list...")
    quest_summaries = client.fetch_quests()
    
    # Filter by world if specified
    if world_id:
        quest_summaries = [q for q in quest_summaries if q.get("world_id") == world_id]
        print(f"✅ Found {len(quest_summaries)} quests in {world_id}")
    else:
        print(f"✅ Found {len(quest_summaries)} quests")
    
    # Data structures
    all_refs = set()
    missing_by_ref = defaultdict(lambda: {"path": None, "quests": []})
    missing_by_quest = defaultdict(lambda: {"missing": [], "invalid": []})
    invalid_refs = defaultdict(list)
    quests_with_missing = set()
    
    # Coverage tracking
    coverage_by_quest = {}
    quests_no_tutorial = []
    quests_empty_tutorial = []
    quests_no_terms = []
    quests_no_codex_refs = []
    total_coverage_score = 0.0
    
    # Policy violations
    policy_violations = {}  # {slug: [violation messages]}
    
    print("\n🔍 Scanning quests for codex references...")
    for summary in quest_summaries:
        slug = summary.get("slug")
        if not slug:
            continue
        
        # Fetch full details
        quest = client.fetch_quest_detail(slug)
        if not quest:
            continue
        
        # Extract refs
        refs = extract_codex_refs(quest)
        all_refs.update(refs)
        
        # Calculate coverage
        coverage = calculate_coverage(quest, refs)
        coverage_by_quest[slug] = coverage
        total_coverage_score += coverage["coverage_score"]
        
        # Track coverage gaps
        if not coverage["has_tutorial"]:
            quests_no_tutorial.append(slug)
        elif coverage["tutorial_length"] == 0:
            quests_empty_tutorial.append(slug)
        
        if not coverage["has_terms"]:
            quests_no_terms.append(slug)
        
        if coverage["codex_refs_total"] == 0:
            quests_no_codex_refs.append(slug)
        
        # Validate policy
        violations = validate_quest_policy(slug, quest, coverage)
        if violations:
            policy_violations[slug] = violations
        
        # Check each ref
        for ref in refs:
            exists, path = check_ref_exists(ref)
            
            if not path:
                # Invalid ref (couldn't resolve)
                invalid_refs[ref].append(slug)
                missing_by_quest[slug]["invalid"].append(ref)
                continue
            
            if not exists:
                # Missing file
                missing_by_ref[ref]["path"] = path
                missing_by_ref[ref]["quests"].append(slug)
                missing_by_quest[slug]["missing"].append(ref)
                quests_with_missing.add(slug)
    
    print(f"✅ Scanned {len(quest_summaries)} quests")
    
    # Compute counts
    unique_refs = len(all_refs)
    missing_unique_refs = len(missing_by_ref)
    invalid_unique_refs = len(invalid_refs)
    avg_coverage = total_coverage_score / len(quest_summaries) if quest_summaries else 0.0
    
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {
            "quests_scanned": len(quest_summaries),
            "total_refs": len(all_refs),
            "unique_refs": unique_refs,
            "missing_unique_refs": missing_unique_refs,
            "invalid_unique_refs": invalid_unique_refs,
            "quests_with_missing": len(quests_with_missing),
        },
        "coverage": {
            "average_score": round(avg_coverage, 1),
            "quests_no_tutorial": len(quests_no_tutorial),
            "quests_empty_tutorial": len(quests_empty_tutorial),
            "quests_no_terms": len(quests_no_terms),
            "quests_no_codex_refs": len(quests_no_codex_refs),
            "quests_with_full_coverage": sum(1 for c in coverage_by_quest.values() if c["coverage_score"] >= 90),
        },
        "policy": {
            "violations_count": len(policy_violations),
            "violations_by_quest": policy_violations,
            "starters_scanned": sum(1 for summary in quest_summaries if summary.get("slug") in STARTER_QUESTS),
            "starters_compliant": sum(1 for summary in quest_summaries if summary.get("slug") in STARTER_QUESTS and summary.get("slug") not in policy_violations),
        },
        "coverage_by_quest": coverage_by_quest,
        "missing_by_ref": dict(missing_by_ref),
        "missing_by_quest": {k: v for k, v in missing_by_quest.items() if v["missing"] or v["invalid"]},
        "invalid_refs": dict(invalid_refs),
        "gaps": {
            "no_tutorial": quests_no_tutorial[:10],  # Top 10
            "no_terms": quests_no_terms[:10],
            "no_codex_refs": quests_no_codex_refs[:10],
        }
    }


# ==================== REPORT GENERATORS ====================

def generate_markdown_report(data: Dict) -> str:
    """Generate human-readable Markdown report."""
    counts = data["counts"]
    coverage = data.get("coverage", {})
    gaps = data.get("gaps", {})
    
    # Calculate coverage percentage
    coverage_pct = (counts["unique_refs"] / counts["quests_scanned"] * 100) if counts["quests_scanned"] > 0 else 0
    zero_coverage_pct = (coverage.get('quests_no_codex_refs', 0) / counts['quests_scanned'] * 100) if counts['quests_scanned'] > 0 else 0.0
    
    md = f"""# Codex Coverage Audit Report

**Generated:** {data['generated_at']}

## Executive Summary

- **Coverage:** {coverage_pct:.1f}% ({counts['unique_refs']} refs across {counts['quests_scanned']} quests)
- **Average Coverage Score:** {coverage.get('average_score', 0)}/ 100
- **Quests with Full Coverage (≥90):** {coverage.get('quests_with_full_coverage', 0)}
- **Quests with Zero Coverage:** {coverage.get('quests_no_codex_refs', 0)} ({zero_coverage_pct:.1f}%)
- **Invalid Refs:** {counts['invalid_unique_refs']}
- **Missing Refs:** {counts['missing_unique_refs']}

---

## Coverage Gaps

### Top Issues

1. **{coverage.get('quests_no_tutorial', 0)} quests have NO tutorial**
2. **{coverage.get('quests_no_terms', 0)} quests have NO terms**
3. **{coverage.get('quests_no_codex_refs', 0)} quests have NO codex refs**

### Sample Uncovered Quests

**No Tutorial:**
"""
    
    for quest in gaps.get("no_tutorial", [])[:5]:
        md += f"- `{quest}`\n"
    
    md += "\n**No Terms:**\n"
    for quest in gaps.get("no_terms", [])[:5]:
        md += f"- `{quest}`\n"
    
    md += "\n**No Codex Refs:**\n"
    for quest in gaps.get("no_codex_refs", [])[:5]:
        md += f"- `{quest}`\n"
    
    md += "\n---\n\n## Policy Violations\n\n"
    
    policy = data.get("policy", {})
    violations_by_quest = policy.get("violations_by_quest", {})
    
    md += f"**Starter Quests:** {policy.get('starters_scanned', 0)} scanned, "
    md += f"{policy.get('starters_compliant', 0)} compliant, "
    md += f"{policy.get('violations_count', 0)} violations\n\n"
    
    if violations_by_quest:
        for quest_slug, violations in sorted(violations_by_quest.items()):
            md += f"### ❌ `{quest_slug}` (Starter)\n\n"
            for v in violations:
                md += f"- {v}\n"
            md += "\n"
    else:
        md += "*All starter quests meet policy requirements!* ✅\n"
    
    md += "\n---\n\n## Top Missing References (by frequency)\n\n"
    
    # Sort by number of quests referencing
    missing_sorted = sorted(
        data["missing_by_ref"].items(),
        key=lambda x: len(x[1]["quests"]),
        reverse=True
    )
    
    if missing_sorted:
        md += "| Reference | Path | Quests Affected |\n"
        md += "|-----------|------|----------------|\n"
        for ref, info in missing_sorted[:20]:  # Top 20
            quests_str = ", ".join(info["quests"][:3])
            if len(info["quests"]) > 3:
                quests_str += f" (+{len(info['quests']) - 3} more)"
            md += f"| `{ref}` | `{info['path']}` | {quests_str} |\n"
    else:
        md += "*No missing references found!* ✅\n"
    
    md += "\n---\n\n## Quests with Missing References\n\n"
    
    if data["missing_by_quest"]:
        for quest_slug, info in sorted(data["missing_by_quest"].items()):
            if info["missing"]:
                md += f"### `{quest_slug}`\n\n"
                md += "**Missing:**\n"
                for ref in info["missing"]:
                    md += f"- `{ref}`\n"
                md += "\n"
    else:
        md += "*All quests have valid references!* ✅\n"
    
    md += "\n---\n\n## Invalid References\n\n"
    
    if data["invalid_refs"]:
        md += "These references could not be resolved to a file path:\n\n"
        for ref, quests in sorted(data["invalid_refs"].items()):
            md += f"- `{ref}` (in {len(quests)} quest(s))\n"
    else:
        md += "*No invalid references found!* ✅\n"
    
    return md


def write_stub_file(ref: str, path: str):
    """Create a stub Codex markdown file for a missing reference."""
    ref_clean = ref.replace("codex:", "")
    title = ref_clean.split("/")[-1].replace("-", " ").title()
    
    # Extract world if possible
    parts = ref_clean.split("/")
    world = parts[1].title() if len(parts) > 1 else "General"
    
    content = f"""---
id: {ref_clean}
title: {title}
section: Glossary
world: {world}
---

# {title}

**TODO:** Add content for this term.

## Overview

(Description needed)

## Examples

```python
# Example code here
```

## Related Terms

- (Add related terms)
"""
    
    # Create directories if needed
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✅ Created stub: {path}")


# ==================== CLI ====================

def main():
    parser = argparse.ArgumentParser(description="Audit Codex coverage across quests")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8092",
        help="Backend API base URL"
    )
    parser.add_argument(
        "--world",
        help="Filter quests by world ID (e.g., 'world-python', 'world-typescript')"
    )
    parser.add_argument(
        "--source",
        choices=["api", "disk"],
        default="api",
        help="Source of truth (api=backend, disk=filesystem)"
    )
    parser.add_argument(
        "--out",
        help="Custom path for JSON output (default: artifacts/codex-missing.json)"
    )
    parser.add_argument(
        "--md",
        help="Custom path for Markdown output (default: artifacts/codex-missing.md)"
    )
    parser.add_argument(
        "--write-stubs",
        action="store_true",
        help="Automatically create stub Codex files for missing refs"
    )
    args = parser.parse_args()
    
    # Ensure artifacts dir exists
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    
    # Run audit
    print(f"🚀 Starting Codex audit (Source: {args.source})\n")
    data = audit_quests(args.base_url, world_id=args.world, source=args.source, root_dir=os.getcwd())
    
    # Determine output paths
    json_out = args.out if args.out else ARTIFACTS_DIR / "codex-missing.json"
    md_out = args.md if args.md else ARTIFACTS_DIR / "codex-missing.md"
    
    # Write JSON
    print(f"\n📄 JSON report: {json_out}")
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    # Write Markdown
    md = generate_markdown_report(data)
    print(f"📄 Markdown report: {md_out}")
    with open(md_out, "w", encoding="utf-8") as f:
        f.write(md)
    
    # Create stubs if requested
    if args.write_stubs and data["counts"]["missing_unique_refs"] > 0:
        print(f"\n✍️ Creating stub Codex files for {data['counts']['missing_unique_refs']} missing refs...")
        for ref in data.get("missing", []):
            create_stub_codex_file(ref)
        print("✅ Stubs created")
    
    # Summary
    counts = data["counts"]
    print(f"\n✅ Audit complete!")
    print(f"   - {counts['missing_unique_refs']} missing references")
    print(f"   - {counts['invalid_unique_refs']} invalid references")
    print(f"   - {counts['quests_with_missing']} quests affected")


if __name__ == "__main__":
    main()
