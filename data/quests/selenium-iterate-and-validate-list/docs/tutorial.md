# Tutorial: Iterating & Validating Lists

In quality assurance, tables and lists are everywhere. Instead of targeting one specific item, your job is often to verify that *every* visible item in a dataset adheres to the correct business logic.

### 1. What You're Testing
You will navigate to an IT Support queue (`/tickets`). You will read the status of every single ticket displayed in the HTML table and ensure no corrupted or invalid statuses exist.

### 2. Key Concept: Element Collections
So far you have used `driver.find_element()` (singular). If you pass `By.CSS_SELECTOR` to this method and 5 buttons match, Selenium just returns the very first one it finds and ignores the rest!

To capture all of them, use `driver.find_elements()` (plural syntax!). This returns a standard Python `list` containing multiple WebElements. 
**Analogy**: 
- `find_element` is asking: "Give me the first apple you see."
- `find_elements` is asking: "Give me a basket containing every apple you see."

Furthermore, WebElements are nested! You can call `find_element` *on another WebElement* to restrict your search strictly inside that element's chunk of HTML.

### 3. Step-by-Step Breakdown
1. **Navigate**: Open `/tickets`.
2. **Plural Search**: Use `ticket_rows = driver.find_elements(By.CSS_SELECTOR, "[data-testid='ticket-row']")`.
3. **Loop**: Iterate over the Python list using a standard `for row in ticket_rows:` loop.
4. **Nested Search**: Inside the loop, check the current `row` variable specifically: `status = row.find_element(By.CSS_SELECTOR, "[data-testid='ticket-status']")`.
5. **Assert Context**: Assert that `status.text` is a valid string.

### 4. Example Code Summary
```python
from selenium.webdriver.common.by import By

driver.get(app_url)

# PLURAL! Returns a List.
rows = driver.find_elements(By.CSS_SELECTOR, "[data-testid='ticket-row']")
assert len(rows) > 0, "No tickets found!"

valid_options = ["Open", "Closed", "Pending"]

for row in rows:
    # Nested search! Only looks inside this specific <tr> tag
    status_td = row.find_element(By.CSS_SELECTOR, "[data-testid='ticket-status']")
    
    # Assert
    assert status_td.text in valid_options, f"Corrupted ticket status: {status_td.text}"

print("ALL_TICKETS_VALIDATED")
```

### 5. How to Verify Success
In your **Automation Trace**, you won't see separate steps for every single iteration unless you manually log them. When your loop completes successfully and doesn't hit the `AssertionError`, it prints the magic phrase to pass the quest.

### 6. What Failure Looks Like & How to Debug
**Trace Output**:
```
❌ AssertionError: Corrupted ticket status: Refunded
```
**How to Debug**: If your assertion fails midway through the loop, the trace will crash immediately. Ensure your `valid_options` list covers all the business logic cases shown in the target App Preview!
