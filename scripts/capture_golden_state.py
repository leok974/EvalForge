
import json
import shutil
import subprocess
import sys
import os
import tempfile
from pathlib import Path
import argparse

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))
from scripts.utils_questpacks import get_all_quest_slugs

def run_command(cmd, cwd, env=None):
    try:
        result = subprocess.run(
            cmd, 
            cwd=str(cwd), 
            capture_output=True, 
            text=True, 
            env=env or os.environ.copy()
        )
        return result
    except Exception as e:
        print(f"Error executing {cmd}: {e}")
        return None

def capture_state(slug, root_dir):
    print(f"📸 Capturing State for {slug}...")
    
    quest_dir = root_dir / "data/quests" / slug
    if not quest_dir.exists():
        print(f"❌ Quest {slug} not found.")
        return

    workspace_dir = quest_dir / "workspace"
    grading_dir = quest_dir / "grading"
    solutions_dir = grading_dir / "solutions"
    
    if not solutions_dir.exists():
        print(f"⚠️ No solutions dir at {solutions_dir}. Skipping.")
        return

    # Use temp dir
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Copy workspace
        if workspace_dir.exists():
            for item in workspace_dir.iterdir():
                if item.is_dir():
                    shutil.copytree(item, temp_path / item.name)
                else:
                    shutil.copy2(item, temp_path)
        else:
            print(f"⚠️ No workspace dir at {workspace_dir}. Starting empty.")

        # Determine strategy: Executable vs Static
        executable = None
        runner = None
        
        if (solutions_dir / "task.sh").exists():
            executable = solutions_dir / "task.sh"
            if shutil.which("bash"): runner = "bash"
            elif shutil.which("sh"): runner = "sh"
        elif (solutions_dir / "task.py").exists():
            executable = solutions_dir / "task.py"
            runner = sys.executable
        elif (solutions_dir / "main.py").exists():
            executable = solutions_dir / "main.py"
            runner = sys.executable
        elif (solutions_dir / "index.js").exists():
             executable = solutions_dir / "index.js"
             runner = "node"
        
        if executable and runner:
            # Prepare Env
            env = os.environ.copy()
            env["GIT_AUTHOR_NAME"] = "Test User"
            env["GIT_AUTHOR_EMAIL"] = "test@example.com"
            env["GIT_COMMITTER_NAME"] = "Test User"
            env["GIT_COMMITTER_EMAIL"] = "test@example.com"
            env["HOME"] = str(temp_path) 
            
            # Wrapper for Bash
            if runner in ["bash", "sh"]:
                wrapper_content = """#!/bin/bash
git config --global user.email "test@example.com"
git config --global user.name "Test User"
git config --global init.defaultBranch main
source ./task.sh
"""
                with open(temp_path / "wrapper.sh", "w", newline="\n") as f:
                    f.write(wrapper_content)
                
                # Copy solution script
                with open(executable, "r", encoding="utf-8") as f: content = f.read()
                with open(temp_path / "task.sh", "w", newline="\n", encoding="utf-8") as f: f.write(content)
                
                cmd = [runner, "wrapper.sh"]
            else:
                shutil.copy2(executable, temp_path / executable.name)
                cmd = [runner, executable.name]

            print(f"   Executing {slug} solution ({executable.name})...")
            res = run_command(cmd, temp_path, env)
            
            if res.returncode != 0:
                print(f"❌ Solution failed (Exit {res.returncode})")
                print("Stderr:", res.stderr)
                return

            print("   ✅ Solution executed successfully.")
            
        else:
            # STATIC SOLUTION: Copy files from solutions dir to workspace
            print("   ℹ️ No executable solution script found. Applying static solution files...")
            for item in solutions_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, temp_path / item.name) # Overwrite
                elif item.is_dir():
                    if (temp_path / item.name).exists():
                        shutil.rmtree(temp_path / item.name)
                    shutil.copytree(item, temp_path / item.name)
            
            print("   ✅ Static solution applied.")
        
        # CAPTURE STATE
        state = {
            "type": "state",
            "files": [],
            "git": {}
        }
        
        # 1. Files
        for f in temp_path.rglob("*"):
             if f.is_file() and ".git" not in f.parts and "wrapper.sh" != f.name:
                 try:
                     rel = f.relative_to(temp_path).as_posix()
                     state["files"].append(rel)
                 except: pass
                 
        state["files"].sort()
        
        # 2. Git Status
        if (temp_path / ".git").exists():
             state["git"]["has_dot_git"] = True
             r = run_command(["git", "status", "--porcelain"], temp_path, os.environ.copy())
             if r and r.returncode == 0:
                 state["git"]["status_porcelain"] = r.stdout
             r = run_command(["git", "log", "--oneline", "-n", "10"], temp_path, os.environ.copy())
             if r and r.returncode == 0:
                 logs = r.stdout.strip().split("\n")
                 state["git"]["log_oneline"] = [l.strip() for l in logs if l.strip()]
        else:
            state["git"]["has_dot_git"] = False

        # Save to grading/golden.state.json
        out_file = grading_dir / "golden.state.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
            
        print(f"   Saved {out_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", help="Specific quest slug")
    parser.add_argument("--slugs", help="Comma separated list of slugs")
    parser.add_argument("--world", help="Filter by world (html, css, infra, git...)")
    args = parser.parse_args()
    
    root_dir = Path(".")
    targets = []
    
    if args.slug:
        targets = [args.slug]
    elif args.slugs:
        targets = args.slugs.split(",")
    elif args.world:
        all_slugs = get_all_quest_slugs()
        w = args.world.lower()
        for s in all_slugs:
            if w in s:
                 targets.append(s)
    else:
        # Default Git list
        targets = [
            "git-add-commit", "git-branch-merge", "git-init-clone",
            "git-rebase-linear", "git-remote-push", "git-stash",
            "git-status-diff", "git-tag-release", "git-undo-revert"
        ]
        
    print(f"Scanning {len(targets)} targets...")
    for slug in targets:
        capture_state(slug, root_dir)

if __name__ == "__main__":
    main()
