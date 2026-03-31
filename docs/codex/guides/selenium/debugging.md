# Debugging Selenium Failures

Selenium operates an invisible browser in the background. Because you cannot see it, debugging failures requires reading the **Automation Trace** like a detective. 

Below are the most common failures you will encounter in EvalForge and in the real world, and exactly how to solve them.

---

## 1. Element Not Found (`NoSuchElementException`)
**What the Trace shows**:
```
❌ Verify redirect to dashboard
↳ Message: no such element: Unable to locate element: {"method":"css selector","selector":"[data-testid='wrong-id']"}
```
**Why it happened**: Selenium tried to interact with an element before it existed, or the locator you provided is completely wrong.
**The Fix**:
1. Check your spelling. A typo in a `data-testid` is the #1 culprit.
2. Use the **App Preview** in EvalForge to right-click -> Inspect the element and verify its `data-testid`.
3. If the element loads dynamically (e.g. after a spinner), you need to wait for it (see *Race Conditions* below).

## 2. Timeout Exception (`TimeoutException`)
**What the Trace shows**:
```
❌ Read and assert dashboard title
↳ Message: [Timed out]
```
**Why it happened**: You used `WebDriverWait(driver, 5).until(...)` and the condition did not become true within 5 seconds.
**The Fix**:
1. Is the mock CMS running slowly? EvalForge routes like `/latency` often have intentional 3-5 second delays. Try increasing your timeout to `10` or `15`.
2. Did the page actually navigate? If you clicked a button but the URL never changed, you may be waiting for a URL that will never arrive. Verify the step *before* the timeout.

## 3. The Click "Did Nothing" (Page didn't navigate)
**What the Trace shows**:
```
❌ Verify redirect to dashboard
↳ AssertionError: Expected /dashboard in URL, got: http://mock-cms:8765/login
```
**Why it happened**: Sometimes submitting a form does not magically flip the browser URL. In modern apps using the PRG (Post-Redirect-Get) pattern, jumping from `/login` to `/dashboard` takes a few milliseconds of network overhead. If you `assert` the URL immediately after clicking, you will check the URL *before* the redirect finishes.
**The Fix**: Block the script until the redirect finishes!
```python
# Bad: Race condition!
submit_button.click()
assert "/dashboard" in driver.current_url

# Good: Wait for the network
submit_button.click()
WebDriverWait(driver, 5).until(lambda d: "/dashboard" in d.current_url)
assert "/dashboard" in driver.current_url
```

## 4. Stale Element Reference (`StaleElementReferenceException`)
**Why it happened**: You found an element, assigned it to a variable, the page reloaded or React re-rendered, and *then* you tried to click that variable. The DOM element has been destroyed and recreated!
**The Fix**: Always re-query the element right before you need it.
```python
# Bad
btn = driver.find_element(By.CSS_SELECTOR, "button")
driver.refresh()
btn.click() # Fails immediately

# Good
btn = driver.find_element(By.CSS_SELECTOR, "button")
driver.refresh()
btn = driver.find_element(By.CSS_SELECTOR, "button") # Find it again!
btn.click()
```

## 5. Using the Automation Trace
When a quest fails, **always scroll to the bottom of the Terminal Console to check the Automation Trace**.

Every step represents one action (like `Navigate`, `Type`, `Click`, `Wait`, `Screenshot`). A green checkmark ✅ means the step passed. A red cross ❌ means the step crashed.
Look at the *last successful step* to understand what state the browser was in right before the failure.
