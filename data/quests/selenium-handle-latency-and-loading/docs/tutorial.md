# Tutorial: Latency & Loading

Modern Single Page Applications (SPAs) use Javascript to update the DOM asynchronously. This means there are times when an element exists in the DOM, but it's hidden (invisible) while data is loading via a spinning icon!

### 1. What You're Testing
You will navigate to a system initialization page that artificially delays rendering its main control box by exactly 3.0 seconds to simulate a slow backend. You must wait for the UI to finish loading before clicking the confirmation button.

### 2. Key Concept: Eliminating Flaky Tests
The #1 cause of failed automation tests (called "Flaky Tests") is using `time.sleep(5)`. Do not use sleep!
By using `WebDriverWait` paired with `expected_conditions`, Selenium binds its wait to the exact millisecond the DOM reports the expected state.

**Analogy**: 
- `time.sleep()` is setting a microwave for 5 minutes and hoping the popcorn is done when the timer beeps (it might be burnt or uncooked).
- `WebDriverWait` is standing by the stove listening for the popcorn; you take it off the moment it finishes popping. 

### 3. Step-by-Step Breakdown
1. **Navigate**: Open `/latency?delay=3.0`
2. **Explicit Wait**: Use `WebDriverWait(driver, 10)` to poll the DOM.
3. **Visibility Check**: Instead of just checking if the button *exists* in the HTML source (it does!), you must wait until it is *visible* on the screen using `EC.visibility_of_element_located`.
4. **Interact**: Once the wait function successfully returns the element, click it!

### 4. Example Code Summary
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver.get(app_url)

# Wait up to 10 seconds for the button to become VISIBLE
try:
    confirm_btn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='confirm-sync']"))
    )
    confirm_btn.click()
    print("SYNC_CONFIRMED")
except Exception as e:
    print(f"FAILED: Timeout waiting for sync button to appear.")
```

### 5. How to Verify Success
In your **Automation Trace**, you should see a successful wait, followed by a successful click. Ensure `SYNC_CONFIRMED` appears in the console.

### 6. What Failure Looks Like & How to Debug
**Trace Output**:
```
❌ Message: element not interactable
```
**How to Debug**: If you use `time.sleep(1)` or `driver.find_element()` immediately, your script will find the button in the invisible DOM tree, but you cannot click what you cannot see! You will receive an `element not interactable` error. Always use `WebDriverWait` for dynamic elements.
