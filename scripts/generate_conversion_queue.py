#!/usr/bin/env python3
"""
Generate Golden Run Conversion Queue.

Reads docs/audits/GOLDEN_COVERAGE_AUDIT.json and generates a prioritized queue of quests to convert to golden.run.json.
Checks for solution file existence to better diagnose blockers for missing quests.

Output: docs/audits/GOLDEN_RUN_CONVERSION_QUEUE.md
"""

import json
import os
from pathlib import Path
from datetime import datetime

AUDIT_JSON_PATH = Path("docs/audits/GOLDEN_COVERAGE_AUDIT.json")
QUEUE_MD_PATH = Path("docs/audits/GOLDEN_RUN_CONVERSION_QUEUE.md")

def check_solution_exists(slug: str) -> bool:
    """Check if a solution main.py exists."""
    # Assuming standard structure
    paths = [
        Path(f"data/quests/{slug}/solution/main.py"),
        Path(f"data/quests/{slug}/solution/task.py"), # Sometimes task.py is solution?
        Path(f"data/quests/{slug}/grading/solution.py"), # Legacy?
    ]
    for p in paths:
        if p.exists():
            return True
    return False

def generate_queue():
    if not AUDIT_JSON_PATH.exists():
        print(f"❌ Audit JSON not found at {AUDIT_JSON_PATH}. Run audit_golden_coverage.py first.")
        return

    with open(AUDIT_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    spec_only = data.get("quests_with_golden_spec", [])
    missing = data.get("quests_missing_golden", [])
    
    # Sort by slug
    spec_only.sort(key=lambda x: x["slug"])
    missing.sort(key=lambda x: x["slug"])

    md_lines = [
        "# Golden Run Conversion Queue",
        "",
        f"**Date:** {datetime.now().isoformat()}",
        "",
        "This queue prioritizes quests that need to be converted to `golden.run.json`.",
        "",
        "## 1. Spec-Only Quests (Blocked by Fixtures/Environment)",
        "",
        "These quests have `golden.spec.json` but failed run capture previously.",
        "",
        "| Quest Slug | World | Blocker | Fix Required |",
        "|---|---|---|---|",
    ]

    for q in spec_only:
        slug = q["slug"]
        world = q["world"]
        blocker = q.get("blocked_reason", "Unknown")
        fixtures = q.get("required_fixtures", [])
        
        fix = "Unknown"
        if "fixture" in blocker.lower() or fixtures:
            fix = "Materialize full workspace (Phase B)"
        elif "solution" in blocker.lower():
            fix = "Fix solution code"
            
        md_lines.append(f"| `{slug}` | {world} | {blocker} | {fix} |")

    md_lines.extend([
        "",
        "## 2. Missing Golden Quests (Needs Investigation)",
        "",
        "These quests have NO golden capture. Checking solution existence...",
        "",
        "| Quest Slug | World | Solution Exists? | Action |",
        "|---|---|---|---|",
    ])

    for q in missing:
        slug = q["slug"]
        world = q["world"]
        has_solution = check_solution_exists(slug)
        solution_status = "✅ Yes" if has_solution else "❌ No"
        action = "Run Batch Capture (Phase C)" if has_solution else "Write Solution Matcher"
        
        md_lines.append(f"| `{slug}` | {world} | {solution_status} | {action} |")

    md_lines.extend([
        "",
        "## progress Tracking",
        "",
        "- [ ] Phase B: Fix python-data-forge fixtures",
        "- [ ] Phase C: Run batch capture for unblocked",
        "- [ ] Phase D: Audit & Upgrade Objectives",
    ])

    with open(QUEUE_MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"✅ Generated Conversion Queue at {QUEUE_MD_PATH}")
    print(f"   - Spec Only: {len(spec_only)}")
    print(f"   - Missing: {len(missing)}")

if __name__ == "__main__":
    generate_queue()
