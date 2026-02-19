import argparse
import json
import subprocess
import sys
import re
from pathlib import Path

# --- Helpers ---

def strip_ansi(text: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def find_questpack_for_slug(slug: str) -> Path | None:
    base_dir = Path("data/questpacks")
    
    # Recursively find all json files
    candidates = list(base_dir.rglob("*.json"))
        
    for p in candidates:
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Legacy list format
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "quest_path" in item:
                        if Path(item["quest_path"]).name == slug:
                            return p
            
            # Modern dict format
            elif isinstance(data, dict):
                # Check "quests" list
                quests = data.get("quests", [])
                if isinstance(quests, list):
                    for q in quests:
                        if isinstance(q, dict) and q.get("slug") == slug:
                            return p
                        # Also check quest_path in modern dict
                        if isinstance(q, dict) and "quest_path" in q:
                             if Path(q["quest_path"]).name == slug:
                                return p
                # Check "entries" list (sometimes used)
                entries = data.get("entries", [])
                if isinstance(entries, list):
                    for q in entries:
                         if isinstance(q, dict) and q.get("slug") == slug:
                            return p

        except Exception:
            continue
            
    return None

def main():
    parser = argparse.ArgumentParser(description="Capture golden.run.json via unified runner")
    parser.add_argument("--slug", required=True, help="Quest slug to capture")
    
    args = parser.parse_args()
    slug = args.slug
    
    # 1. Find Questpack
    questpack = find_questpack_for_slug(slug)
    if not questpack:
        print(f"❌ Could not find questpack containing slug: {slug}")
        sys.exit(1)
        
    print(f"✅ Found questpack: {questpack}")
    
    # 2. Run via run_world_public_tests.mjs (The Unified Runner)
    # We use this because it handles dispatching to Python/Node/etc internally
    cmd = [
        "node",
        "scripts/run_world_public_tests.mjs",
        "--questpack", str(questpack),
        "--mode", "solution",
        "--only-slug", slug
    ]
    
    print(f"🚀 Running: {' '.join(cmd)}")
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8"
        # We don't verify return code immediately because we want to capture the output even if it failed?
        # Actually expected behavior for golden run is usually SUCCESS.
    )
    
    stdout_clean = strip_ansi(result.stdout)
    stderr_clean = strip_ansi(result.stderr)
    
    # 3. Construct Golden Data
    # Match the format of existing golden.run.json
    golden_data = {
        "exit_code": result.returncode,
        "stdout": stdout_clean,
        "stderr": stderr_clean,
        "generated_at": subprocess.check_output(["date", "-Iseconds"] if sys.platform != 'win32' else ["powershell", "Get-Date -Format 'yyyy-MM-ddTHH:mm:ss'"], text=True).strip(),
        "runner_used": "unified_via_capture_script"
    }

    # 4. Write to file
    quest_dir = Path(f"data/quests/{slug}")
    if not quest_dir.exists():
         print(f"❌ Quest directory not found: {quest_dir}")
         sys.exit(1)
         
    grading_dir = quest_dir / "grading"
    grading_dir.mkdir(parents=True, exist_ok=True)
    
    golden_path = grading_dir / "golden.run.json"
    
    with open(golden_path, "w", encoding="utf-8") as f:
        json.dump(golden_data, f, indent=4)
        
    print(f"✨ Wrote {golden_path}")
    print(f"   Exit Code: {golden_data['exit_code']}")
    print(f"   Stdout len: {len(golden_data['stdout'])}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
