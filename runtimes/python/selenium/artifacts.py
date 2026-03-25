import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def capture_artifacts(driver, artifact_dir, prefix="failure"):
    """
    Captures screenshot, DOM, and metadata for a Selenium run.
    """
    if not os.path.exists(artifact_dir):
        os.makedirs(artifact_dir, exist_ok=True)
        
    timestamp = datetime.now().isoformat()
    
    screenshot_path = os.path.join(artifact_dir, f"{prefix}.png")
    dom_path = os.path.join(artifact_dir, f"{prefix}.html")
    meta_path = os.path.join(artifact_dir, f"{prefix}_meta.json")
    
    artifacts = {}
    
    try:
        # 1. Screenshot
        driver.save_screenshot(screenshot_path)
        artifacts["screenshot"] = screenshot_path
        
        # 2. DOM Snapshot
        with open(dom_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        artifacts["dom"] = dom_path
        
        # 3. Metadata
        meta = {
            "timestamp": timestamp,
            "current_url": driver.current_url,
            "title": driver.title,
            "window_size": driver.get_window_size()
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
        artifacts["metadata"] = meta_path
        
    except Exception as e:
        logger.error(f"Failed to capture artifacts: {e}")
        
    return artifacts
