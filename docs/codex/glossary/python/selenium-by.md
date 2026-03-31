# Locating Elements (By)

To interact with a webpage, you must first find the elements you want to control. Selenium's `By` class provides several strategies for this.

## Common Strategies

- **`By.ID`**: Fast and reliable if IDs are unique.
- **`By.NAME`**: Good for form fields.
- **`By.CSS_SELECTOR`**: The most flexible and powerful strategy.
- **`By.XPATH`**: Useful for complex queries but can be slower and brittle.

## Best Practices in EvalForge

We recommend using **CSS Selectors** targeting `data-testid` attributes for maximum stability.

```python
from selenium.webdriver.common.by import By

username = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-username']")
```
