import os
import sys
import json
import time
import traceback
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumHarness:
    def __init__(self, artifacts_dir):
        self.artifacts_dir = Path(artifacts_dir)
        self.screenshots_dir = self.artifacts_dir / "screenshots"
        self.dom_dir = self.artifacts_dir / "dom_snapshots"
        
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.dom_dir.mkdir(parents=True, exist_ok=True)
        
        self.artifacts = {
            "screenshots": [],
            "dom_snapshots": [],
            "logs": []
        }
        
        self.driver = self._init_driver()

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280,720")
        
        # In Docker, we assume chromedriver is in PATH or use webdriver_manager
        try:
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            print(f"ERROR[selenium-harness]: Failed to init driver: {e}", file=sys.stderr)
            raise

    def take_screenshot(self, name):
        timestamp = time.strftime("%H%M%S")
        filename = f"screenshot_{timestamp}_{name}.png"
        path = self.screenshots_dir / filename
        self.driver.save_screenshot(str(path))
        
        self.artifacts["screenshots"].append({
            "id": name,
            "path": f"screenshots/{filename}",
            "timestamp": time.time()
        })

    def take_dom_snapshot(self, name):
        timestamp = time.strftime("%H%M%S")
        filename = f"dom_{timestamp}_{name}.html"
        path = self.dom_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
            
        self.artifacts["dom_snapshots"].append({
            "id": name,
            "path": f"dom_snapshots/{filename}",
            "timestamp": time.time()
        })

    def close(self):
        if self.driver:
            self.driver.quit()
        self.save_manifest()

    def save_manifest(self):
        with open(self.artifacts_dir / "selenium_artifacts.json", "w", encoding="utf-8") as f:
            json.dump(self.artifacts, f, indent=2)
        # Also emit to stdout for fast capture
        print(f"\n<<EVALFORGE_ARTIFACTS_START>>{json.dumps({'selenium': self.artifacts})}<<EVALFORGE_ARTIFACTS_END>>\n")

def main():
    start_dir = Path('/workspace')
    artifacts_dir = os.getenv("EVALFORGE_ARTIFACTS_DIR", str(start_dir / ".evalforge"))
    entrypoint = os.getenv("EVALFORGE_ENTRYPOINT", "task.py")
    
    harness = SeleniumHarness(artifacts_dir)
    
    # Inject harness into globals for student code
    # We can provide a 'browser' object
    
    try:
        # Load student code
        with open(start_dir / entrypoint, "r", encoding="utf-8") as f:
            code = f.read()
            
        # Execute in a sandbox-ish way (globals)
        exec_globals = {
            "browser": harness.driver,
            "take_screenshot": harness.take_screenshot,
            "take_dom_snapshot": harness.take_dom_snapshot,
            "__name__": "__main__",
        }
        
        exec(code, exec_globals)
        
    except Exception as e:
        print(f"Execution Failed: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        # Try to capture failure state
        try:
            app_url = os.getenv("EVALFORGE_APP_URL", "http://host.docker.internal:8765")
            harness.driver.get(app_url)
            harness.take_screenshot("failure_state")
            harness.take_dom_snapshot("failure_state")
        except Exception as capture_e:
            print(f"Failed to capture artifact: {capture_e}", file=sys.stderr)
        sys.exit(1)
    finally:
        harness.close()

if __name__ == "__main__":
    main()
