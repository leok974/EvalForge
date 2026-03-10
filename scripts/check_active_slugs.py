import os
from arcade_app.services.quest_visibility import get_active_quest_config

def check():
    active_slugs, slug_map = get_active_quest_config()
    print(f"Total active slugs: {len(active_slugs)}")
    print(f"sql-order-by in active_slugs: {'sql-order-by' in active_slugs}")
    
    # Find which pack it's in
    pack = slug_map.get("sql-order-by")
    print(f"sql-order-by is in pack: {pack}")

if __name__ == "__main__":
    check()
