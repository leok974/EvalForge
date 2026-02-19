import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from scripts.utils_questpacks import get_all_quest_slugs
from scripts.audit_objectives_schema import audit_all_quests

def generate_backfill_queue():
    print("📋 Generating Backfill Queue...")
    
    # 1. Audit Objectives
    obj_report = audit_all_quests()
    invalid_slugs = set(q['slug'] for q in obj_report['invalid_quests'])
    no_obj_slugs = set(obj_report['quests_with_no_objectives'])
    
    # 2. Audit Golden
    golden_missing_slugs = set()
    all_slugs = get_all_quest_slugs()
    
    for slug in all_slugs:
        grading_dir = Path(f"data/quests/{slug}/grading")
        has_run = (grading_dir / "golden.run.json").exists() or (grading_dir / "golden.json").exists()
        has_state = (grading_dir / "golden.state.json").exists()
        has_spec = (grading_dir / "golden.spec.json").exists()
        
        if not (has_run or has_state or has_spec):
            golden_missing_slugs.add(slug)
            
    # 3. Categorize
    overlap = invalid_slugs.intersection(golden_missing_slugs)
    invalid_only = invalid_slugs - overlap
    golden_only = golden_missing_slugs - overlap
    
    # 4. Generate Report
    md = f"# Phase I Backfill Queue\n\nTotal Quests: {len(all_slugs)}\n\n"
    
    md += f"## A3) HIGH PRIORITY: Overlap (Invalid Objectives + Missing Golden) ({len(overlap)})\n"
    md += "These quests are broken in multiple ways.\n\n"
    for slug in sorted(overlap):
        md += f"- [ ] `{slug}`\n"
        
    md += f"\n## A1) Invalid Objectives Only ({len(invalid_only)})\n"
    md += "These have valid golden artifacts but invalid objective schemas.\n\n"
    for slug in sorted(invalid_only):
         md += f"- [ ] `{slug}`\n"
         
    md += f"\n## A2) Missing Golden Only ({len(golden_only)})\n"
    md += "These have valid objectives (likely seeded) but match no golden artifacts.\n\n"
    for slug in sorted(golden_only):
        md += f"- [ ] `{slug}`\n"
        
    md += f"\n## No Objectives ({len(no_obj_slugs)})\n"
    for slug in sorted(no_obj_slugs):
        md += f"- [ ] `{slug}`\n"

    # Write
    out_path = Path("docs/audits/PHASE_I_BACKFILL_QUEUE.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
        
    print(f"✅ Report generated: {out_path}")
    print(f"- Overlap: {len(overlap)}")
    print(f"- Invalid Only: {len(invalid_only)}")
    print(f"- Golden Only: {len(golden_only)}")

if __name__ == "__main__":
    generate_backfill_queue()
