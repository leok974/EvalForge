# Tutorial: Evidence Gatherer

In a real-world testing environment, screenshots are the definitive proof that an automation script worked! This is especially important when tests are run by CI/CD bots on remote servers.

### 1. What You're Testing
In this final Selenium task, your goal is to log in, navigate to the dashboard, and invoke the Selenium WebDriver to capture a full-page artifact screenshot of the resulting UI.

### 2. Key Concept: Gathering Evidence & Artifacts
**Analogy**: Your invisible robot has done all of the lifting, but without a photograph of the finish line, your boss (or in this case, EvalForge) won't believe it succeeded.

In EvalForge, scripts often need to save outputs such as `.csv` data, JSON files, or `.png` screenshots. Because Docker environments are isolated, relying on hard-coded paths like `C:\Users\screenshots` will fail! Always use the dynamic `EVALFORGE_ARTIFACT_DIR` environment variable to ensure files are placed where the platform expects them.

### 3. Step-by-Step Breakdown
1. **Locate Artifact Path**: Pull the valid directory path from the `os.environ` array.
2. **Build Filename**: Concatenate your specific target filename (`dashboard_evidence.png`) to the directory path using `os.path.join`.
3. **Capture**: Once the page is fully rendered, execute `driver.save_screenshot(filename)`.
4. **Assert**: Confirm your code executed by asserting `os.path.exists()` on the newly written file!

### 4. Example Code Summary

```python
import os
from selenium.webdriver.support.ui import WebDriverWait

# 1. Provide exact system location
artifact_dir = os.environ.get("EVALFORGE_ARTIFACT_DIR", "./artifacts")
screenshot_path = os.path.join(artifact_dir, "dashboard_evidence.png")

# 2. Complete previous interactions
WebDriverWait(driver, 5).until(lambda d: "/dashboard" in d.current_url)

# 3. Take the photo!
driver.save_screenshot(screenshot_path)

# Verify
assert os.path.exists(screenshot_path), "Screenshot file not found"
```

### 5. How to Verify Success
In your **Automation Trace**, the final step `📷 Save dashboard screenshot` will glow green. Your console output should state `SCREENSHOT_SAVED` with the fully resolved `.png` artifact path printed. 

### 6. What Failure Looks Like & How to Debug
**Trace Output**:
```
❌ Save dashboard screenshot
↳ AssertionError: Screenshot file not found
```
**How to debug**:
An `AssertionError` here means the `save_screenshot` command was likely skipped, or the provided path was completely wrong, causing Python to fail the `os.path.exists` check. Examine your `os.path.join` variables. If the trace successfully logged the `screenshot` step but failed the check, check if your execution environment allowed file-writing permissions or if the directory needed to be dynamically `makedirs()`.
