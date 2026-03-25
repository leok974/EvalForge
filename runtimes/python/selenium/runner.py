import os
import json
from .harness import run_quest

class SeleniumRunner:
    """
    Backend service for managing the lifecycle of a Selenium quest run.
    """
    def __init__(self, workspace_root, artifact_root):
        self.workspace_root = workspace_root
        self.artifact_root = artifact_root

    def run(self, quest_slug, script_content, app_url):
        # 1. Prepare workspace
        quest_workspace = os.path.join(self.workspace_root, quest_slug)
        os.makedirs(quest_workspace, exist_ok=True)
        
        script_path = os.path.join(quest_workspace, "solution.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
            
        # 2. Prepare artifacts dir
        artifact_dir = os.path.join(self.artifact_root, quest_slug)
        os.makedirs(artifact_dir, exist_ok=True)
        
        # 3. Execute
        result = run_quest(script_path, app_url, artifact_dir)
        
        # 4. Save results
        results_path = os.path.join(artifact_dir, "result.json")
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
            
        return result
