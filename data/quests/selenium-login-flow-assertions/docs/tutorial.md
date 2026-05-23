# Tutorial: Multi-Step Assertions

Basic interactions are great, but the heart of QA is verifying state after a sequence of actions. In this quest, you will build a true End-to-End (E2E) assertion script.

### 1. What You're Testing
You will automate the `/login` flow, force the driver to wait for the `/dashboard` redirect, and formally verify that the UI loaded correctly by asserting both the URL and the textual content of the page.

### 2. Key Concept: State Dependency
When you combine actions with assertions, you create a **state dependency**. 
**Analogy**: You log into your bank. You must first assert that you are on the "Accounts" page (URL check) before asserting that your balance actually says "$100" (DOM check). If you try to read your balance before the URL changes, your script crashes!

### 3. Step-by-Step Breakdown
1. **Navigate**: Open the `/login` page.
2. **Interact**: `send_keys` to the username and password fields. `click()` the submit button.
3. **Wait**: Use `WebDriverWait` to block until the URL contains `/dashboard`.
4. **Assert State**: Use Python's `assert` to verify the URL contains `/dashboard`.
5. **Assert Content**: Locate the `[data-testid='dashboard-title']` and `assert` that it contains the word "admin".
6. **Pass**: Print `ASSERTIONS_PASSED` to complete the quest.

### 4. Example Code Summary
```python
# 1 & 2. Assume you have already clicked login
login_btn.click()

# 3. Wait for the PRG Redirect
WebDriverWait(driver, 5).until(lambda d: "/dashboard" in d.current_url)

# 4 & 5. Prove the state is correct
assert "/dashboard" in driver.current_url, "Redirect failed!"

title = driver.find_element(By.CSS_SELECTOR, "[data-testid='dashboard-title']")
assert "admin" in title.text.lower(), "Welcome text missing!"

print("ASSERTIONS_PASSED")
```

### 5. How to Verify Success
In your **Automation Trace**, you will see sequential green checks for the navigation, typing, and clicking. Finally, if your URL and DOM assertions pass, you will capture the flag!

### 6. What Failure Looks Like & How to Debug
**Trace Output**:
```
❌ [Timed out]
```
**How to Debug**: If your script hangs right after clicking the login button, you likely supplied the wrong credentials or forgot to use an explicit wait. If it throws an `AssertionError` on the text check, ensure you are locating the correct `data-testid` in the **App Preview**!
