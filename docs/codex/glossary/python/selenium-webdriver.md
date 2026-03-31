# Selenium WebDriver

The **WebDriver** is the core component of Selenium that allows you to control a web browser programmatically. It acts as a bridge between your test script and the browser.

## Key Concepts

- **Driver Initialization**: You must start a driver instance (e.g., `webdriver.Chrome()`) to begin.
- **Navigation**: Use `driver.get(url)` to visit a page.
- **Cleanup**: Always use `driver.quit()` to close the browser and free up resources.

## Example

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://example.com")
print(driver.title)
driver.quit()
```
