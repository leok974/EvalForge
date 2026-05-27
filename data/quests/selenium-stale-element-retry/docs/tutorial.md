# Tutorial: Stale Element Retry

Imagine you find an element in the DOM and save it to a variable `btn`. You click it, and the website's javascript framework (React, Vue) updates the page by destroying the old button and rendering a *new* button with exactly the same IDs to replace it. 

If you try to click `btn` again, Python crashes!

### 1. What You're Testing
You will navigate to a Mock Hardware Sensor Node. Every time you query the sensor, the Mock CMS destroys the HTML container and rebuilds it with a new temperature value. You must handle the resulting `StaleElementReferenceException` gracefully.

### 2. Key Concept: Stale References
A **Stale Element Reference Exception** occurs when you attempt to interact with an element that no longer exists in the browser's current DOM, even if the graphical UI looks identical.
**Analogy**: You grab a friend's phone number and save it in your contacts (`find_element()`). Your friend deletes their old number and gets a new one. If you try to call your saved contact, you get an error (`StaleElementReferenceException`). You must look up their new number (`find_element()` again!).

### 3. Step-by-Step Breakdown
1. **Initial Search**: Locate `data-testid="sensor-reading"` and read its `.text`.
2. **Trigger Reset**: Click the `data-testid="refresh-button"` which takes ~500ms to rebuild the DOM.
3. **Intentional Crash**: Use a `try/except StaleElementReferenceException` block. Inside the `try`, attempt to read the *old* variable's `.text` again. It will fail!
4. **Re-Query**: In the exception block, or after it, call `driver.find_element` again to grab the fresh DOM node.
5. **Pass**: Prove the new text is different and print the success command.

### 4. Example Code Summary
```python
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time

driver.get(app_url)

# 1. Grab Element
sensor = driver.find_element(By.CSS_SELECTOR, "[data-testid='sensor-reading']")

# 2. Trigger Action (Destroys DOM behind the scenes!)
driver.find_element(By.CSS_SELECTOR, "[data-testid='refresh-button']").click()
time.sleep(1) # Let the network finish

# 3. Defensive catch!
try:
    print(sensor.text)
    assert False, "Should have thrown Stale Element Exception!"
except StaleElementReferenceException:
    print("Caught Stale Element!")

# 4. Re-Query! This works!
sensor_fresh = driver.find_element(By.CSS_SELECTOR, "[data-testid='sensor-reading']")
print(f"New Value: {sensor_fresh.text}")
print("SENSOR_UPDATED")
```

### 5. How to Verify Success
Your code will intentionally catch a Stale Element Exception, which represents advanced framework maturity!

### 6. What Failure Looks Like & How to Debug
**Trace Output**:
```
❌ Message: stale element reference: stale element not found
```
**How to Debug**: If you fail to catch this exception, your script crashes uncontrollably. Whenever you see a "Stale Element" error in the real world, the solution is always the same: **Find the element again immediately before you use it.**
