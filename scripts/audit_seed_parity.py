import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from arcade_app.seed_quests_standard_worlds import STANDARD_QUESTLINES
from scripts.utils_questpacks import get_all_quest_slugs

def audit_seed_parity():
    """
    Audit consistency between:
    1. Seed configuration (STANDARD_QUESTLINES)
    2. Questpacks (data/questpacks/*.json)
    3. On-disk Quests (data/quests/<slug>)
    """
    print("🌱 Auditing Seed Parity...")
    
    # 1. Get all quests from Questpacks
    pack_slugs = get_all_quest_slugs()
    print(f"Found {len(pack_slugs)} quests in questpacks.")
    
    # 2. Get all quests from Seed Config
    seed_slugs = set()
    for q in STANDARD_QUESTLINES:
        seed_slugs.add(q.get("slug"))
        
    print(f"Found {len(seed_slugs)} quests in seed config.")
    
    failures = []
    
    # 3. Check Seed -> Disk
    # Every seeded quest MUST exist on disk
    for slug in seed_slugs:
        # Check workspace
        ws_path = Path(f"data/quests/{slug}/workspace")
        if not ws_path.exists():
            failures.append(f"Seeded quest {slug} missing workspace: {ws_path}")
            
    # 4. Check Pack -> Disk
    # Every pack quest MUST exist on disk (workspace or docs)
    for slug in pack_slugs:
        # Modern path
        ws_path = Path(f"data/quests/{slug}/workspace")
        # Docs path (legacy definitions)
        docs_path = Path(f"docs/quests/{slug}/quest.json")
        
        if not ws_path.exists() and not docs_path.exists():
             failures.append(f"Pack quest {slug} missing from disk userspace.")

    # 5. Check Seed -> Pack coverage
    # Are all seeded quests in packs? (Should be)
    missing_in_packs = seed_slugs - pack_slugs
    if missing_in_packs:
        print(f"[WARN] {len(missing_in_packs)} seeded quests not in any questpack: {missing_in_packs}")
        # This might be fine if they are dev-only?
        
    # 6. Check Pack -> Seed coverage
    # Are all pack quests seeded?
    # This is the big gap. Currently only 16 are seeded.
    missing_in_seed = pack_slugs - seed_slugs
    if missing_in_seed:
        print(f"[INFO] {len(missing_in_seed)} pack quests are NOT in seed config (Legacy/Generated).")
        # failures.append(f"Pack quest {slug} not seeded.") 
        # We don't fail on this yet, as we know we have legacy quests.
        
    if failures:
        print("\n[STOP] SEED PARITY FAILED")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    else:
        print("\n[OK] SEED PARITY PASSED (Basic checks)")
        sys.exit(0)

if __name__ == "__main__":
    audit_seed_parity()
