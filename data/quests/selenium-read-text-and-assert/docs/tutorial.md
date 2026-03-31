# Tutorial: The Truth in Text

After an action like a click, the page content usually changes. Your job in QA Automation isn't just to click buttons, it's to verify that the app did what it was supposed to do!

### 1. What You're Testing
In this quest, your goal is to verify that a successful login actually loaded the correct user profile on the dashboard by reading the text of a specific DOM element.

### 2. Key Concept: Element Property Extraction and Assertions
To build reliable automation, you must assert that the page is in the expected state. 
**Analogy**: You've clicked "Bake" on the oven. Now you have to check if the pie is actually cooked by pulling it out and examining it.

Once you locate an element, Selenium `webdriver` allows you to access its properties. The `.text` property pulls the inner string from the DOM element. By using Python's `assert` keyword, you can create a test boundary!

### 3. Step-by-Step Breakdown
1. **Locate Element**: Locate the `[data-testid='dashboard-title']` heading. Ensure you use an explicit `WebDriverWait` so you don't jump the gun before the frontend finishes rendering!
2. **Read Text**: Call the `.text` property on the newly located element.
3. **Assert**: Write an `assert` expression to check the text matches your expectations.

### 4. Example Code Summary

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Wait up to 10 seconds for the element to appear
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='dashboard-title']"))
)

# 2. Extract Element and text
dashboard_title = driver.find_element(By.CSS_SELECTOR, "[data-testid='dashboard-title']")
print(f"Title text is: {dashboard_title.text}")

# 3. Prove it
assert "Welcome" in dashboard_title.text, f"Expected Welcome, got {dashboard_title.text}"
```

### 5. How to Verify Success
In your **Automation Trace**, you will see sequential green checks. The final step `✔️ Read and assert dashboard title text` will glow green because your `assert` expression evaluated to boolean `True`! 

### 6. What Failure Looks Like & How to Debug
**Trace Output**:
```
❌ Read and assert dashboard title text
↳ AssertionError: Expected Welcome, got Invalid Credentials
```
**How to debug**:
If you receive an `AssertionError`, it means your test executed without crashing, but the business logic of the app failed! Did you use the wrong Mock CMS username? Was the user suspended? Did the element load incorrect template data? Use the **App Preview** side-panel to mimic what you did and uncover the UI discrepancy!
