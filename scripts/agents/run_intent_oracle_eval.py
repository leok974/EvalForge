import os
import sys
import json
import requests
from pathlib import Path
from typing import Optional

BASE_URL = os.environ.get("EVALFORGE_BASE_URL", "http://localhost:8081")
API_TOKEN = os.environ.get("EVALFORGE_API_TOKEN")

if not API_TOKEN:
    # Fallback for local dev if not set, but warn
    # print("WARN: EVALFORGE_API_TOKEN not set, using mock-token", file=sys.stderr)
    API_TOKEN = "mock-token"

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {API_TOKEN}"})


def assert_true(cond, msg):
    if not cond:
        raise RuntimeError(msg)


def login():
    # Trigger mock login to ensure user 'leo' exists in DB
    # allow_redirects=False because we don't have a frontend running at 5173
    r = session.get(f"{BASE_URL}/api/auth/github/callback?code=mock_code", allow_redirects=False)
    # Expect 307 Temporary Redirect
    if r.status_code != 307:
        raise RuntimeError(f"Login failed: expected 307, got {r.status_code}")
    # The response sets a cookie, but session handles it. 
    # In mock mode, get_current_user just checks DB for 'leo', 
    # but hitting this endpoint creates 'leo' if missing.
    return r

def get_boss_info():
    r = session.get(f"{BASE_URL}/api/boss/current")
    r.raise_for_status()
    return r.json()


def force_intent_oracle():
    r = session.post(f"{BASE_URL}/api/dev/force_boss", json={"boss_id": "intent_oracle"})
    r.raise_for_status()
    return r.json()


def accept_boss():
    r = session.post(f"{BASE_URL}/api/boss/accept", json={"boss_id": "intent_oracle"})
    r.raise_for_status()
    return r.json()


def submit_boss(encounter_id: int, code: str):
    r = session.post(f"{BASE_URL}/api/boss/submit", json={"encounter_id": encounter_id, "code": code})
    r.raise_for_status()
    return r.json()


def load_candidate_code(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Candidate planner file not found: {path}")
    return p.read_text(encoding="utf-8")


def fetch_integrity() -> Optional[int]:
    """
    Try to read the current profile integrity from the backend.
    """
    try:
        r = session.get(f"{BASE_URL}/api/profile/me")
        r.raise_for_status()
        data = r.json()
        # Shape might be { "integrity": 100, ... } or { "profile": { "integrity": 100 } }
        if "integrity" in data:
            return data["integrity"]
        if "profile" in data and "integrity" in data["profile"]:
            return data["profile"]["integrity"]
    except Exception:
        return None
    return None


def fetch_boss_hp() -> Optional[int]:
    """
    Try to read the current boss HP from /api/boss/current.
    """
    try:
        data = get_boss_info()
        # Shape might be { "encounter": { "hp": 80 }, ... }
        enc = data.get("encounter") or data.get("state") or {}
        if isinstance(enc, dict) and "hp" in enc:
            return enc["hp"]
        if "hp" in data:
            return data["hp"]
    except Exception:
        return None
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: run_intent_oracle_eval.py path/to/candidate_planner.py", file=sys.stderr)
        sys.exit(1)

    candidate_path = sys.argv[1]
    try:
        code = load_candidate_code(candidate_path)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    try:
        # Ensure we are logged in (creates user in DB if needed)
        login()

        # Ensure we are evaluating the Intent Oracle boss
        force_intent_oracle()
        
        # Snapshot BEFORE
        integrity_before = fetch_integrity()
        boss_hp_before = fetch_boss_hp()

        accept_resp = accept_boss()
        eid = accept_resp["encounter_id"]
        
        # If we just started a fresh fight, boss HP might be full, 
        # but let's trust what we fetched or fetch again if needed.
        # Actually, accept_boss might reset HP, so maybe fetch boss HP *after* accept?
        # Let's fetch boss HP again after accept to be sure we have the starting HP of the *current* fight.
        boss_hp_before = fetch_boss_hp()

        result = submit_boss(eid, code)
        
        # Snapshot AFTER
        integrity_after = fetch_integrity()
        boss_hp_after = fetch_boss_hp()
        
        payload = {
            "boss_id": "intent_oracle",
            "success": result.get("status") == "win", # Map 'win' to boolean if needed, or keep string
            "score": result.get("score"),
            "raw": result,
            "rubric": result.get("rubric"), # Assuming submit_boss returns rubric
        }

        # Add deltas
        if integrity_before is not None and integrity_after is not None:
            payload["integrity_before"] = integrity_before
            payload["integrity_after"] = integrity_after
            payload["integrity_delta"] = integrity_after - integrity_before

        if boss_hp_before is not None and boss_hp_after is not None:
            payload["boss_hp_before"] = boss_hp_before
            payload["boss_hp_after"] = boss_hp_after
            payload["boss_hp_delta"] = boss_hp_after - boss_hp_before

        print(json.dumps(payload, indent=2))
        
    except Exception as e:
        # Print error as JSON so backend can parse it if possible, or at least stderr
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
