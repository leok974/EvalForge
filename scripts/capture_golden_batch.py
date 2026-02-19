import sys
import os
import json
import subprocess
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from scripts.utils_questpacks import get_all_quest_slugs

def capture_golden_batch(target_world=None, plan_file="docs/audits/GOLDEN_ROLLOUT_PLAN.json"):
    print(f"📸 Capturing Golden Artifacts (World: {target_world}, Plan: {plan_file})...")
    
    # Load plan
    plan_path = Path(plan_file)
    if not plan_path.exists():
        print("Plan not found. Run plan_golden_rollout.py first.")
        return
        
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
        
    # Filter
    queue = [q for q in plan if q["world"] == target_world] if target_world else plan
    
    print(f"Queue size: {len(queue)}")
    
    for item in queue:
        slug = item["slug"]
        print(f"\nProcessing {slug}...")
        
        quest_dir = Path(f"data/quests/{slug}")
        workspace_dir = quest_dir / "workspace"
        grading_dir = quest_dir / "grading"
        grading_dir.mkdir(exist_ok=True, parents=True) # Ensure grading dir exists
        
        # Determine entrypoint
        # We can look at quest.json if we want, but standard is main.py/index.js
        entrypoint = None
        
        if (workspace_dir / "main.py").exists():
            entrypoint = (workspace_dir / "main.py").resolve()
            runner = [sys.executable, str(entrypoint)]
        elif (workspace_dir / "task.sh").exists():
            entrypoint = (workspace_dir / "task.sh").resolve()
            # Use bash if available, else sh
            import shutil
            shell = shutil.which("bash") or shutil.which("sh")
            if not shell: shell = "bash" # Hope for best
            runner = [shell, str(entrypoint)]
        elif (workspace_dir / "index.js").exists():
            entrypoint = (workspace_dir / "index.js").resolve()
            runner = ["node", str(entrypoint)]
        elif (workspace_dir / "package.json").exists():
             # Fallback to npm test
             entrypoint = (workspace_dir / "package.json").resolve()
             # shell=True needed for npm on windows sometimes, but subprocess list is safer
             # On windows npm is npm.cmd
             npm = "npm.cmd" if os.name == "nt" else "npm"
             runner = [npm, "test"]
        elif (workspace_dir / "task.py").exists():
             entrypoint = (workspace_dir / "task.py").resolve()
             runner = [sys.executable, str(entrypoint)]
             
        # Resolve CWD too
        workspace_dir = workspace_dir.resolve()
        
        if not entrypoint:
            print(f"⚠️ No entrypoint found for {slug}. Creating placeholder spec.")
            create_placeholder_spec(slug, grading_dir, "Missing entrypoint")
            continue
            
        # Run
        try:
            # We assume these are safe to run (seeded/legacy code)
            result = subprocess.run(
                runner,
                cwd=workspace_dir,
                capture_output=True,
                text=True,
                timeout=5 # Short timeout
            )
            
            # Create golden.run.json
            golden_run = {
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "generated_at": "2026-02-18", # static date for now or dynamic
            }
            
            # Write
            with open(grading_dir / "golden.run.json", "w", encoding="utf-8") as f:
                json.dump(golden_run, f, indent=4)
                
            print(f"✅ Captured golden.run.json for {slug}")
            
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout running {slug}. Creating placeholder.")
            create_placeholder_spec(slug, grading_dir, "Timeout")
        except Exception as e:
            print(f"❌ Error running {slug}: {e}. Creating placeholder.")
            create_placeholder_spec(slug, grading_dir, str(e))

def create_placeholder_spec(slug, grading_dir, reason):
    spec = {
        "blocked_reason": reason,
        "requires_fix": True
    }
    with open(grading_dir / "golden.spec.json", "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=4)
    print(f"⚠️ Created golden.spec.json for {slug}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--world", help="Filter by world (python, js, ml, git...)")
    parser.add_argument("--plan", default="docs/audits/GOLDEN_ROLLOUT_PLAN.json", help="Path to plan JSON")
    args = parser.parse_args()
    
    capture_golden_batch(args.world, args.plan)
