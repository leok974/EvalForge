
import asyncio
import httpx
import sys

BASE_URL = "http://localhost:8000"
# Use a test user
HEADERS = {"x-dev-user": "test-user-progress-v2"}
QUEST_SLUG = "first-sparks"

async def test_progress_flow():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        print("1. Check Initial Progress...")
        res = await client.get("/api/profile/progress", headers=HEADERS)
        if res.status_code != 200:
            print(f"Failed to get progress: {res.text}")
            return
        
        initial_progress = res.json()
        print(f"Initial: {len(initial_progress['quests'])} quests started.")

        print("2. Submit Quest Solution...")
        # Valid code for first-sparks
        code = """
print("Hello, World!")
"""
        res = await client.post(
            f"/api/quests/{QUEST_SLUG}/submit",
            json={"code": code},
            headers=HEADERS
        )
        if res.status_code != 200:
            print(f"Submit failed: {res.text}")
            sys.exit(1)
            
        submit_data = res.json()
        print(f"Submit Result: passed={submit_data['passed']}, xp={submit_data['xp_awarded']}")
        assert submit_data['passed'] == True
        
        print("3. Verify Progress Update...")
        res = await client.get("/api/profile/progress", headers=HEADERS)
        updated_progress = res.json()
        
        # Find our quest
        quest_prog = next((q for q in updated_progress['quests'] if q['quest_id'] == QUEST_SLUG), None)
        if not quest_prog:
            print("❌ Quest progress NOT found in profile!")
            sys.exit(1)
            
        print(f"Quest Status: {quest_prog['status']}")
        print(f"Quest Attempts: {quest_prog['attempts_count']}")
        
        if quest_prog['status'] not in ("completed", "mastered"):
            print("❌ Status wrong!")
            sys.exit(1)
            
        if quest_prog['attempts_count'] < 1:
             print("❌ Attempts count wrong!")
             sys.exit(1)

        print("✅ Backend Progress Flow Verified!")

if __name__ == "__main__":
    asyncio.run(test_progress_flow())
