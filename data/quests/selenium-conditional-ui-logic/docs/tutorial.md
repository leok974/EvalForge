# Tutorial: Conditional UI Logic

Web applications are unpredictable. Advertisements, GDPR cookie banners, and "Announcement" modals can appear randomly and hijack the screen, blocking your automation script from clicking the button it actually wants!

### 1. What You're Testing
You will navigate to `/modals?show_modal=true`. The system will spawn a blocking modal dialogue after a short delay. You must write defensive code that checks if the modal exists, closes it if it does, and then continues the script.

### 2. Key Concept: Defensive Try/Except Blocks
To handle unpredictable UI, developers use "Branching Logic". 
**Analogy**: You are walking down a hallway. If a door is open, you walk through it. If the door is closed, you don't just smash your face into it and crash; you stop, turn the handle, open it, and *then* walk through.

In Python, we achieve this by attempting an action inside a `try` block. If the element isn't there, Selenium throws a `TimeoutException`, which we "catch" and gracefully ignore!

### 3. Step-by-Step Breakdown
1. **Navigate**: Open the provided `app_url`.
2. **Try to Wait**: Create a `try/except TimeoutException` block. Inside the `try`, use a short `WebDriverWait` (e.g. 2s) to look for the modal's cancel button.
3. **Handle It**: If the wait succeeds, click the cancel button.
4. **Pass Gracefully**: If the wait times out, the `except TimeoutException:` block fires. Simply use the `pass` keyword to do nothing!
5. **Resume Flow**: After the try/except block, use `find_element` to click the main `[data-testid='trigger-override']` button on the parent page to prove the modal is gone.

### 4. Example Code Summary
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException # Critical!

# 1. Look for the modal defensively
try:
    cancel_btn = WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='modal-cancel']"))
    )
    # The modal appeared! Click it.
    cancel_btn.click()
    print("Modal caught and closed.")
    
except TimeoutException:
    # 2. Oh, it didn't appear. No problem! Move on.
    print("No modal detected, continuing flow.")

# 3. Resume main test!
driver.find_element(By.CSS_SELECTOR, "[data-testid='trigger-override']").click()
print("DEFENSE_ACTIVE")
```

### 5. How to Verify Success
In your **Automation Trace**, you will see your script successfully click the final button. If you alter the URL to `?show_modal=false` in your script, it should STILL PASS!

### 6. What Failure Looks Like & How to Debug
**Trace Output**:
```
❌ Message: element click intercepted: Element <button> is not clickable at point (50, 50). Other element would receive the click: <div class="overlay"></div>
```
**How to Debug**: If you fail to close the modal before trying to click the main page, Selenium will simulate a real browser physics check and block your click! It literally tells you "Other element would receive the click". Use your `try/except` defensively to clear the overlay out of the way.
