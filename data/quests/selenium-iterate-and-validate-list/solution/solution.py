from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

driver.get("http://mock-cms:8765/tickets")

ticket_rows = driver.find_elements(By.CSS_SELECTOR, "[data-testid='ticket-row']")
assert len(ticket_rows) == 4, f"Expected 4 rows, found {len(ticket_rows)}"

valid_statuses = ["Open", "Closed", "Pending"]
for row in ticket_rows:
    status_element = row.find_element(By.CSS_SELECTOR, "[data-testid='ticket-status']")
    status_text = status_element.text
    assert status_text in valid_statuses, f"Invalid status {status_text} found!"

print("ALL_TICKETS_VALIDATED")
driver.quit()
