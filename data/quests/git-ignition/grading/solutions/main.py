import os
import shutil
import subprocess
from pathlib import Path

def run_git(args, cwd):
    # Use standard git env for reproducibility
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = "EvalForge Bot"
    env["GIT_AUTHOR_EMAIL"] = "evalforge@example.com"
    env["GIT_COMMITTER_NAME"] = "EvalForge Bot"
    env["GIT_COMMITTER_EMAIL"] = "evalforge@example.com"
    # Ensure UTF-8
    env["LC_ALL"] = "C.UTF-8"
    
    subprocess.run(["git"] + args, cwd=cwd, env=env, check=True)

def main():
    root = Path(".")
    outputs = root / "outputs"
    outputs.mkdir(exist_ok=True)
    
    tmp_repo = root / "tmp" / "repo"
    if tmp_repo.exists():
        # Handle permission errors on Windows (git readonly files)
        def on_rm_error(func, path, exc_info):
            os.chmod(path, 0o777)
            func(path)
        shutil.rmtree(tmp_repo, onerror=on_rm_error)
        
    tmp_repo.mkdir(parents=True, exist_ok=True)
    
    # Git operations
    run_git(["-c", "init.defaultBranch=main", "init", "-q"], cwd=tmp_repo)
    
    hello_txt = tmp_repo / "hello.txt"
    hello_txt.write_text("Hello, EvalForge!", encoding="utf-8")
    
    run_git(["add", "hello.txt"], cwd=tmp_repo)
    run_git(["commit", "-q", "-m", "chore: initial commit", "--no-gpg-sign"], cwd=tmp_repo)
    
    # State file generation
    state_txt = outputs / "state.txt"
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=tmp_repo, text=True).strip()
    commits = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=tmp_repo, text=True).strip()
    
    # ls behavior: only visible files
    files = sorted([f for f in os.listdir(tmp_repo) if not f.startswith(".")])
    files_str = " ".join(files) # Space separated like ls output in shell often
    
    with open(state_txt, "w", encoding="utf-8") as f:
        f.write(f"BRANCH={branch}\n")
        f.write(f"COMMITS={commits}\n")
        f.write(f"FILES={files_str}\n")

if __name__ == "__main__":
    main()
