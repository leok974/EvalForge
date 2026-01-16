
import asyncio
import httpx
import sys
import os
import json

# Add root to pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

BASE_URL = "http://localhost:8000"
HEADERS = {"x-dev-user": "smoke-tester"}

async def smoke_test_quest(quest_id):
    print(f"🔥 Smoking quest: {quest_id}...")
    
    # 1. Get Quest (Verify it exists + config loaded)
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        res = await client.get(f"/api/quests/{quest_id}", headers=HEADERS)
        if res.status_code != 200:
            print(f"  ❌ Failed to fetch quest: {res.status_code}")
            return False
            
        quest_data = res.json()
        print(f"  ✅ Quest loaded: {quest_data['title']}")
        
        # Check if config present in response (optional, depending on API exposure)
        # Assuming we just rely on running it.

        # 2. Run Starter Code (Expect Fail usually, unless designed to pass)
        print("  Running starter code...")
        starter_code = quest_data.get("starter_code", "")
        if not starter_code:
             print("  ⚠️ No starter_code in API response (did seed run?)")
             # Try to infer or skip
             return False

        res = await client.post(
            f"/api/quests/{quest_id}/run",
            json={"code": starter_code, "language": "python", "mode": "execute"},
            headers=HEADERS
        )
        
        if res.status_code != 200:
            print(f"  ❌ Run failed: {res.text}")
            return False
            
        run_data = res.json()
        print(f"  Run Result: Passed={run_data['passed']}")
        
        # Verify objectives are being checked
        objs = run_data.get("objective_results", [])
        if not objs:
             print("  ❌ No objective results returned (validator not wired?)")
             return False
        
        print(f"  Objectives: {[o['id'] for o in objs]}")
        
        # 3. Verify 'Generic' Validator is Working
        # If we see ids from our JSON config, it works.
        # e.g., 'tminus', 'liftoff'
        json_ids = {'main', 'tminus', 'liftoff', 'var_msg', 'print_msg'} # heuristic
        found_ids = {o['id'] for o in objs}
        
        overlap = json_ids.intersection(found_ids)
        if not overlap and len(json_ids) > 0:
             print(f"  ⚠️ Warning: Returned objectives {found_ids} don't match expected set {json_ids}")
        else:
             print(f"  ✅ Validator returned expected objectives: {overlap}")

        return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--quest_id", required=True)
    parser.add_argument("--base_url", default="http://localhost:8000")
    args = parser.parse_args()
    
    BASE_URL = args.base_url
    asyncio.run(smoke_test_quest(args.quest_id))
