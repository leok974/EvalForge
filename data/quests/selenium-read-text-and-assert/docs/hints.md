## Hint 1
Use `.text` to extract the visible string from a WebElement.

## Hint 2
Don't forget `WebDriverWait(driver, 10).until(EC.presence_of_element_located(...))` before trying to find the title.

## Hint 3
Your assertion statement `assert "Welcome" in title_el.text` should run after the page loads.
