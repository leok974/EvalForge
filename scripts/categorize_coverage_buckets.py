#!/usr/bin/env python3
"""
Categorize quests into coverage buckets for world sprint analysis.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List


def categorize_into_buckets(coverage_data: Dict, world_filter: str = None) -> Dict:
    """Categorize quests into coverage buckets.
    
    Args:
        coverage_data: Full coverage JSON from audit
        world_filter: Optional world prefix to filter slugs (e.g., 'python' matches 'python-ignition')
    
    Buckets:
    - A (None): score = 0
    - B (Partial): 0 < score < 70
    - C (Good): 70 <= score < 90
    - D (Excellent): >= 90
    """
    coverage_by_quest = coverage_data.get("coverage_by_quest", {})
    
    buckets = {
        "none": [],
        "partial": [],
        "good": [],
        "excellent": []
    }
    
    for slug, metrics in coverage_by_quest.items():
        # Filter by world if specified (match slug prefix)
        if world_filter:
            # Handle both "python" and "world-python" filters
            filter_normalized = world_filter.replace("world-", "")
            if not slug.startswith(filter_normalized):
                continue
            
        score = metrics.get("coverage_score", 0)
        
        quest_info = {
            "slug": slug,
            "score": score,
            "has_tutorial": metrics.get("has_tutorial", False),
            "tutorial_length": metrics.get("tutorial_length", 0),
            "terms_total": metrics.get("terms_total", 0),
            "terms_with_ref": metrics.get("terms_with_codex_ref", 0),
            "codex_refs_total": metrics.get("codex_refs_total", 0),
        }
        
        if score == 0:
            buckets["none"].append(quest_info)
        elif score < 70:
            buckets["partial"].append(quest_info)
        elif score < 90:
            buckets["good"].append(quest_info)
        else:
            buckets["excellent"].append(quest_info)
    
    return buckets


def generate_buckets_report(buckets: Dict, world_id: str = None) -> str:
    """Generate markdown report of buckets."""
    world_label = f"{world_id} " if world_id else ""
    
    md = f"""# {world_label.title()}Coverage Buckets

**Total Quests:** {sum(len(b) for b in buckets.values())}

## Summary

- **Bucket A (None):** {len(buckets['none'])} quests (score = 0)
- **Bucket B (Partial):** {len(buckets['partial'])} quests (0 < score < 70)
- **Bucket C (Good):** {len(buckets['good'])} quests (70 ≤ score < 90)
- **Bucket D (Excellent):** {len(buckets['excellent'])} quests (score ≥ 90)

---

## Bucket A: None (Priority for Tier-1 Backfill)

These quests need immediate baseline coverage.

| Slug | Tutorial | Terms | Codex Refs | Issue |
|------|----------|-------|------------|-------|
"""
    
    for quest in buckets["none"]:
        issue = []
        if not quest["has_tutorial"]:
            issue.append("No tutorial")
        if quest["terms_total"] == 0:
            issue.append("No terms")
        if quest["codex_refs_total"] == 0:
            issue.append("No refs")
        
        md += f"| `{quest['slug']}` | {'✅' if quest['has_tutorial'] else '❌'} | {quest['terms_total']} | {quest['codex_refs_total']} | {', '.join(issue)} |\n"
    
    md += f"""

---

## Bucket B: Partial (Needs refinement)

These quests have some coverage but need improvement.

| Slug | Score | Tutorial | Terms | Codex Refs |
|------|-------|----------|-------|------------|
"""
    
    for quest in buckets["partial"][:20]:  # Show top 20
        md += f"| `{quest['slug']}` | {quest['score']} | {'✅' if quest['has_tutorial'] else '❌'} | {quest['terms_total']} ({quest['terms_with_ref']} linked) | {quest['codex_refs_total']} |\n"
    
    if len(buckets["partial"]) > 20:
        md += f"\n*...and {len(buckets['partial']) - 20} more*\n"
    
    md += f"""

---

## Bucket C: Good (Main path candidates)

These quests have solid coverage.

| Slug | Score | Terms | Codex Refs |
|------|-------|-------|------------|
"""
    
    for quest in buckets["good"][:10]:
        md += f"| `{quest['slug']}` | {quest['score']} | {quest['terms_total']} | {quest['codex_refs_total']} |\n"
    
    md += f"""

---

## Bucket D: Excellent (Golden examples)

These quests demonstrate full coverage.

| Slug | Score | Terms | Codex Refs |
|------|-------|-------|------------|
"""
    
    for quest in buckets["excellent"]:
        md += f"| `{quest['slug']}` | {quest['score']} | {quest['terms_total']} | {quest['codex_refs_total']} |\n"
    
    return md


def main():
    parser = argparse.ArgumentParser(description="Categorize quests into coverage buckets")
    parser.add_argument("--coverage-file", default="artifacts/codex-missing.json", help="Coverage JSON file")
    parser.add_argument("--world", help="Filter by world ID (e.g., 'world-python')")
    parser.add_argument("--out", help="Output JSON file (default: artifacts/world-{world}-buckets.json)")
    parser.add_argument("--md", help="Output Markdown file (default: artifacts/world-{world}-buckets.md)")
    args = parser.parse_args()
    
    # Load coverage data
    with open(args.coverage_file, 'r', encoding='utf-8') as f:
        coverage_data = json.load(f)
    
    # Categorize
    buckets = categorize_into_buckets(coverage_data, args.world)
    
    # Determine output paths
    world_suffix = args.world.replace("world-", "") if args.world else "all"
    json_out = args.out if args.out else f"artifacts/world-{world_suffix}-buckets.json"
    md_out = args.md if args.md else f"artifacts/world-{world_suffix}-buckets.md"
    
    # Write JSON
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump(buckets, f, indent=2)
    print(f"📄 JSON buckets: {json_out}")
    
    # Write Markdown
    md = generate_buckets_report(buckets, args.world)
    with open(md_out, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"📄 Markdown buckets: {md_out}")
    
    # Summary
    print(f"\n✅ Bucket summary for {args.world or 'all quests'}:")
    print(f"   - None (A): {len(buckets['none'])}")
    print(f"   - Partial (B): {len(buckets['partial'])}")
    print(f"   - Good (C): {len(buckets['good'])}")
    print(f"   - Excellent (D): {len(buckets['excellent'])}")


if __name__ == "__main__":
    main()
