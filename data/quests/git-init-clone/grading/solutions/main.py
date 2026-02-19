import os
import shutil
import subprocess
from pathlib import Path

def run_git(args, cwd):
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = "EvalForge Bot"
    env["GIT_AUTHOR_EMAIL"] = "evalforge@example.com"
    env["GIT_COMMITTER_NAME"] = "EvalForge Bot"
    env["GIT_COMMITTER_EMAIL"] = "evalforge@example.com"
    env["LC_ALL"] = "C.UTF-8"
    subprocess.run(["git"] + args, cwd=cwd, env=env, check=True)

def main():
    root = Path(".")
    
    # Clean up
    if (root / "my-repo").exists(): shutil.rmtree(root / "my-repo")
    if (root / "my-clone").exists(): shutil.rmtree(root / "my-clone")
    
    # Initialize repo
    my_repo = root / "my-repo"
    my_repo.mkdir()
    run_git(["init", "-q"], cwd=my_repo)
    
    # Add initial commit so we can clone
    (my_repo / "README.md").write_text("# My Repo", encoding="utf-8")
    run_git(["add", "README.md"], cwd=my_repo)
    run_git(["commit", "-q", "-m", "Initial commit"], cwd=my_repo)

    # Clone repo
    run_git(["clone", "-q", "./my-repo", "./my-clone"], cwd=root)

if __name__ == "__main__":
    main()
