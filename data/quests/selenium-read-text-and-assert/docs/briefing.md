# The Truth in Text

Clicking buttons isn't enough — you need to verify the outcome. After logging in, confirm the dashboard loaded by reading a visible heading.

After a successful login, use an explicit wait to locate the dashboard heading, then read its text and print `Dashboard Title: <text>`.

**Key pattern:**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
heading = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
print(f"Dashboard Title: {heading.text}")
```

Always use `WebDriverWait` after navigation — the page may not render instantly. Avoid `time.sleep()` which creates brittle, slow tests.
