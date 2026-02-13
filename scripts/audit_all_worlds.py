import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Configuration
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_QUESTPACKS = REPO_ROOT / "data" / "questpacks"
DATA_QUESTS = REPO_ROOT / "data" / "quests"
OUTPUT_JSON = REPO_ROOT / "docs" / "audits" / "WORLDS_UPGRADE_STATUS.json"
OUTPUT_MD = REPO_ROOT / "docs" / "audits" / "WORLDS_UPGRADE_STATUS.md"

# Ensure output dir exists
OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

def run_tests(pack_path, mode):
    """Run tests and parse output for pass/fail counts."""
    cmd = [
        "node", 
        str(REPO_ROOT / "scripts" / "run_world_public_tests.mjs"),
        "--questpack", str(pack_path),
        "--mode", mode
    ]
    try:
        # We run with timeout to avoid hangs
        result = subprocess.run(
            cmd, 
            cwd=str(REPO_ROOT), 
            capture_output=True, 
            text=True, 
            timeout=120, # 2 minutes per pack max
            encoding='utf-8',
            shell=True if os.name == 'nt' else False
        )
        output = result.stdout + result.stderr
        
        # Parse output for summary line or cues
        # Usually "EF_RUN_WORLD_SUMMARY: X public tests passed." or similar.
        # Or individual [PASS] [FAIL].
        
        pass_count = output.count("[PASS]")
        fail_count = output.count("[FAIL]")
        
        # Alternative parsing if explicit summary exists
        # But [PASS]/[FAIL] is printed by python runners. 
        # Node runner prints "✔" or "✖".
        if pass_count == 0 and fail_count == 0:
             # Try regex for node tap output?
             pass_count = output.count("✔")
             fail_count = output.count("✖") + output.count("failed") # approximate
        
        return {
            "ran": True,
            "pass": pass_count,
            "fail": fail_count,
            "errors": [l for l in output.splitlines() if "ERR_" in l or "Error:" in l][:5]
        }
    except subprocess.TimeoutExpired:
        return {"ran": False, "pass": 0, "fail": 0, "errors": ["Timeout"]}
    except Exception as e:
        return {"ran": False, "pass": 0, "fail": 0, "errors": [str(e)]}

def audit_pack(pack_file):
    print(f"Auditing {pack_file.name}...")
    try:
        data = json.loads(pack_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            "world_key": pack_file.stem,
            "questpack": str(pack_file.relative_to(REPO_ROOT)), # Use relative path for JSON output
            "format": "broken",
            "slugs": [],
            "status": "NEEDS_UPGRADE"
        }

    # Determine format and slugs
    slugs = []
    fmt = "legacy"
    if "quests" in data and isinstance(data["quests"], list):
        # Modern? List of objects with slug?
        if len(data["quests"]) > 0 and isinstance(data["quests"][0], dict) and "slug" in data["quests"][0]:
            fmt = "modern"
            slugs = [q["slug"] for q in data["quests"]]
        elif len(data["quests"]) > 0 and isinstance(data["quests"][0], str):
            # Legacy list of strings?
            slugs = data["quests"]
    
    # Check structure
    missing_data = []
    missing_public = []
    missing_solutions = []
    missing_fixtures = []

    for s in slugs:
        q_dir = DATA_QUESTS / s
        if not q_dir.exists():
            missing_data.append(s)
            continue
            
        if not (q_dir / "workspace").exists():
            missing_data.append(f"{s}/workspace")
            
        # Public tests
        public_tests = list((q_dir / "grading" / "public").glob("*")) if (q_dir / "grading" / "public").exists() else []
        if not public_tests:
             missing_public.append(s)
             
        # Solution
        solutions = list((q_dir / "grading" / "solutions").glob("*")) if (q_dir / "grading" / "solutions").exists() else []
        if not solutions:
             missing_solutions.append(s)
             
        # Fixtures (loose check)
        # If sql/python, verify common fixtures? 
        # For now just existence of fixtures dir if tests reference it? Hard to know if referenced.
        # We skip explicit fixture check unless we know what to look for.
        
    # Verification
    # Only verify if we have slugs
    student_res = {"ran": False}
    solution_res = {"ran": False}
    
    status = "NEEDS_UPGRADE"
    
    if slugs:
        print(f"  Verifying Student Mode...")
        student_res = run_tests(pack_file, "student")
        print(f"  Verifying Solution Mode...")
        solution_res = run_tests(pack_file, "solution")
        
        # Status determination
        # Training grade = modern format + structural integrity + 100% pass solution + ran
        is_modern = fmt == "modern"
        struct_ok = not (missing_data or missing_public or missing_solutions)
        sol_pass = solution_res.get("pass", 0) >= len(slugs) and solution_res.get("fail", 0) == 0
        
        if is_modern and struct_ok and sol_pass:
            status = "TRAINING_GRADE"
        elif is_modern and struct_ok:
            status = "NEEDS_VERIFY" # Structure ok but tests failed?
        else:
            status = "NEEDS_UPGRADE"
            
    return {
        "world_key": pack_file.stem.replace("_core", ""),
        "questpack": str(pack_file.relative_to(REPO_ROOT)),
        "format": fmt,
        "slugs": slugs,
        "structure": {
            "quests_missing_data_dir": missing_data,
            "quests_missing_public_tests": missing_public,
            "quests_missing_solutions": missing_solutions
        },
        "verification": {
            "student": student_res,
            "solution": solution_res
        },
        "status": status
    }

def main():
    report = {
        "generated_at": datetime.now().isoformat(),
        "repo": {
            "os": os.name
        },
        "worlds": []
    }
    
    packs = list(DATA_QUESTPACKS.glob("*.json"))
    # Prioritize core packs mostly
    # But user said "Prefer checking 100%"
    
    for p in packs:
        world_res = audit_pack(p)
        report["worlds"].append(world_res)
        
    # Write JSON
    OUTPUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON}")
    
    # Write MD
    md_lines = [
        "# Worlds Upgrade Status",
        "",
        "| World | Pack | Format | Student (P/F) | Solution (P/F) | Status | Top Blocker |",
        "|---|---|---|---|---|---|---|"
    ]
    
    # Sort by status (Needs Upgrade first) then name
    sorted_worlds = sorted(report["worlds"], key=lambda x: (x["status"] == "TRAINING_GRADE", x["world_key"]))
    
    for w in sorted_worlds:
        s_res = w["verification"]["student"]
        sol_res = w["verification"]["solution"]
        
        stud_str = f"{s_res.get('pass',0)}/{s_res.get('fail',0)}" if s_res.get("ran") else "-"
        sol_str = f"{sol_res.get('pass',0)}/{sol_res.get('fail',0)}" if sol_res.get("ran") else "-"
        
        blocker = "-"
        if w["format"] == "legacy": blocker = "Legacy Format"
        elif w["structure"]["quests_missing_public_tests"]: blocker = "Missing Tests"
        elif w["structure"]["quests_missing_solutions"]: blocker = "Missing Solutions"
        elif sol_res.get("fail", 0) > 0: blocker = "Tests Failing"
        elif w["status"] == "TRAINING_GRADE": blocker = "None"
        
        md_lines.append(f"| {w['world_key']} | {Path(w['questpack']).name} | {w['format']} | {stud_str} | {sol_str} | {w['status']} | {blocker} |")
        
    OUTPUT_MD.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_MD}")

if __name__ == "__main__":
    main()
