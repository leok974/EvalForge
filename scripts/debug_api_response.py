
import asyncio
import httpx
import os
import sys

# Add root to path so we can import arcade_app
sys.path.append(os.getcwd())

from arcade_app.services.quest_visibility import get_active_quest_config

async def check_api():
    print("--- DEBUGGING QUEST VISIBILITY ---")
    
    # 1. Check Internal Service Logic
    try:
        active_slugs, active_packs = get_active_quest_config()
        print(f"✅ Service: Loaded {len(active_slugs)} active slugs.")
        print(f"   Sample: {list(active_slugs)[:5]}")
        
        target_slugs = ["first-sparks", "hello-variable"]
        for slug in target_slugs:
            status = "✅ FOUND" if slug in active_slugs else "❌ MISSING"
            print(f"   Target '{slug}': {status}")
    except Exception as e:
        print(f"❌ Service: Failed to load config: {e}")
        import traceback
        traceback.print_exc()

    # 2. Check Live API (Default)
    async with httpx.AsyncClient() as client:
        try:
            # Try Docker internal port if running inside container, else localhost
            # But here we are running ON HOST (likely), so localhost:8092
            url = "http://localhost:8092/api/quests"
            print(f"👉 Requesting: {url}")
            res = await client.get(url)
            print(f"   Status: {res.status_code}")
            if res.status_code == 200:
                quests = res.json()
                print(f"   Count: {len(quests)}")
                if len(quests) > 0:
                     print(f"   Sample: {[q['slug'] for q in quests[:3]]}")
            else:
                 print(f"   Error: {res.text}")
        except Exception as e:
             print(f"❌ API Request Failed: {e}")

    # 3. Check Live API (Admin)
    async with httpx.AsyncClient() as client:
        try:
            url = "http://localhost:8092/api/quests?include_inactive=true"
            print(f"👉 Requesting (Admin): {url}")
            res = await client.get(url)
            print(f"   Status: {res.status_code}")
            if res.status_code == 200:
                quests = res.json()
                print(f"   Count: {len(quests)}")
        except Exception as e:
             print(f"❌ API Request Failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_api())
