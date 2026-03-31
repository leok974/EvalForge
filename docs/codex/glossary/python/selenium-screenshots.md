# Artifacts & QA Evidence Gathering

When you write scripts that execute headlessly across dozens of Continuous Integration (CI/CD) pipelines inside Linux servers and Docker containers, there's nobody sitting around watching the GUI to see if your automation was a success.

How do you prove that a test passed, failed, or that a bug exists if you cannot see the browser?

### 1. What Are Artifacts?
Artifacts are durable files (like `.png` images, `.csv` data, or `.json` logs) created by the machine running your script and placed in a safe storage location before it shuts down. Artifacts survive the destruction of the container and serve as evidence.

In professional QA, **visual evidence** is the gold standard for debugging UI regressions. Instead of guessing why a button assertion failed, a screenshot artifact provides an instant visual answer! If your code throws a `NoSuchElementException`, capturing a screenshot in the `except` block instantly tells you exactly what the DOM rendered at the moment of failure!

### 2. Why Environment Variables Matter
One of the most common rookie mistakes is hard-coding file paths directly into the test file:
```python
# Fails when run on another machine!
driver.save_screenshot("C:/Users/Bob/Desktop/screenshots/evidence.png")
```
Your script will crash the second it's handed to your coworker Alice or the remote Linux build server, because that directory does not exist!
To solve this, professional automation pipelines provide standard directory path strings via System Environment Variables.

In EvalForge, the exact folder path your script should drop files into is assigned to `os.environ.get("EVALFORGE_ARTIFACT_DIR")`. All you have to do is dynamically construct the final filename using Python's `os.path.join()`.

### 3. EvalForge Workflow

```python
import os
from selenium.webdriver.common.by import By

# 1. Ask the system for the artifact location
artifact_dir = os.environ.get("EVALFORGE_ARTIFACT_DIR", "./artifacts")
os.makedirs(artifact_dir, exist_ok=True)

# 2. Build the final filename
screenshot_path = os.path.join(artifact_dir, "ui_evidence_104.png")

# 3. Take the photo!
driver.save_screenshot(screenshot_path)

# Verify for your own sanity!
if os.path.exists(screenshot_path):
    print("Screenshot saved successfully!")
    print(f"Path: {screenshot_path}")
```
