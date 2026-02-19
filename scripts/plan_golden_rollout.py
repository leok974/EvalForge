import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from scripts.utils_questpacks import get_all_quest_slugs

def plan_golden_rollout():
    print("📋 Planning Golden Rollout...")
    
    all_slugs = get_all_quest_slugs()
    missing_golden = []
    
    for slug in all_slugs:
        grading_dir = Path(f"data/quests/{slug}/grading")
        has_run = (grading_dir / "golden.run.json").exists() or (grading_dir / "golden.json").exists()
        has_state = (grading_dir / "golden.state.json").exists()
        has_spec = (grading_dir / "golden.spec.json").exists()
        
        if not (has_run or has_state or has_spec):
            # Check world
            world = "unknown"
            if "py" in slug or "python" in slug: world = "python"
            elif "js" in slug or "ts" in slug: world = "js"
            elif "ml" in slug: world = "ml"
            elif "sql" in slug: world = "sql"
            elif "git" in slug: world = "git"
            elif "infra" in slug: world = "infra"
            elif "agent" in slug: world = "agents"
            
            missing_missing = {
                "slug": slug,
                "world": world
            }
            missing_golden.append(missing_missing)
            
    # Sort by priority
    # Python -> JS -> ML -> SQL -> Git/Infra -> Others
    priority_map = {
        "python": 1,
        "js": 2,
        "ml": 3,
        "sql": 4,
        "git": 5,
        "infra": 5,
        "agents": 6,
        "unknown": 7
    }
    
    missing_golden.sort(key=lambda x: (priority_map.get(x["world"], 99), x["slug"]))
    
    print(f"Found {len(missing_golden)} quests missing golden artifacts.")
    
    # Write plan
    out_path = Path("docs/audits/GOLDEN_ROLLOUT_PLAN.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(missing_golden, f, indent=4)
        
    print(f"✅ Plan saved to {out_path}")
    
    # Print summary
    from collections import Counter
    counts = Counter(m["world"] for m in missing_golden)
    for w, c in counts.most_common():
        print(f"- {w}: {c}")

if __name__ == "__main__":
    plan_golden_rollout()
