# Explicit Waits

Modern web applications are dynamic. Elements may not appear instantly. **Explicit Waits** allow your script to wait for a specific condition (like an element being visible) before proceeding.

## Why Use Waits?

- Prevents `NoSuchElementException`.
- Handles network latency and slow rendering.
- Makes tests more reliable (less "flaky").

## Example

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait up to 10 seconds for the title to appear
wait = WebDriverWait(driver, 10)
title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='dashboard-title']")))
```
