
import subprocess
import sys
import os
import requests

def run_cmd(cmd):
    print(f"🚀 Running: {cmd}")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    
    ret = subprocess.run(cmd, shell=True, env=env)
    if ret.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        sys.exit(ret.returncode)

def check_quest_count(world_id, min_count):
    print(f"🔍 Verifying quest count for {world_id} (via API, min: {min_count})...")
    try:
        resp = requests.get(f"http://127.0.0.1:8092/api/quests?world={world_id}", timeout=5)
        resp.raise_for_status()
        quests = resp.json()
        count = len(quests)
        if count < min_count:
            print(f"❌ Verification Failed: {world_id} has {count} quests, expected >= {min_count}")
            sys.exit(1)
        print(f"✅ Pass: {world_id} has {count} quests")
    except Exception as e:
        print(f"❌ API Check Failed: {e}")
        # warning only if api is down? No, this is integrity check, fail hard.
        sys.exit(1)

def main():
    print("🛡️  Starting DB Integrity Check (Release Gate)...")
    
    # 1. Seed DB
    run_cmd("python scripts/questpack_seed.py --all")
    
    # 2. Check Counts
    check_quest_count("world-python", 8) # Tier-2 targets (might be more)
    check_quest_count("world-js", 10) 
    check_quest_count("world-typescript", 10)
    
    # 3. Audit Content Integrity
    worlds = ["world-python", "world-js", "world-typescript"]
    for w in worlds:
        print(f"\n🌍 Verifying {w} content via API...")
        run_cmd(f"python scripts/codex_audit_missing.py --world {w} --source api")
        run_cmd(f"python scripts/categorize_coverage_buckets.py --world {w}")
    
    print("\n✅ DB Integrity Check Passed! Application state matches expectations.")

if __name__ == "__main__":
    main()
