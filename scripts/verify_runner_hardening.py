import requests
import json
import time

API_URL = "http://localhost:8092"
QUEST_SLUG = "python-ignition" # Ensure this exists or use a known one
# Use a known slug from python_systems.json if python-ignition is not registered? 
# "python-hello-world" or whatever exists.
# I'll try 'python-ignition' first as I created it.

def check_runner_hardening():
    print(f"Triggering run for {QUEST_SLUG}...")
    
    payload = {
        "code": "", 
        "language": "python",
        "mode": "validate",
        "workspace": [
            {
                "path": "task.py",
                "content": "print(UNIQUE_VARIABLE_FOR_VERIFICATION_12345)"
            }
        ]
    }
    
    # Headers for dev auth
    headers = {
        "x-dev-user": "dev-verifier",
        "Content-Type": "application/json"
    }
    
    try:
        # Use a real endpoint. /api/quests/{id}/run
        # I need to ensure the quest exists in DB. 
        # If python-ignition was seeded, it should be there.
        response = requests.post(f"{API_URL}/api/quests/{QUEST_SLUG}/run", json=payload, headers=headers)
        
        if response.status_code == 404:
            print(f"Quest {QUEST_SLUG} not found. Trying 'python-system-boot'...")
            # Fallback to a known quest if python-ignition missing
            QUEST_SLUG_ALT = "python-system-boot" 
            response = requests.post(f"{API_URL}/api/quests/{QUEST_SLUG_ALT}/run", json=payload, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to run quest: {response.status_code}")
            print(response.text)
            return

        data = response.json()
        stderr = data.get("stderr", "")
        stdout = data.get("stdout", "")
        
        print("\n--- Execution Result ---")
        print(f"Exit Code: {data.get('exit_code')}")
        print(f"Stdout: {stdout}")
        print(f"Stderr: {stderr}")
        print(f"Objective Results: {data.get('objective_results')}")
        
        if "NameError" in stderr or "NameError" in stdout:
            print("\n✅ SUCCESS: Caught expected NameError (Code execution works!)")
        elif "Errno 2" in stderr or "No such file" in stderr:
            print("\n❌ FAILURE: Caught Errno 2 (File missing!)")
        elif "WORKSPACE_MISSING" in stderr:
            print("\n❌ FAILURE: Preflight check failed (File missing!)")
        elif "Traceback" in stderr or "Traceback" in stdout:
             print("\n✅ SUCCESS: Caught Traceback (Code execution works!)")
        else:
            print("\n⚠️ UNKNOWN: Unexpected stderr content.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_runner_hardening()
