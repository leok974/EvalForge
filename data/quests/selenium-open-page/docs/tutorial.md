# Tutorial: Eyes on the Target

Welcome to your first Selenium automation task!

### 1. What You're Testing
In this quest, you will verify that the EvalForge Mock CMS `/login` page is properly accessible. You will write an automated script to open a headless web browser, navigate to the local mock environments, and ensure the page's `<title>` tag is exactly `"CMS Login"`.

### 2. Key Concept: The WebDriver 
Selenium is not a browser; it is a **WebDriver bridge** that sends programmatic commands to a real browser (like Chrome). 
**Analogy**: Think of Selenium as a remote control and the browser as your TV. When you run `driver.get(url)`, Selenium pushes the "channel up" button, forcing the browser to load the page.

*Note on EvalForge Environments:* The **App Preview** panel on your right is a sandbox iframe. It shows you the Mock CMS for visual reference, but your Python script will spawn a completely separate, invisible ("headless") Chrome instance in the background!

### 3. Step-by-Step Breakdown
1. **Initialize the Driver**: We provide the `driver` object to you in the harness.
2. **Navigate**: Use the `.get()` method to navigate to the `app_url`.
3. **Inspect**: Read the `.title` property of the browser to see the current page title.
4. **Assert**: Compare the title to `"CMS Login"`. If it does not match, throw an `AssertionError`.

### 4. Example Code Summary

```python
# 1. Drive to the URL
driver.get(app_url)

# 2. Extract the state
title = driver.title

# 3. Prove it worked
assert title == "CMS Login", f"Expected 'CMS Login', got '{title}'"

# Log the success for the quest
print(f"TITLE_MATCH: {title}")
```

### 5. How to Verify Success
When you run the script, check the **Automation Trace** panel located at the bottom of your console. It will display a green `✅` next to the `navigate` and `assert` steps, proving that the invisible browser successfully loaded the page.

### 6. What Failure Looks Like & How to Debug
**Trace Output**:
```
❌ Verify page title matches 'CMS Login'
↳ AssertionError: Expected 'CMS Login', got 'Foundry Login'
```
**How to debug**:
If the title didn't match, your test properly caught a regression in the Mock CMS! Always check the trace to ensure the previous command (`Open page`) was successful. If the page didn't open correctly (e.g. `WebDriverException: ERR_CONNECTION_REFUSED`), the title assertion will fail. Use the **App Preview** to manually inspect the live title.
