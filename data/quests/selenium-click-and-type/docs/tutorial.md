# Tutorial: Data Entry Specialist

Once you've located the input fields in the DOM, the next step is interaction. 

### 1. What You're Testing
In this quest, you will learn how to send keystrokes to an element and click a button. You will automate the full login flow for the Mock CMS, proving that a user can successfully enter credentials and navigate to the dashboard.

### 2. Key Concept: Interaction and the PRG Pattern
These are the fundamental building blocks of almost all web automation: `send_keys` and `.click()`.
**Analogy**: You've told your robot where the keyboard and mouse are (Locating elements); now you are telling it what buttons to physically press.

One critical detail the robot must understand is the **Post-Redirect-Get (PRG)** pattern. When you click "Login", the Mock CMS receives the POST form and then *redirects* the browser to the `/dashboard` route. This redirect takes a fraction of a second. If your automation doesn't realize it needs to wait for the redirect, it will fail checking for the dashboard.

### 3. Step-by-Step Breakdown
1. **Send Keys**: To type into a text field, locate the element and call `send_keys(text)`. Good practice is to use `.clear()` first to empty the field!
2. **Click Elements**: To click a button or link, locate the element and call `click()`.
3. **Wait**: Use an explicit `WebDriverWait` to block your script until the browser finishes loading the new URL.

### 4. Example Code Summary

```python
username_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-username']")
username_field.clear() 
username_field.send_keys("admin")

login_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']")
login_button.click()

# Explicit Wait! Wait up to 5s for the redirect...
from selenium.webdriver.support.ui import WebDriverWait
WebDriverWait(driver, 5).until(lambda d: "/dashboard" in d.current_url)

print(f"LOGIN_SUCCESS: {driver.current_url}")
```

### 5. How to Verify Success
In your **Automation Trace**, you will see sequential green checks for each interaction step (⌨️ Type Username, 🖱️ Click Login). At the end, you should see the `✔️ Verify redirect to dashboard` step pass.

### 6. What Failure Looks Like & How to Debug
**Trace Output**:
```
❌ Verify redirect to dashboard
↳ Message: [Timed out]
```
**How to debug**:
If you receive a `[Timed out]` exception, your `WebDriverWait` never found the intended URL. Was your password wrong? If you entered an invalid password, the PRG redirect never fired, and the page simply refreshed `login.html` instead! Always test your flows manually in the **App Preview** before executing the headless browser to ensure you understand the flow logic.
