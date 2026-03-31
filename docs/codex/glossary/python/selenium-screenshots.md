# Capturing Screenshots

Screenshots are essential for debugging and providing evidence of test results.

## How to Capture

Use the `save_screenshot(filename)` method on the WebDriver instance.

```python
driver.save_screenshot("screenshot.png")
```

## EvalForge Artifacts

In EvalForge, you should save screenshots to the directory specified in the `EVALFORGE_ARTIFACT_DIR` environment variable. This allows the platform to automatically surface them in the UI.

```python
import os
path = os.path.join(os.environ["EVALFORGE_ARTIFACT_DIR"], "dashboard.png")
driver.save_screenshot(path)
```
