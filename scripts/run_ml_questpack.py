import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def run_ml_questpack(questpack_path, mode="student", only_slug=None):
    """
    Runs tests for an ML questpack using pytest.
    """
    try:
        with open(questpack_path, "r", encoding="utf-8") as f:
            pack_data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load questpack: {e}")
        return

    quests = pack_data.get("quests", [])
    if not quests:
        logger.error("No quests found in questpack.")
        return

    root_dir = Path.cwd()
    results = []
    passed_count = 0
    total_count = 0

    logger.info(f"=== Running {len(quests)} ML quests from {questpack_path} in {mode} mode ===")

    for quest in quests:
        slug = quest["slug"]
        if only_slug and slug != only_slug:
            continue

        total_count += 1
        quest_dir = root_dir / "data" / "quests" / slug
        grading_dir = quest_dir / "grading"
        public_tests = grading_dir / "public"
        
        # Check if tests exist
        if not public_tests.exists():
             logger.error(f"Missing tests for {slug}: {public_tests}")
             results.append({"slug": slug, "status": "failed", "error": "Missing tests"})
             continue

        # Solution Mode Swap
        backups = []
        if mode == "solution":
            sol_dir = grading_dir / "solutions"
            ws_dir = quest_dir / "workspace"
            if sol_dir.exists() and ws_dir.exists():
                for sol_file in sol_dir.glob("*"):
                    if sol_file.is_file():
                        target = ws_dir / sol_file.name
                        if target.exists():
                            backup = target.with_suffix(target.suffix + ".bak")
                            shutil.copy2(target, backup)
                            backups.append((target, backup))
                        else:
                            backups.append((target, None)) # Track new file
                        shutil.copy2(sol_file, target)
            else:
                logger.warning(f"No solution found for {slug} at {sol_dir}")

        # Run Tests (Pytest)
        # We run pytest on the directory. We add root to PYTHONPATH so imports work.
        env = os.environ.copy()
        # Add quest_dir to PYTHONPATH so 'import workspace' works
        env["PYTHONPATH"] = str(quest_dir) + os.pathsep + str(root_dir) + os.pathsep + env.get("PYTHONPATH", "")
        
        # Determine test files
        test_files = list(public_tests.glob("*_test.py")) + list(public_tests.glob("test_*.py"))
        if not test_files:
             logger.error(f"No test files found in {public_tests}")
             results.append({"slug": slug, "status": "failed", "error": "No test files"})
             if mode == "solution": # Cleanup
                 for target, backup in reversed(backups):
                     if backup and backup.exists():
                         shutil.move(backup, target)
                     elif target.exists():
                         target.unlink()
             continue

        cmd = [sys.executable, "-m", "pytest", "-q", "--tb=short"] + [str(f) for f in test_files]
        
        try:
            result = subprocess.run(cmd, env=env, cwd=root_dir, capture_output=True, text=True)
            success = result.returncode == 0
            
            if success:
                logger.info(f"✅ PASS: {slug}")
                passed_count += 1
                results.append({"slug": slug, "status": "passed"})
            else:
                logger.error(f"❌ FAIL: {slug}")
                logger.error(result.stdout)
                logger.error(result.stderr)
                results.append({"slug": slug, "status": "failed", "output": result.stdout})

        except Exception as e:
            logger.error(f"Error running runner for {slug}: {e}")
            results.append({"slug": slug, "status": "failed", "error": str(e)})

        # Cleanup Swaps
        if mode == "solution":
            for target, backup in reversed(backups):
                try:
                    if backup and backup.exists():
                        shutil.move(backup, target)
                    elif target.exists(): # Was a new file
                        target.unlink()
                except Exception as e:
                     logger.warning(f"Failed to restore {target}: {e}")

    # Results JSON
    summary = {
        "total": total_count,
        "passed": passed_count,
        "failed": total_count - passed_count,
        "errors": [],
        "slugs": results
    }
    print(f"EF_RUNNER_RESULT_JSON={json.dumps(summary)}")
    
    if passed_count < total_count:
        logger.info(f"\n❌ ML questpack FAILED ({passed_count}/{total_count} passed)")
        sys.exit(1)
    else:
        logger.info(f"\n✅ ML questpack OK ({passed_count}/{total_count} passed)")
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--questpack", required=True)
    parser.add_argument("--mode", default="student", choices=["student", "solution"])
    parser.add_argument("--only-slug")
    args = parser.parse_args()
    
    run_ml_questpack(args.questpack, args.mode, args.only_slug)
