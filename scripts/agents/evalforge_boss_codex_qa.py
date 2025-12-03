import os
import sys
import requests
import time

# Configuration
BASE_URL = os.environ.get("EVALFORGE_BASE_URL", "http://localhost:8081")
API_TOKEN = os.environ.get("EVALFORGE_API_TOKEN", "dev-token-placeholder")

session = requests.Session()
session.cookies.set("session_token", API_TOKEN)

def assert_true(condition, msg):
    if not condition:
        print(f"[FAIL] {msg}")
        sys.exit(1)
    print(f"[OK] {msg}")

def login():
    print("Logging in as 'leo' (mock)...")
    r = session.get(f"{BASE_URL}/api/auth/github/callback?code=mock_code", allow_redirects=False)
    # 307 is expected
    if r.status_code not in [200, 307]:
        r.raise_for_status()
    print("[OK] Logged in")

def get_boss_codex():
    r = session.get(f"{BASE_URL}/api/codex/boss/boss-reactor-core")
    if r.status_code == 401:
        print("[FAIL] Authentication failed. Please set EVALFORGE_API_TOKEN.")
        sys.exit(1)
    r.raise_for_status()
    return r.json()

def force_boss():
    r = session.post(f"{BASE_URL}/api/dev/force_boss", json={"boss_id": "boss-reactor-core"})
    r.raise_for_status()
    return r.json()

def accept_boss():
    r = session.post(f"{BASE_URL}/api/boss/accept", json={"boss_id": "boss-reactor-core"})
    r.raise_for_status()
    return r.json()

def submit_boss(code: str, encounter_id: int):
    r = session.post(f"{BASE_URL}/api/boss/submit", json={"encounter_id": encounter_id, "code": code})
    r.raise_for_status()
    return r.json()

def reset_progress():
    r = session.delete(f"{BASE_URL}/api/dev/boss_codex/boss-reactor-core")
    r.raise_for_status()
    print("[OK] Reset boss progress")

def qa_boss_codex():
    print(f"=== Boss Codex QA – Reactor Core (Target: {BASE_URL}) ===")

    # 0. Login (Seeds user 'leo')
    login()

    # 1. Reset State
    try:
        reset_progress()
    except Exception as e:
        print(f"[WARN] Failed to reset progress (Server might need restart for new routes): {e}")
        # We continue, but expect failures if state isn't clean
        pass

    # A: Initial state
    try:
        codex = get_boss_codex()
        tier = codex["boss"]["tier_unlocked"]
        # If we couldn't reset, tier might not be 0. We'll warn instead of fail for A.
        if tier != 0:
            print(f"[WARN] Initial tier_unlocked != 0 (got {tier}). Assuming previous run state.")
        else:
            print(f"[OK] Initial tier_unlocked == 0")
            
        for doc in codex["docs"]:
            if tier == 0:
                assert_true(doc["unlocked"] is False, f"Doc tier {doc['tier']} is initially locked")
                assert_true(doc["body_md"] is None, f"Doc tier {doc['tier']} has no body_md initially")
    except Exception as e:
        print(f"[FAIL] Failed to get initial codex state: {e}")
        sys.exit(1)

    # B: First failure → unlock Tier 1
    print("\n--- Phase B: First Failure ---")
    try:
        spawn_data = force_boss()
        enc_id = spawn_data["encounter_id"]
        submit_boss("def solve(x): raise Exception('bad')", enc_id)  # intentionally wrong

        codex = get_boss_codex()
        tier = codex["boss"]["tier_unlocked"]
        assert_true(tier >= 1, f"Tier unlocked >= 1 after first failure (got {tier})")
        tiers = {d["tier"]: d for d in codex["docs"]}
        assert_true(tiers[1]["unlocked"] is True, "Tier 1 doc unlocked after first failure")
        assert_true(tiers[1]["body_md"] is not None, "Tier 1 body_md present")
    except Exception as e:
        print(f"[FAIL] Phase B failed: {e}")
        sys.exit(1)

    # C: Multiple failures → unlock Tier 2
    print("\n--- Phase C: Multiple Failures ---")
    try:
        # We need 3 deaths total for Tier 2. We have 1 (or more if previous runs existed).
        # We'll just do 2 more to be safe.
        for i in range(2):
            print(f"  > Failure {i+2}...")
            spawn_data = force_boss()
            enc_id = spawn_data["encounter_id"]
            submit_boss("def solve(x): return None", enc_id)

        codex = get_boss_codex()
        tier = codex["boss"]["tier_unlocked"]
        assert_true(tier >= 2, f"Tier unlocked >= 2 after multiple failures (got {tier})")
        tiers = {d["tier"]: d for d in codex["docs"]}
        assert_true(tiers[2]["unlocked"] is True, "Tier 2 doc unlocked")
        assert_true(tiers[2]["body_md"] is not None, "Tier 2 body_md present")
    except Exception as e:
        print(f"[FAIL] Phase C failed: {e}")
        sys.exit(1)

    # D: Victory → unlock Tier 3
    print("\n--- Phase D: Victory ---")
    GOOD_CODE = """
def solve(payload):
    # MAGIC_BOSS_PASS
    return payload
"""
    try:
        spawn_data = force_boss()
        enc_id = spawn_data["encounter_id"]
        result = submit_boss(GOOD_CODE, enc_id)
        
        if result.get("status") != "win":
            print(f"[FAIL] Boss submission failed. Status: {result.get('status')}. Score: {result.get('score')}")
            sys.exit(1)
        
        assert_true(result.get("status") == "win", "Boss submission succeeded")

        codex = get_boss_codex()
        tier = codex["boss"]["tier_unlocked"]
        assert_true(tier == 3, f"Tier unlocked == 3 after first kill (got {tier})")
        tiers = {d["tier"]: d for d in codex["docs"]}
        assert_true(tiers[3]["unlocked"] is True, "Tier 3 doc unlocked")
        assert_true(tiers[3]["body_md"] is not None, "Tier 3 body_md present")
    except Exception as e:
        print(f"[FAIL] Phase D failed: {e}")
        sys.exit(1)

    print("\n=== Boss Codex QA – Reactor Core ✅ PASS ===")

if __name__ == "__main__":
    qa_boss_codex()
