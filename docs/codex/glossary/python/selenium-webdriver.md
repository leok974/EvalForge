# Selenium WebDriver

The **WebDriver** is the core bridge architecture of Selenium that allows you to control a web browser programmatically. It acts as an API translator between your Python test script and the browser's native engine (like Chrome's V8 or Gecko).

### 1. What it does
When you call `webdriver.Chrome()`, Selenium spawns a fresh, isolated browser process. Your Python script then sends HTTP commands (like "Click element X" or "Navigate to Y") to a local proxy server (the ChromeDriver), which translates them into native browser actions.

### 2. Why it exists
Without WebDriver, testing a website would require a human to manually click paths, which is slow, expensive, and unscalable for CI/CD pipelines. WebDriver democratizes access to the browser's internal state for automated verification.

### 3. EvalForge Specfic Environment: Headless vs App Preview
In EvalForge, you will see an **App Preview** panel on your right. **This is a Sandbox Iframe, NOT the browser Selenium is controlling!**
When your Python tests execute, EvalForge spawns an invisible ("headless") Chrome instance in the background. Your code commands that invisible tracker, whilst the App Preview is purely for your visual reference to inspect DOM elements.

The **Automation Trace** parses exactly what your invisible WebDriver did and prints it into your console, giving you a structured history of your automation steps.

### 4. Common Mistake: Forgetting to Quit
Always use `driver.quit()` in a `finally` block to close the browser and free up kernel resources. Otherwise, you will leak "zombie" processes!

```python
from selenium import webdriver

driver = webdriver.Chrome()
try:
    driver.get("https://example.com")
    print(driver.title)
finally:
    driver.quit() # Crucial!
```
