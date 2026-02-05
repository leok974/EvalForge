
import json
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text

# Add root to pythonpath
sys.path.append(os.getcwd())

from arcade_app.database import DATABASE_URL

def load_active_slugs(root_dir: Path):
    config_path = root_dir / "configs" / "questpacks_active.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    active_slugs = set()
    questpacks = config.get("active_questpacks", [])
    
    print(f"Loading {len(questpacks)} active questpacks...")
    for pack_rel in questpacks:
        pack_path = root_dir / pack_rel
        if not pack_path.exists():
            print(f"  ⚠️ Missing pack: {pack_path}")
            continue
            
        with open(pack_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        quests = []
        if isinstance(data, list): quests = data
        elif isinstance(data, dict):
            if "packs" in data: quests = data["packs"]
            elif "quests" in data: quests = data["quests"]
            elif "slug" in data: quests = [data]
            
        for q in quests:
            slug = q.get("slug")
            # Handle external
            if not slug and "quest_path" in q:
                q_dir = root_dir / q["quest_path"]
                q_json = q_dir / "quest.json"
                if q_json.exists():
                    try:
                        with open(q_json, "r") as qf:
                            slug = json.load(qf).get("slug")
                    except: pass
            
            if slug:
                active_slugs.add(slug)
                
    return active_slugs

def get_db_slugs():
    # Force sync driver for this script
    sync_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    engine = create_engine(sync_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT slug FROM questdefinition"))
        return {row[0] for row in result}

def main():
    root = Path(os.getcwd())
    
    print("🔍 Auditing Quest Visibility...")
    
    # 1. Active Set
    active = load_active_slugs(root)
    print(f"✅ Active Config: {len(active)} quests")
    
    # 2. DB Set
    db_slugs = get_db_slugs()
    print(f"🗄️  Database:     {len(db_slugs)} quests")
    
    # 3. Disk Scan (Basic)
    disk_slugs = {p.name for p in (root / "data" / "quests").iterdir() if p.is_dir()}
    print(f"📂 Disk Folders: {len(disk_slugs)} folders")
    
    # Analysis
    extra_in_db = db_slugs - active
    missing_in_db = active - db_slugs
    
    print("\n--- REPORT ---")
    
    if missing_in_db:
        print(f"\n⚠️  MISSING from DB ({len(missing_in_db)}):")
        for s in list(missing_in_db)[:10]:
            print(f"  - {s}")
            
    if extra_in_db:
        print(f"\n🚫 LEAKING in DB ({len(extra_in_db)}) [Should be hidden]:")
        for s in sorted(list(extra_in_db)):
            print(f"  - {s}")
            
    # Check specific canary
    canary = "quest-py-hidden"
    print(f"\n--- CANARY CHECK: {canary} ---")
    print(f"  In Config: {'YES' if canary in active else 'NO'}")
    print(f"  In DB:     {'YES' if canary in db_slugs else 'NO'}")
    
    if canary in db_slugs and canary not in active:
        print("\n❌ CRITICAL: Canary quest is visible in DB but NOT in active config!")
    elif canary not in db_slugs:
        print("\n⚠️  Canary quest is missing from DB entirely (needs seeding for CI?)")
    else:
        print("\n✅ Canary quest status is consistent.")

if __name__ == "__main__":
    main()
