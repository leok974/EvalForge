
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
        return quests  # Return for further checks
    except Exception as e:
        print(f"❌ API Check Failed: {e}")
        # warning only if api is down? No, this is integrity check, fail hard.
        sys.exit(1)

def check_web_tracks():
    """Ensure Web world has balanced HTML and CSS tracks (10+10 minimum)."""
    print(f"🔍 Verifying Web world track balance...")
    try:
        resp = requests.get(f"http://127.0.0.1:8092/api/quests?world=world-web", timeout=5)
        resp.raise_for_status()
        quests = resp.json()
        
        html_count = sum(1 for q in quests if q.get('slug', '').startswith('html-'))
        css_count = sum(1 for q in quests if q.get('slug', '').startswith('css-'))
        
        if html_count < 10:
            print(f"❌ HTML Track incomplete: {html_count}/10 quests")
            sys.exit(1)
        
        if css_count < 10:
            print(f"❌ CSS Track incomplete: {css_count}/10 quests")
            sys.exit(1)
        
        print(f"✅ Pass: HTML Track has {html_count} quests, CSS Track has {css_count} quests")
    except Exception as e:
        print(f"❌ Track verification failed: {e}")
        sys.exit(1)

def main():
    print("🛡️  Starting DB Integrity Check (Release Gate)...")
    
    # 1. Seed DB
    run_cmd("python scripts/questpack_seed.py --all")
    
    # 2. Check Counts
    check_quest_count("world-python", 8) # Tier-2 targets (might be more)
    check_quest_count("world-js", 10) 
    check_quest_count("world-typescript", 10)
    check_quest_count("world-sql", 10)
    check_quest_count("world-git", 10)
    check_quest_count("world-infra", 10)
    check_quest_count("world-ml", 10)
    check_quest_count("world-agents", 10)
    check_quest_count("world-web", 20)
    
    # 2.5. Check Web world track balance (10 HTML + 10 CSS)
    check_web_tracks()
    
    # 3. Audit Content Integrity
    worlds = ["world-python", "world-js", "world-typescript", "world-sql", "world-git", "world-infra", "world-ml", "world-agents", "world-web"]
    for w in worlds:
        print(f"\n🌍 Verifying {w} content via API...")
        run_cmd(f"python scripts/codex_audit_missing.py --world {w} --source api")
        run_cmd(f"python scripts/categorize_coverage_buckets.py --world {w}")
    
    print("\n✅ DB Integrity Check Passed! Application state matches expectations.")

if __name__ == "__main__":
    main()
