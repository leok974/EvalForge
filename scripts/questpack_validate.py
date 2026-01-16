
import json
import sys
import os
import re
import glob
from pathlib import Path

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

REQUIRED_FIELDS = ["slug", "world_id", "track_id", "title", "language"]
# starter_code is optional if workspace is provided

ALLOWED_KINDS = {
    "ast", "stdout_regex", "stderr_empty", "exit_code_zero", "not_timed_out", # Existing
    "source_regex", # Phase 5
    "tests_pass" # Phase 6
}

ALLOWED_EXTENSIONS = {".py", ".ts", ".js", ".json", ".md", ".txt"}
MAX_FILE_SIZE_BYTES = 50 * 1024 # 50KB

def validate_path(path, slug):
    if ".." in path or path.startswith("/") or path.startswith("\\"):
        print(f"  ❌ Quest ({slug}): Invalid path '{path}' (traversal/absolute)")
        return False
    ext = os.path.splitext(path)[1]
    if ext not in ALLOWED_EXTENSIONS:
        print(f"  ❌ Quest ({slug}): forbidden extension '{ext}' in path '{path}'")
        return False
    return True

def validate_quest_pack(file_path):
    print(f"🔍 Validating {file_path}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ JSON Error: {e}")
        return False

    if not isinstance(data, list):
        print("❌ Root must be a list of quest definitions")
        return False

    all_ok = True
    slugs = set()

    for idx, q in enumerate(data):
        slug = q.get("slug", f"Quest#{idx}")
        
        # Check Required Fields
        missing = [f for f in REQUIRED_FIELDS if f not in q]
        if missing:
            print(f"  ❌ Quest #{idx}: Missing fields {missing}")
            all_ok = False
        
        # Uniqueness
        if slug in slugs:
             print(f"  ❌ Quest #{idx}: Duplicate slug '{slug}'")
             all_ok = False
        slugs.add(slug)
        
        # Check Language
        lang = q.get("language", "python")
        if lang not in ["python", "typescript"]:
             print(f"  ❌ Quest ({slug}): Unsupported language '{lang}'")
             all_ok = False

        # --- Phase 6: Workspace Validation ---
        workspace = q.get("workspace")
        files_map = {}
        
        if workspace:
            entrypoint = workspace.get("entrypoint")
            if not entrypoint:
                print(f"  ❌ Quest ({slug}): Workspace missing 'entrypoint'")
                all_ok = False
            
            for f in workspace.get("files", []):
                path = f.get("path")
                content = f.get("content", "")
                
                if not validate_path(path, slug):
                    all_ok = False
                
                if len(content.encode('utf-8')) > MAX_FILE_SIZE_BYTES:
                     print(f"  ❌ Quest ({slug}): File '{path}' exceeds max size")
                     all_ok = False
                     
                files_map[path] = f
            
            if entrypoint and entrypoint not in files_map:
                print(f"  ❌ Quest ({slug}): Entrypoint '{entrypoint}' not in workspace files")
                all_ok = False
        else:
            # Legacy Single File Check
            if "starter_code" not in q:
                print(f"  ❌ Quest ({slug}): Must have either 'workspace' or 'starter_code'")
                all_ok = False

        # --- Phase 6: Grading Validation ---
        grading = q.get("grading", {})
        mode = grading.get("mode", "run")
        if mode not in ["run", "tests"]:
            print(f"  ❌ Quest ({slug}): Invalid grading mode '{mode}'")
            all_ok = False
            
        if mode == "tests":
            public_tests = grading.get("public_tests", [])
            hidden_tests = grading.get("hidden_tests", [])
            if not public_tests and not hidden_tests:
                 print(f"  ⚠️ Quest ({slug}): Grading mode is 'tests' but no tests provided")
            
            for t in public_tests + hidden_tests:
                if not validate_path(t.get("path"), slug):
                    all_ok = False

        # Check Objectives
        for obj in q.get("objectives_json", []):
            kind = obj.get("kind")
            if kind not in ALLOWED_KINDS:
                print(f"  ❌ Quest ({slug}): Invalid objective kind '{kind}'")
                all_ok = False
            
            # Syntax validation for regex
            if kind in ["stdout_regex", "source_regex"]:
                pattern = obj.get("rule", {}).get("pattern")
                try:
                    re.compile(pattern)
                except Exception as e:
                    print(f"  ❌ Quest ({slug}): Invalid regex '{pattern}' - {e}")
                    all_ok = False

        # Check Smoke Metadata
        smoke = q.get("smoke", {})
        if smoke:
            if "solution_code" not in smoke and "solution_workspace_files" not in smoke:
                 print(f"  ⚠️ Quest ({slug}): Missing 'smoke.solution_code' or 'solution_workspace_files'")

    if all_ok:
        print(f"✅ {file_path} is valid.")
    return all_ok

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="File or directory of questpacks")
    args = parser.parse_args()
    
    target_files = []
    if os.path.isdir(args.path):
        target_files = glob.glob(os.path.join(args.path, "*.json"))
    else:
        target_files = [args.path]
        
    print(f"Found {len(target_files)} file(s) to validate.")
    
    success = True
    for f in target_files:
        if not validate_quest_pack(f):
            success = False
            
    if not success:
        sys.exit(1)
        
    print("All checks passed.")
