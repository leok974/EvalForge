import subprocess
import os

def run(cmd):
    # Shell=True for windows git command + args
    subprocess.check_call(cmd, shell=True)

if __name__ == "__main__":
    # Simulate a remote repo to clone from
    os.makedirs("remote_repo", exist_ok=True)
    subprocess.check_call("git init", cwd="remote_repo", shell=True)
    
    # Config remote
    subprocess.check_call("git config user.email 'remote@example.com'", cwd="remote_repo", shell=True)
    subprocess.check_call("git config user.name 'Remote'", cwd="remote_repo", shell=True)
    
    with open("remote_repo/README.md", "w") as f:
        f.write("# Remote Repo\n")
    
    subprocess.check_call("git add README.md", cwd="remote_repo", shell=True)
    subprocess.check_call(["git", "commit", "-m", "Initial commit"], cwd="remote_repo")
    
    # Solution: Clone it
    subprocess.check_call(["git", "clone", "./remote_repo", "my_cloned_repo"])
