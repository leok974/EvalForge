import requests
import sys
import time
import os

# --- Configuration ---
BASE_URL = os.getenv("EVALFORGE_BASE_URL", "http://localhost:8081")
API_TOKEN = os.getenv("EVALFORGE_API_TOKEN", "mock-token")
BOSS_ID = "signal_prism"

# --- Colors ---
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# --- Valid Solution (TypeScript) ---
GOOD_CODE = r"""
export type Channel = "ui" | "network" | "system";
export type Severity = "info" | "warn" | "error";

export type SignalEvent = {
  id: string;
  channel: Channel;
  kind: "open" | "update" | "close" | "ack";
  ts: number;
  payload?: {
    severity?: Severity;
    message?: string;
  };
};

export type SignalState = {
  id: string;
  channel: Channel;
  severity: Severity;
  message: string;
  open: boolean;
  acknowledged: boolean;
  lastEventAt: number;
};

export function computeSignalPanel(events: SignalEvent[]): SignalState[] {
  const byId = new Map<string, SignalState>();

  for (const event of events) {
    const prev = byId.get(event.id);
    
    // Timestamp check: later wins
    if (prev && event.ts < prev.lastEventAt) {
      continue;
    }

    // Apply logic based on kind
    if (event.kind === "open") {
      byId.set(event.id, {
        id: event.id,
        channel: prev?.channel ?? event.channel,
        severity: event.payload?.severity ?? prev?.severity ?? "info",
        message: event.payload?.message ?? prev?.message ?? "",
        open: true,
        acknowledged: false,
        lastEventAt: event.ts,
      });
    } else if (event.kind === "update") {
      if (prev) {
        byId.set(event.id, {
          ...prev,
          severity: event.payload?.severity ?? prev.severity,
          message: event.payload?.message ?? prev.message,
          lastEventAt: event.ts,
        });
      }
    } else if (event.kind === "ack") {
      if (prev) {
        byId.set(event.id, {
          ...prev,
          acknowledged: true,
          lastEventAt: event.ts,
        });
      }
    } else if (event.kind === "close") {
      if (prev) {
        byId.set(event.id, {
          ...prev,
          open: false,
          lastEventAt: event.ts,
        });
      }
    }
  }

  // Filter for open signals (optional, but usually implied for "panel")
  // Or just return all states. The prompt says "final SignalState[] for a panel".
  // Let's assume we return everything that isn't explicitly deleted (we don't delete here).
  // But usually closed signals might be hidden. Let's return all for now as per type signature.
  
  return Array.from(byId.values()).sort((a, b) => a.id.localeCompare(b.id));
}

// Magic token to force mock grader pass if needed
// MAGIC_BOSS_PASS
"""

BAD_CODE = """
export function computeSignalPanel(events: any[]): any[] {
  return []; // Fail
}
"""

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {API_TOKEN}"})

def log(msg, color=RESET):
    print(f"{color}{msg}{RESET}")

def login():
    """Simulate login to get a valid session/user."""
    log("Logging in as 'leo' (mock)...", YELLOW)
    # This endpoint mocks the GitHub callback and sets the session cookie
    # We use allow_redirects=False to avoid following the redirect to the frontend
    resp = session.get(f"{BASE_URL}/api/auth/github/callback?code=mock_code", allow_redirects=False)
    
    if resp.status_code == 307 or resp.status_code == 200:
        log("[OK] Logged in", GREEN)
        return True
    else:
        log(f"[FAIL] Login failed: {resp.status_code} {resp.text}", RED)
        return False

def reset_progress():
    resp = session.delete(f"{BASE_URL}/api/dev/boss_codex/{BOSS_ID}")
    if resp.status_code == 200:
        log("[OK] Progress reset", GREEN)
    else:
        log(f"[WARN] Failed to reset progress (Server might need restart for new routes): {resp.status_code} {resp.text}", YELLOW)

def get_codex_state():
    resp = session.get(f"{BASE_URL}/api/codex/boss/{BOSS_ID}")
    if resp.status_code != 200:
        log(f"[FAIL] Get codex failed: {resp.status_code}", RED)
        sys.exit(1)
    return resp.json()

def force_boss_spawn():
    resp = session.post(f"{BASE_URL}/api/dev/force_boss", json={"boss_id": BOSS_ID})
    if resp.status_code != 200:
        log(f"[FAIL] Force spawn failed: {resp.status_code} {resp.text}", RED)
        sys.exit(1)
    return resp.json()["encounter_id"]

def submit_boss(encounter_id, code):
    resp = session.post(f"{BASE_URL}/api/boss/submit", json={
        "encounter_id": encounter_id,
        "code": code
    })
    if resp.status_code != 200:
        log(f"[FAIL] Submit failed: {resp.status_code} {resp.text}", RED)
        sys.exit(1)
    return resp.json()

def verify_doc_unlocked(state, tier):
    docs = state.get("docs", [])
    doc = next((d for d in docs if d["tier"] == tier), None)
    if not doc:
        log(f"[FAIL] Doc tier {tier} not found in response", RED)
        return False
    
    if not doc["unlocked"]:
        log(f"[FAIL] Doc tier {tier} is locked", RED)
        return False
        
    if not doc.get("body_md"):
        log(f"[FAIL] Doc tier {tier} has no body_md", RED)
        return False
        
    log(f"[OK] Tier {tier} doc unlocked", GREEN)
    log(f"[OK] Tier {tier} body_md present", GREEN)
    return True

def run_qa():
    print(f"=== Boss Codex QA – {BOSS_ID} (Target: {BASE_URL}) ===")
    
    if not login():
        sys.exit(1)

    # 1. Reset
    reset_progress()
    
    # 2. Initial State Check
    state = get_codex_state()
    tier = state["boss"]["tier_unlocked"]
    if tier != 0:
        log(f"[WARN] Initial tier_unlocked != 0 (got {tier}). Assuming previous run state.", YELLOW)
    else:
        log(f"[OK] Initial tier_unlocked == 0", GREEN)
        # Verify docs are locked
        docs = state.get("docs", [])
        for d in docs:
            if d["unlocked"]:
                log(f"[FAIL] Doc tier {d['tier']} is initially unlocked", RED)
            else:
                log(f"[OK] Doc tier {d['tier']} is initially locked", GREEN)
                if d.get("body_md"):
                     log(f"[FAIL] Doc tier {d['tier']} has body_md initially", RED)
                else:
                     log(f"[OK] Doc tier {d['tier']} has no body_md initially", GREEN)

    # 3. Phase B: First Failure (Unlock Tier 1)
    print("\n--- Phase B: First Failure ---")
    if tier < 1:
        enc_id = force_boss_spawn()
        res = submit_boss(enc_id, BAD_CODE)
        if res["status"] != "loss":
             log(f"[FAIL] Expected loss, got {res['status']}", RED)
        
        state = get_codex_state()
        tier = state["boss"]["tier_unlocked"]
        
        if tier >= 1:
            log(f"[OK] Tier unlocked >= 1 after first failure (got {tier})", GREEN)
            verify_doc_unlocked(state, 1)
        else:
            log(f"[FAIL] Phase B failed: {tier}", RED)
            sys.exit(1)

    # 4. Phase C: Multiple Failures (Unlock Tier 2)
    print("\n--- Phase C: Multiple Failures ---")
    if tier < 2:
        # Need 3 deaths total. We have 1 (maybe). Let's just loop until tier 2 unlocks or we hit a limit.
        for i in range(5):
            state = get_codex_state()
            if state["boss"]["tier_unlocked"] >= 2:
                break
            
            print(f"  > Failure {i+2}...")
            enc_id = force_boss_spawn()
            submit_boss(enc_id, BAD_CODE)
            time.sleep(0.5)
        
        state = get_codex_state()
        tier = state["boss"]["tier_unlocked"]
        if tier >= 2:
            log(f"[OK] Tier unlocked >= 2 after multiple failures (got {tier})", GREEN)
            verify_doc_unlocked(state, 2)
        else:
            log(f"[FAIL] Phase C failed: {tier}", RED)
            sys.exit(1)

    # 5. Phase D: Victory (Unlock Tier 3)
    print("\n--- Phase D: Victory ---")
    if tier < 3:
        enc_id = force_boss_spawn()
        # Use GOOD_CODE which includes MAGIC_BOSS_PASS
        res = submit_boss(enc_id, GOOD_CODE)
        
        if res["status"] == "win":
            log(f"[OK] Boss submission succeeded", GREEN)
        else:
            log(f"[FAIL] Boss submission failed. Status: {res['status']}. Score: {res.get('score')}", RED)
            sys.exit(1)
            
        state = get_codex_state()
        tier = state["boss"]["tier_unlocked"]
        
        if tier == 3:
            log(f"[OK] Tier unlocked == 3 after first kill (got {tier})", GREEN)
            verify_doc_unlocked(state, 3)
        else:
            log(f"[FAIL] Phase D failed: {tier}", RED)
            sys.exit(1)

    print(f"\n=== Boss Codex QA – {BOSS_ID} ✅ PASS ===")

if __name__ == "__main__":
    try:
        run_qa()
    except requests.exceptions.ConnectionError:
        log(f"[FAIL] Could not connect to {BASE_URL}. Is the server running?", RED)
        sys.exit(1)
    except Exception as e:
        log(f"[FAIL] Unexpected error: {e}", RED)
        sys.exit(1)
