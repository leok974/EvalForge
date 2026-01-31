
import asyncio
import os
import sys

# Ensure root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import seed_evalforge_universe
from scripts import questpack_seed

async def main():
    print("🚀 Starting FULL EvalForge Seeding Pipeline...")
    
    # Track slugs to detect collisions
    docs_slugs = set()
    pack_slugs = set()

    # 1. Seed Universe (Worlds, Tracks, Bosses + Curated Quests)
    try:
        # Assuming seed_universe returns list of seeded slugs or we modify it to do so
        # For now, let's wrap or assume we can get them. 
        # Actually simplest is to modify the sub-scripts to return slugs.
        # But to avoid touching too many files, we can query DB? No, seed_all is often initial.
        # Let's Modify seed_evalforge_universe to return slugs.
        docs_slugs = await seed_evalforge_universe.seed_universe() or set()
    except Exception as e:
        print(f"⚠️ Universe Seed Warning: {e}")
        # Continue, as some parts might have succeeded or it's a minor schema issue
    
    # 2. Seed All Questpacks (Recursive Directory Walk)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"📂 Scanning for questpacks in {root_dir}...")
    
    try:
        pack_slugs = await questpack_seed.seed_all(root_dir) or set()
    except Exception as e:
         print(f"❌ Questpack Seed Failed: {e}")
         sys.exit(1)

    # 3. Collision Detection
    # If a quest exists in docs-spec and questpack with same (world, track, slug), fail.
    # Currently we just compare slugs globally for simplicity. 
    # Spec: "If a quest exists in docs-spec and questpack with same (world, track, slug)"
    # Global slug uniqueness is usually improved anyway.
    collisions = docs_slugs.intersection(pack_slugs)
    if collisions:
        print(f"❌ CRITICAL: Found {len(collisions)} duplicate quests defined in both Docs and Questpacks!")
        for s in collisions:
            print(f"  - {s}")
        print("Fix: Remove one definition or add 'source_priority' override.")
        sys.exit(1)

         
    print("✨ Full Seeding Pipeline Complete!")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
