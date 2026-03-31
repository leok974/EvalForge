# Tutorial: The Hunt for ID

After opening a page, you need to find the specific elements you want to interact with!

### 1. What You're Testing
In this quest, you will scan the Mock CMS `/login` page to locate the username and password input fields using `data-testid` attributes.

### 2. Key Concept: Element Locators (`By`)
To interact with an element, you must first ask the browser to search the DOM (Document Object Model) for it. 
**Analogy**: Finding an element is like looking for a book in a library. You need the exact call number (the *selector*) to give to the librarian (Selenium `webdriver`).

In modern automation, never construct fragile selectors based on tag hierarchy (like `div > form > span > input`). Instead, use explicit testing IDs like `data-testid="login-username"`. 

The most robust way to locate elements is via `By.CSS_SELECTOR`:
`driver.find_element(By.CSS_SELECTOR, "[data-testid='login-username']")`

### 3. Step-by-Step Breakdown
1. **App Preview Inspect**: Open your App Preview. Right-click the Username field and select **Inspect**. You will see the `data-testid` attached to the HTML element.
2. **Find Element**: In your Python script, import `By` from `selenium.webdriver.common.by`.
3. **Execute Query**: Use `driver.find_element` to locate the target elements.

### 4. Example Code Summary

```python
from selenium.webdriver.common.by import By

# 1. Ask Selenium to find the element
username_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-username']")
password_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-password']")

# 2. Output success
print(f"STATUS_VALUE field: {username_field}")
```

### 5. How to Verify Success
Your script will emit a valid string representing the `WebElement` object found in memory. The **Automation Trace** will show a green `✅` next to your element lookup, proving you queried the page correctly.

### 6. What Failure Looks Like & How to Debug
**Trace Output**:
```
❌ Find Username Input
↳ NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"[data-testid='loginn-userr']"}
```
**How to debug**:
If you receive a `NoSuchElementException`, your selector failed to match any element in the DOM. This happens instantly!
Check your spelling in the CSS Selector `[data-testid='...']` against the real source code shown in the **App Preview**. Validate that the element isn't hidden by a modal or hasn't finished loading.
