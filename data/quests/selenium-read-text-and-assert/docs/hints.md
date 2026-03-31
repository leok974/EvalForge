# Hints

Need a little help? Here are a few tips to guide you:

1. Use `.text` to extract the visible string from a WebElement.
2. Don't forget `WebDriverWait(driver, 10).until(EC.presence_of_element_located(...))` before trying to find the title.
3. Your assertion statement `assert "Welcome" in title_el.text` should run after the page loads.
