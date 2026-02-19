#!/usr/bin/env python3
"""
Golden Coverage Audit - Track which quests have golden captures.

Checks:
1. golden.run.json exists (preferred - actual solution run)
2. golden.spec.json exists (fallback - spec-based expectations)
3. Neither exists (FAIL - no golden capture at all)

Outputs:
- docs/audits/GOLDEN_COVERAGE_AUDIT.md
- docs/audits/GOLDEN_COVERAGE_AUDIT.json
- docs/audits/GOLDEN_BLOCKERS.md (spec-only quests + blockers)

Exit codes:
- 0: All quests have golden artifacts (run or spec)
- 1: Some quests missing golden captures
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from scripts.utils_questpacks import get_all_quest_slugs

def audit_golden_coverage():
    """Audit all quests for golden capture coverage."""
    report = {
        "audit_date": datetime.now().isoformat(),
        "total_quests": 0,
        "quests_with_golden_run": [],
        "quests_with_golden_spec": [],
        "quests_missing_golden": [],
        "summary": {}
    }
    
    all_slugs = sorted(list(get_all_quest_slugs()))
    
    for slug in all_slugs:
        # Determine world from questpack metadata if possible? 
        # For now, we just list slug.
        world_id = "unknown" # Could improve this if needed
        report["total_quests"] += 1
        
        quest_dir = Path(f"data/quests/{slug}/grading")
        golden_run = quest_dir / "golden.run.json"
        golden_state = quest_dir / "golden.state.json"
        golden_spec = quest_dir / "golden.spec.json"
        
        # Check regular golden.json (from previous implementation)
        golden_legacy = quest_dir / "golden.json"
        
        if golden_run.exists():
            report["quests_with_golden_run"].append({
                "slug": slug,
                "world": world_id,
                "path": str(golden_run)
            })
        elif golden_state.exists():
            report["quests_with_golden_run"].append({
                "slug": slug,
                "world": world_id,
                "path": str(golden_state),
                "type": "state"
            })
        elif golden_legacy.exists():
            # Treat legacy golden.json as golden.run for now
            report["quests_with_golden_run"].append({
                "slug": slug,
                "world": world_id,
                "path": str(golden_legacy),
                "note": "using legacy golden.json (should migrate to golden.run.json)"
            })
        elif golden_spec.exists():
            # Load spec to get blocker info
            try:
                with open(golden_spec) as f:
                    spec_data = json.load(f)
                report["quests_with_golden_spec"].append({
                    "slug": slug,
                    "world": world_id,
                    "blocked_reason": spec_data.get("blocked_reason", "unknown"),
                    "required_fixtures": spec_data.get("required_fixtures", []),
                    "path": str(golden_spec)
                })
            except Exception as e:
                report["quests_with_golden_spec"].append({
                    "slug": slug,
                    "world": world_id,
                    "error": f"Failed to parse golden.spec.json: {e}",
                    "path": str(golden_spec)
                })
        else:
            report["quests_missing_golden"].append({
                "slug": slug,
                "world": world_id
            })
    
    # Summary
    report["summary"] = {
        "total_quests": report["total_quests"],
        "with_golden_run": len(report["quests_with_golden_run"]),
        "with_golden_spec": len(report["quests_with_golden_spec"]),
        "missing_golden": len(report["quests_missing_golden"]),
        "status": "PASS" if not report["quests_missing_golden"] else "FAIL"
    }
    
    return report

def generate_markdown_report(report: dict) -> str:
    """Generate markdown audit report."""
    status_emoji = "✅" if report["summary"]["status"] == "PASS" else "⚠️"
    
    md = f"""# Golden Coverage Audit Report

**Date:** {report['audit_date']}  
**Status:** {status_emoji} {report['summary']['status']}

## Summary

- **Total Quests:** {report['total_quests']}
- **With golden.run.json:** {report['summary']['with_golden_run']} ✅
- **With golden.spec.json only:** {report['summary']['with_golden_spec']} 📋
- **Missing golden capture:** {report['summary']['missing_golden']} ❌

---

"""
    
    if report['summary']['status'] == "PASS":
        md += "## ✅ All Quests Have Golden Captures!\n\n"
    
    # Golden run quests
    if report['quests_with_golden_run']:
        md += f"## ✅ Quests with Golden Run Captures ({len(report['quests_with_golden_run'])})\n\n"
        md += "These quests have actual solution runs captured:\n\n"
        for quest in report['quests_with_golden_run']:
            note = quest.get('note', '')
            note_str = f" ({note})" if note else ""
            md += f"- **{quest['slug']}** (World: {quest['world']}){note_str}\n"
        md += "\n---\n\n"
    
    # Golden spec quests (blockers)
    if report['quests_with_golden_spec']:
        md += f"## 📋 Quests with Golden Spec Only ({len(report['quests_with_golden_spec'])})\n\n"
        md += "These quests are blocked from golden run capture:\n\n"
        for quest in report['quests_with_golden_spec']:
            md += f"### {quest['slug']} (World: {quest['world']})\n\n"
            if 'error' in quest:
                md += f"❌ **Error:** {quest['error']}\n\n"
            else:
                md += f"**Blocked Reason:** {quest.get('blocked_reason', 'unknown')}\n\n"
                fixtures = quest.get('required_fixtures', [])
                if fixtures:
                    md += "**Required Fixtures:**\n"
                    for fixture in fixtures:
                        md += f"- `{fixture}`\n"
                    md += "\n"
                md += f"**Path:** `{quest['path']}`\n\n"
        md += "See [GOLDEN_BLOCKERS.md](GOLDEN_BLOCKERS.md) for resolution plan.\n\n"
        md += "---\n\n"
    
    # Missing golden
    if report['quests_missing_golden']:
        md += f"## ❌ Quests Missing Golden Capture ({len(report['quests_missing_golden'])})\n\n"
        md += "**CRITICAL:** These quests have NO golden capture (neither run nor spec):\n\n"
        for quest in report['quests_missing_golden']:
            md += f"- **{quest['slug']}** (World: {quest['world']})\n"
        md += "\n"
    
    return md

def generate_blockers_doc(report: dict) -> str:
    """Generate blockers documentation."""
    spec_quests = report['quests_with_golden_spec']
    
    if not spec_quests:
        return """# Golden Capture Blockers

**Status:** All quests have golden.run.json captures! 🎉

No blockers to resolve.
"""
    
    md = f"""# Golden Capture Blockers

**Date:** {report['audit_date']}

This document tracks quests that only have `golden.spec.json` (spec-based expectations) instead of `golden.run.json` (actual solution runs).

## Summary

- **Total Spec-Only Quests:** {len(spec_quests)}
- **Goal:** Convert all to golden.run.json

---

"""
    
    for quest in spec_quests:
        slug = quest['slug']
        world = quest['world']
        blocked_reason = quest.get('blocked_reason', 'unknown')
        fixtures = quest.get('required_fixtures', [])
        
        md += f"## {slug}\n\n"
        md += f"**World:** {world}  \n"
        md += f"**Blocked Reason:** {blocked_reason}\n\n"
        
        if fixtures:
            md += "**Required Fixtures:**\n"
            for fixture in fixtures:
                md += f"- `{fixture}`\n"
            md += "\n"
        
        md += "**Resolution Steps:**\n"
        if "fixture" in blocked_reason.lower():
            md += "1. Update `code_runner.py` to include fixtures in temp workspace\n"
            md += "2. Re-run `capture_golden_stdout.py --slug " + slug + "`\n"
            md += "3. Verify golden.run.json created\n"
            md += "4. Delete golden.spec.json\n"
        else:
            md += "1. Fix solution file\n"
            md += "2. Re-capture with `capture_golden_stdout.py --slug " + slug + "`\n"
            md += "3. Delete golden.spec.json\n"
        md += "\n**Status:** ⏳ Pending\n\n---\n\n"
    
    return md

if __name__ == "__main__":
    print("📊 Auditing golden capture coverage...")
    
    # Ensure audit directory exists
    Path("docs/audits").mkdir(parents=True, exist_ok=True)
    
    # Run audit
    report = audit_golden_coverage()
    
    # Generate JSON
    json_path = "docs/audits/GOLDEN_COVERAGE_AUDIT.json"
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"📄 JSON report: {json_path}")
    
    # Generate Markdown
    md = generate_markdown_report(report)
    md_path = "docs/audits/GOLDEN_COVERAGE_AUDIT.md"
    with open(md_path, "w", encoding='utf-8') as f:
        f.write(md)
    print(f"📄 Markdown report: {md_path}")
    
    # Generate Blockers doc
    blockers = generate_blockers_doc(report)
    blockers_path = "docs/audits/GOLDEN_BLOCKERS.md"
    with open(blockers_path, "w", encoding='utf-8') as f:
        f.write(blockers)
    print(f"📄 Blockers doc: {blockers_path}")
    
    # Print summary
    print(f"\n{'-'*60}")
    print(f"Status: {report['summary']['status']}")
    print(f"Golden Run: {report['summary']['with_golden_run']}/{report['total_quests']} quests")
    print(f"Golden Spec (blockers): {report['summary']['with_golden_spec']}")
    print(f"Missing: {report['summary']['missing_golden']}")
    print(f"{'-'*60}")
    
    # Exit code - only fail if completely missing
    has_errors = report['summary']['status'] == "FAIL"
    sys.exit(1 if has_errors else 0)
