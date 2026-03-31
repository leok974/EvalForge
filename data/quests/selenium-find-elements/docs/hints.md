## Hint 1
Look at the DOM structure in the App Preview to find the exact `data-testid` values for the username and password fields.

## Hint 2
Use `driver.find_element(By.CSS_SELECTOR, "[data-testid='...']")` to grab the elements. Make sure you don't use `find_elements` (plural) unless you want a list!
