import os
import sys
import json
import traceback
import subprocess
from .browser import build_driver
from .artifacts import capture_artifacts

def run_quest(script_path, app_url, artifact_dir):
    """
    Executes a learner's Selenium script and captures results.
    """
    results = {
        "status": "success",
        "failure_type": None,
        "message": "",
        "artifacts": {}
    }
    
    # Inject environment variables for the learner's script
    env = os.environ.copy()
    env["EVALFORGE_APP_URL"] = app_url
    env["EVALFORGE_ARTIFACT_DIR"] = artifact_dir
    
    driver = None
    try:
        # We don't build the driver here for the learner, 
        # but we might use it for secondary verification.
        # However, the spec says the learner code build its own driver usually?
        # "Learner starter code can use OS env vars"
        
        # Actually, let's run the script as a subprocess and capture its output.
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True
        )
        stdout, stderr = process.communicate(timeout=60)
        
        results["stdout"] = stdout
        results["stderr"] = stderr
        
        if process.returncode != 0:
            results["status"] = "failed"
            results["failure_type"] = "runtime_error"
            results["message"] = stderr
            
            # Since the script failed, let's capture a screenshot of the app's initial state
            # to give the learner a hint of what the page looks like.
            try:
                driver = build_driver()
                driver.get(app_url)
                artifacts = capture_artifacts(driver, artifact_dir, prefix="failure_state")
                results["artifacts"] = artifacts
            except Exception as capture_e:
                results["message"] += f"\n[Artifact Capture Failed: {capture_e}]"
            finally:
                if driver:
                    driver.quit()
    except subprocess.TimeoutExpired:
        results["status"] = "failed"
        results["failure_type"] = "timeout"
        results["message"] = "Execution timed out after 60 seconds."
    except Exception as e:
        results["status"] = "failed"
        results["failure_type"] = "unexpected_exception"
        results["message"] = str(e)
        results["traceback"] = traceback.format_exc()
        
    return results
