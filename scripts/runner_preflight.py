
import sys
import os
import subprocess

def check_docker_socket():
    sock = "/var/run/docker.sock"
    if os.path.exists(sock):
        print(f"✅ Docker socket found at {sock}")
        return True
    else:
        print(f"❌ Docker socket MISSING at {sock}")
        return False

def check_docker_cli():
    try:
        ver = subprocess.check_output(["docker", "--version"], stderr=subprocess.STDOUT)
        print(f"✅ Docker CLI found: {ver.decode().strip()}")
        return True
    except FileNotFoundError:
        print("❌ Docker CLI binary NOT FOUND in PATH")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker CLI error: {e.output.decode()}")
        return False

def check_docker_connectivity():
    try:
        out = subprocess.check_output(["docker", "ps"], stderr=subprocess.STDOUT)
        print("✅ Docker Daemon connectivity confirmed (docker ps works)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker Daemon connectivity FAILED: {e.output.decode()}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error checking connectivity: {e}")
        return False

def main():
    print("🔍 Runner Preflight Check...")
    
    steps = [
        check_docker_socket,
        check_docker_cli,
        check_docker_connectivity
    ]
    
    success = True
    for step in steps:
        if not step():
            success = False
            
    if not success:
        print("\n💥 Preflight CHECK FAILED. Runners will not work.")
        sys.exit(1)
    
    print("\n✨ Preflight CHECK PASSED. Ready to run code.")
    sys.exit(0)

if __name__ == "__main__":
    main()
