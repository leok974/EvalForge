
import argparse
import subprocess
import sys
import os

def run_step(cmd, desc):
    print(f"\n🚀 [STEP] {desc}")
    print(f"   Exec: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd, env=os.environ.copy())
        print(f"   ✅ {desc} passed.")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {desc} FAILED (Exit {e.returncode})")
        sys.exit(e.returncode)

def main():
    parser = argparse.ArgumentParser(description="Validate all content (CI Mirror)")
    parser.add_argument("--fast", action="store_true", help="Skip full seed (assume DB ready) or run smoke subset")
    parser.add_argument("--no-seed", action="store_true", help="Skip seeding")
    parser.add_argument("--only-slug", help="Limit smoke tests to slug")
    parser.add_argument("--clean", action="store_true", help="Interactive check before running")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug output")
    
    args = parser.parse_args()

    # 0. Setup Env
    # Ensure local execution unless CI env is set?
    # User said: "mirrors CI locally". CI runs Preflight.
    
    # 1. Runner Preflight
    run_step([sys.executable, "scripts/runner_preflight.py"], "Runner Preflight")
    
    # 2. Seed All (unless skipped)
    if not args.no_seed:
        # In fast mode, maybe we still seed? Yes, verification needs DB.
        run_step([sys.executable, "scripts/seed_all.py"], "Seeding Content")
        
    # 3. Content Audit
    run_step([sys.executable, "scripts/content_audit.py"], "Content Audit")
    
    # 4. Smoke Tests
    smoke_cmd = [sys.executable, "scripts/questpack_smoke.py", "--all"]
    if args.only_slug:
        smoke_cmd.extend(["--only", args.only_slug])
    if args.debug:
        smoke_cmd.append("--debug")
        
    # We always set Docker backend for smoke steps to be realistic
    print("\n   [INFO] Forcing EXECUTION_BACKEND=docker for smoke tests...")
    os.environ["EXECUTION_BACKEND"] = "docker"
    
    run_step(smoke_cmd, "Smoke Tests")
    
    print("\n✨ All Validation Steps Passed! Content is ready for PR.")

if __name__ == "__main__":
    main()
