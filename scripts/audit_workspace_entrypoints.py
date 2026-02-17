import json
import os
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional

# --- CONFIG ---
DATA_DIR = Path("data")
QUESTS_DIR = DATA_DIR / "quests"
QUESTPACKS_DIR = DATA_DIR / "questpacks"
OUTPUT_DIR = Path("docs/audits")

OUTPUT_MD = OUTPUT_DIR / "WORKSPACE_ENTRYPOINT_AUDIT.md"
OUTPUT_JSON = OUTPUT_DIR / "WORKSPACE_ENTRYPOINT_AUDIT.json"

# --- RULES ---
def check_python_quest(quest_dir: Path, quest: Dict) -> List[str]:
    errors = []
    workspace = quest_dir / "workspace"
    if not workspace.exists():
        errors.append("Missing workspace directory")
        return errors
    
    # Standard Python entrypoint
    validation_files = ["main.py", "task.py", "app.py"]
    if not any((workspace / f).exists() for f in validation_files):
        # Check if it's a test-only quest (rare, but possible)
        # But even then, we usually expect a main.py for the runner
        errors.append(f"Missing entrypoint. Expected one of: {validation_files}")
        
    return errors

def check_node_quest(quest_dir: Path, quest: Dict) -> List[str]:
    errors = []
    workspace = quest_dir / "workspace"
    if not workspace.exists():
        errors.append("Missing workspace directory")
        return errors
    
    # Check for package.json or JS entrypoint
    has_pkg = (workspace / "package.json").exists()
    has_js = any((workspace / f).exists() for f in ["index.js", "main.js", "app.js", "solution.js"])
    
    if not (has_pkg or has_js):
        errors.append("Missing Node entrypoint (index.js/main.js) or package.json")
        
    return errors

def check_sql_quest(quest_dir: Path, quest: Dict) -> List[str]:
    errors = []
    workspace = quest_dir / "workspace"
    if not workspace.exists():
        errors.append("Missing workspace directory")
        return errors
        
    if not (workspace / "task.sql").exists() and not (workspace / "query.sql").exists():
        errors.append("Missing SQL entrypoint (task.sql or query.sql)")
        
    return errors

def check_git_quest(quest_dir: Path, quest: Dict) -> List[str]:
    errors = []
    workspace = quest_dir / "workspace"
    # Git quests might generate workspace dynamically, but if workspace exists, check for script
    if workspace.exists():
        has_script = any((workspace / f).exists() for f in ["task.sh", "solution_generator.js", "setup.sh"])
        if not has_script:
             errors.append("Missing Git entrypoint (task.sh or solution_generator.js)")
    return errors

def check_web_quest(quest_dir: Path, quest: Dict) -> List[str]:
    errors = []
    workspace = quest_dir / "workspace"
    if not workspace.exists():
        errors.append("Missing workspace directory")
        return errors
    
    # HTML or React
    has_html = (workspace / "index.html").exists()
    has_src = (workspace / "src").exists()
    # React Quests in this repo use task.mjs / task.jsx sometimes
    has_task = any((workspace / f).exists() for f in ["task.mjs", "task.jsx", "task.tsx", "App.jsx", "App.tsx"])
    
    if not (has_html or has_src or has_task):
        errors.append("Missing Web entrypoint (index.html, src/ folder, or task.mjs)")
        
    return errors

def check_docker_quest(quest_dir: Path, quest: Dict) -> List[str]:
    errors = []
    workspace = quest_dir / "workspace"
    if not workspace.exists():
        errors.append("Missing workspace directory")
        return errors
        
    has_dockerfile = (workspace / "Dockerfile").exists()
    has_compose = (workspace / "docker-compose.yml").exists() or (workspace / "docker-compose.yaml").exists()
    # Some docker quests might be shell-driven
    has_shell = (workspace / "task.sh").exists()
    
    if not (has_dockerfile or has_compose or has_shell):
        errors.append("Missing Docker entrypoint (Dockerfile, docker-compose.yml, or task.sh)")
        
    return errors

def get_checker(language: str, slug: str) -> Any:
    # Heuristics based on slug or declared language
    if "python" in slug or language == "python":
        return check_python_quest
    if "git" in slug or language in ["git", "bash", "cli"]:
        return check_git_quest
    if "node" in slug or "javascript" in slug or "typescript" in slug or language in ["javascript", "typescript", "node"]:
        return check_node_quest
    if "sql" in slug or language == "sql":
        return check_sql_quest
    if "html" in slug or "css" in slug or "react" in slug or "web" in slug or language in ["html", "css", "react"]:
        return check_web_quest
    if "docker" in slug or language == "docker":
        return check_docker_quest
    if "ml-" in slug or language == "python-ml":
        return check_ml_quest
        
    # Default to checking workspace exists if unknown
    return lambda qd, q: ["Missing workspace dir"] if not (qd / "workspace").exists() else []

# --- MAIN ---

def main():
    print("🔍 Starting Global Workspace Entrypoint Audit...")
    
    # 1. Gather Quests
    quests = {} # slug -> quest_dict
    pack_files = glob.glob(str(QUESTPACKS_DIR / "*.json")) + glob.glob(str(QUESTPACKS_DIR / "_modern" / "*.json"))
    
    print(f"📂 Found {len(pack_files)} quest packs.")
    
    for pf in pack_files:
        try:
            with open(pf, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            pack_quests = []
            if isinstance(data, list):
                pack_quests = data
            elif isinstance(data, dict) and "quests" in data:
                pack_quests = data["quests"]
                
            for q in pack_quests:
                if "slug" in q:
                    quests[q["slug"]] = q
                    # Backfill language if missing from pack metadata (for checker)
                    if "language" not in q:
                         q["language"] = "unknown"
        except Exception as e:
            print(f"❌ Error reading {pf}: {e}")

    print(f"📝 Auditing {len(quests)} unique quests...")

    failures = []
    stats = {"evaluated": 0, "passed": 0, "failed": 0, "by_language": {}}

    for slug, q in quests.items():
        stats["evaluated"] += 1
        quest_dir = QUESTS_DIR / slug
        language = q.get("language", "unknown")
        
        # Determine checker
        checker = get_checker(language, slug)
        
        # Run check
        if not quest_dir.exists():
            errs = ["Quest directory missing"]
        else:
            errs = checker(quest_dir, q)
            
        if errs:
            stats["failed"] += 1
            failures.append({
                "slug": slug,
                "language": language,
                "missing": errs,
                "path": str(quest_dir)
            })
        else:
            stats["passed"] += 1

        # Stats
        lang_key = language
        if lang_key not in stats["by_language"]:
            stats["by_language"][lang_key] = {"pass": 0, "fail": 0}
        
        if errs:
            stats["by_language"][lang_key]["fail"] += 1
        else:
            stats["by_language"][lang_key]["pass"] += 1

    # --- REPORTING ---
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump({
            "scanned_at": "now", # TODO: ISO format
            "stats": stats,
            "failures": failures
        }, f, indent=2)

    # MD
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("# Workspace Entrypoint Audit\n\n")
        f.write(f"**Total Quests**: {stats['evaluated']}\n")
        f.write(f"**Passed**: {stats['passed']} ✅\n")
        f.write(f"**Failed**: {stats['failed']} ❌\n\n")
        
        f.write("## Failures\n\n")
        if not failures:
            f.write("No failures found! 🎉\n")
        else:
            for fail in failures:
                f.write(f"### 🔴 {fail['slug']} ({fail['language']})\n")
                for err in fail['missing']:
                    f.write(f"- {err}\n")
                f.write("\n")
                
        f.write("## Stats by Language\n\n")
        f.write("| Language | Pass | Fail |\n|---|---|---|\n")
        for lang, counts in stats["by_language"].items():
            f.write(f"| {lang} | {counts['pass']} | {counts['fail']} |\n")

    print(f"✅ Audit complete. Reports written to {OUTPUT_DIR}")
    if failures:
        print(f"❌ Found {len(failures)} failures.")
        # sys.exit(1) # Optional: fail build
    else:
        print("🎉 All checks passed.")

if __name__ == "__main__":
    main()
