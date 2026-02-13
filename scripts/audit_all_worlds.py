import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_QUESTPACKS = REPO_ROOT / "data" / "questpacks"
DATA_QUESTS = REPO_ROOT / "data" / "quests"

def run_pack(pack_path, mode):
    cmd = ["node", "scripts/run_world_public_tests.mjs", "--questpack", str(pack_path), "--mode", mode]
    try:
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, encoding="utf-8", errors="replace", timeout=120) 
        stdout = res.stdout
        
        # Extract JSON
        json_line = None
        for line in stdout.splitlines():
            if line.startswith("EF_RUNNER_RESULT_JSON="):
                json_line = line.replace("EF_RUNNER_RESULT_JSON=", "")
                break
        
        result_data = None
        if json_line:
            try:
                result_data = json.loads(json_line)
            except:
                pass
        
        # Formatting result
        ret = {
            "ran": True,
            "exit_code": res.returncode,
            "pass": 0,
            "fail": 0,
            "errors": [],
            "raw_summary": "No summary found"
        }

        # Look for summary line
        for line in stdout.splitlines():
            if "EF_RUN_WORLD_SUMMARY" in line:
                ret["raw_summary"] = line.strip()

        if result_data:
            ret["pass"] = result_data.get("passed", 0)
            ret["fail"] = result_data.get("failed", 0)
            ret["errors"] = result_data.get("errors", [])
        else:
            # Fallback
            if res.returncode == 0:
                ret["pass"] = -1 # Unknown but passed
            else:
                ret["fail"] = -1 # Unknown but failed
                ret["errors"].append("Legacy runner failure or timeout")

        return ret

    except Exception as e:
        return {
            "ran": False,
            "error": str(e)
        }

def audit_pack(pack_path):
    print(f"Auditing {pack_path.name}...")
    try:
        content = json.loads(pack_path.read_text(encoding="utf-8"))
    except:
        return None

    world_id = "unknown"
    if isinstance(content, dict):
        world_id = content.get("world_id", "unknown")
    
    # Extract slugs
    slugs = []
    format_type = "modern"
    if isinstance(content, list):
        format_type = "legacy"
        world_id = "legacy-derived"
        format_type = "legacy"
        for item in content:
            if isinstance(item, dict):
                 path_str = item.get("quest_path") or item.get("questPath")
                 if path_str: slugs.append(path_str.split("/")[-1])
    elif isinstance(content, dict):
        if "quests" in content:
             for q in content["quests"]:
                 if isinstance(q, str): slugs.append(q) # rare
                 elif isinstance(q, dict):
                     if "slug" in q: slugs.append(q["slug"])
                     elif "quest_path" in q: slugs.append(q["quest_path"].split("/")[-1])
        elif "entries" in content: # generic map
             # ...
             pass
    
    # Check Structure
    structure = {
        "missing_dir": [],
        "missing_public": [],
        "missing_solution": []
    }
    
    for s in slugs:
        q_dir = DATA_QUESTS / s
        if not q_dir.exists():
            structure["missing_dir"].append(s)
            continue
        
        if not (q_dir / "grading" / "public").exists() or not list((q_dir / "grading" / "public").iterdir()):
             structure["missing_public"].append(s)
        
        if not (q_dir / "grading" / "solutions").exists() or not list((q_dir / "grading" / "solutions").iterdir()):
             structure["missing_solution"].append(s)

    # Run Verification
    # Only if structure is mostly sane? Or run anyway.
    # Run Student
    student_res = run_pack(pack_path, "student")
    solution_res = run_pack(pack_path, "solution")

    # Determine Status
    status = "NEEDS_UPGRADE"
    if format_type == "modern":
        if not structure["missing_dir"] and not structure["missing_public"] and not structure["missing_solution"]:
            if solution_res["pass"] > 0 and solution_res["fail"] == 0:
                status = "TRAINING_GRADE"
            else:
                 status = "NEEDS_VERIFY" # Structure ok but tests failed
        else:
             status = "NEEDS_UPGRADE" # Missing files
    else:
        status = "NEEDS_UPGRADE" # Legacy format

    return {
        "world_key": world_id,
        "questpack": str(pack_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "format": format_type,
        "slugs": slugs,
        "structure": structure,
        "verification": {
            "student": student_res,
            "solution": solution_res
        },
        "status": status
    }

def main():
    packs = list(DATA_QUESTPACKS.glob("*.json"))
    report = {
        "generated_at": datetime.now().isoformat(),
        "worlds": []
    }
    
    for p in packs:
        # Skip some big ones? No, user asked for Audit.
        # But skip maps? `campaign_map.json` is not a questpack.
        if "map" in p.name or "profile" in p.name or "context" in p.name: continue
        
        res = audit_pack(p)
        if res:
            report["worlds"].append(res)
            
    # Write JSON
    (REPO_ROOT / "docs" / "audits").mkdir(parents=True, exist_ok=True)
    json_path = REPO_ROOT / "docs" / "audits" / "WORLDS_UPGRADE_STATUS.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    
    # Write MD
    md_path = REPO_ROOT / "docs" / "audits" / "WORLDS_UPGRADE_STATUS.md"
    
    lines = ["# World Upgrade Status audit\n", "| World | Pack | Format | Student | Solution | Status | Missing Data |", "|---|---|---|---|---|---|---|"]
    
    for w in report["worlds"]:
        p_name = Path(w["questpack"]).name
        fmt = w["format"]
        stud = w["verification"]["student"]
        sol = w["verification"]["solution"]
        
        s_res = f"{stud.get('pass')}/{stud.get('fail')}" if stud["ran"] else "ERR"
        sol_res = f"{sol.get('pass')}/{sol.get('fail')}" if sol["ran"] else "ERR"
        
        missing = len(w["structure"]["missing_public"]) + len(w["structure"]["missing_solution"])
        
        lines.append(f"| {w['world_key']} | {p_name} | {fmt} | {s_res} | {sol_res} | {w['status']} | {missing} missing |")
        
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Audit Complete. Report: {md_path}")

if __name__ == "__main__":
    main()
