
import requests
import sys

BASE_URL = "http://localhost:8092/api/quests"

def check_quest(slug):
    try:
        url = f"{BASE_URL}/{slug}"
        print(f"\n🔍 Checking {url}...")
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        briefing = data.get("briefing_md", "")
        lore = data.get("lore_md", "")
        objectives = data.get("objectives", []) or data.get("objectives_json", [])
        
        print(f"  📝 Briefing Start: {briefing[:60]!r}")
        print(f"  📜 Lore Start: {lore[:60]!r}")
        print(f"  🎯 Objectives ({len(objectives)}):")
        for o in objectives:
            text = o.get("text", "MISSING")
            print(f"     - {text}")
            
        if "Unknown Mission" in briefing:
            print("  ❌ FAIL: Briefing contains 'Unknown Mission'")
        if "Accessing archival data" in lore:
            print("  ❌ FAIL: Lore contains 'Accessing archival data'")
            
    except Exception as e:
        print(f"  🔥 API Error: {e}")

if __name__ == "__main__":
    slugs = ["hello-variable", "node-ignition", "infra-ignition", "cli-files-folders"]
    for s in slugs:
        check_quest(s)
