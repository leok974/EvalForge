import subprocess
import os

def run(cmd):
    # Shell=True for windows git command + args
    subprocess.check_call(cmd, shell=True)

if __name__ == "__main__":
    # Ensure clean state (safe since we run in temp dir)
    # 1. Git Init
    run("git init")
    
    # 2. Config Identity (Ephemeral)
    run("git config user.email 'student@evalforge.app'")
    run("git config user.name 'Student'")
    
    # 3. Create content
    with open("README.md", "w") as f:
        f.write("# Git Ignition\n")
        
    # 4. Add & Commit
    run("git add README.md")
    run("git commit -m \"Initial commit\"")
