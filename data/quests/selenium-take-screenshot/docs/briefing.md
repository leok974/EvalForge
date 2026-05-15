# Evidence Gatherer

A screenshot is the proof of work in browser automation. Capture the dashboard state as a PNG artifact for audit and debugging.

After logging in and landing on the dashboard, save a full-page screenshot to `screenshot.png`. Print `SCREENSHOT_SAVED: screenshot.png` to confirm the file was written.

**Key pattern:**
```python
driver.save_screenshot("screenshot.png")
print("SCREENSHOT_SAVED: screenshot.png")
```

Screenshots are invaluable for diagnosing flaky tests — if an assertion fails, the screenshot shows you exactly what the browser saw at that moment.
