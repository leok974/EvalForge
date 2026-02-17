#!/usr/bin/env python3
"""
Capture golden solution output for a quest.

Usage:
    python scripts/capture_golden_stdout.py --slug python-loop

Creates:
    data/quests/<slug>/grading/golden.json

This script:
1. Finds the solution file for the quest
2. Runs it using the quest runner
3. Validates exit code == 0
4. Captures stdout with SHA256 hash
5. Saves to grading/golden.json
"""

import sys
import os
import argparse
import json
import hashlib
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

def find_solution_file(quest_dir: Path) -> Path:
    """Find the solution file (try common names and locations)."""
    # Try both 'solution' and 'solutions' directories, and 'grading/solutions'
    possible_dirs = [
        quest_dir / "solution",
        quest_dir / "solutions", 
        quest_dir / "grading" / "solutions"
    ]
    
    for solution_dir in possible_dirs:
        if not solution_dir.exists():
            continue
        
        # Try common filenames
        for filename in ["main.py", "task.py", "solution.py", "index.js", "main.sql"]:
            solution_path = solution_dir / filename
            if solution_path.exists():
                return solution_path
        
        # If no common name, try first Python file in solution dir
        py_files = list(solution_dir.glob("*.py"))
        if py_files:
            return py_files[0]
    
    return None

def run_solution(solution_path: Path, language: str = "python"):
    """Run solution and capture output."""
    # Import here to avoid circular dependencies
    from arcade_app.services.code_runner import run_code
    
    with open(solution_path, encoding='utf-8') as f:
        solution_code = f.read()
    
    print(f"📝 Running solution: {solution_path}")
    print(f"   Code length: {len(solution_code)} bytes")
    
    # Run the solution (timeout in milliseconds)
    result = run_code(
        language=language,
        code=solution_code,
        timeout_ms=10000  # 10 seconds
    )
    
    # Convert to dict format expected by downstream code
    return {
        'stdout': result.stdout,
        'stderr': result.stderr,
        'exit_code': result.exit_code if result.exit_code is not None else (0 if result.ok else 1),
        'timed_out': result.timed_out
    }

def capture_golden(slug: str):
    """Run quest solution and capture output."""
    print(f"🔍 Capturing golden solution for: {slug}")
    
    # 1. Find quest directory
    quest_dir = Path(f"data/quests/{slug}")
    
    if not quest_dir.exists():
        print(f"❌ Quest directory not found: {quest_dir}")
        return False
    
    # 2. Find solution file
    solution_path = find_solution_file(quest_dir)
    
    if not solution_path:
        print(f"❌ No solution file found in: {quest_dir / 'solution'}")
        return False
    
    # 3. Determine language
    language = "python" if solution_path.suffix == ".py" else "javascript"
    
    if language != "python":
        print(f"❌ Only Python solutions supported currently (found: {language})")
        return False
    
    # 4. Run solution
    try:
        result = run_solution(solution_path, language)
    except Exception as e:
        print(f"❌ Failed to run solution: {e}")
        return False
    
    # 5. Validate golden output
    if result['exit_code'] != 0:
        print(f"❌ Solution failed with exit code {result['exit_code']}")
        print(f"   stdout: {result['stdout']}")
        print(f"   stderr: {result['stderr']}")
        return False
    
    if result['stderr']:
        print(f"⚠️  Solution has stderr:")
        print(f"   {result['stderr']}")
        response = input("   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return False
    
    # 6. Calculate stdout hash
    stdout_bytes = result['stdout'].encode('utf-8')
    stdout_hash = hashlib.sha256(stdout_bytes).hexdigest()
    
    # 7. Create golden capture
    golden = {
        "slug": slug,
        "captured_at": datetime.now().isoformat(),
        "mode": "solution",
        "language": language,
        "solution_file": str(solution_path.relative_to(quest_dir)),
        "stdout": result['stdout'],
        "stdout_sha256": stdout_hash,
        "stderr": result['stderr'],
        "exit_code": result['exit_code'],
        "timed_out": result.get('timed_out', False)
    }
    
    # 8. Save to grading/golden.json
    grading_dir = quest_dir / "grading"
    grading_dir.mkdir(exist_ok=True)
    
    golden_path = grading_dir / "golden.json"
    with open(golden_path, 'w', encoding='utf-8') as f:
        json.dump(golden, f, indent=2)
    
    print(f"\n✅ Golden capture saved: {golden_path}")
    print(f"   stdout hash: {stdout_hash[:16]}...")
    print(f"   stdout length: {len(result['stdout'])} bytes")
    print(f"   stdout preview: {repr(result['stdout'][:100])}")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Capture golden solution output for a quest"
    )
    parser.add_argument("--slug", required=True, help="Quest slug (e.g., python-loop)")
    args = parser.parse_args()
    
    success = capture_golden(args.slug)
    sys.exit(0 if success else 1)
