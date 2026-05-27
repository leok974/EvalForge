from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

driver.get("http://mock-cms:8765/login")

# Send keys
driver.find_element(By.CSS_SELECTOR, "[data-testid='login-username']").send_keys("admin")
driver.find_element(By.CSS_SELECTOR, "[data-testid='login-password']").send_keys("secret123")

# Click
driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']").click()

# Explicit Wait for redirect
WebDriverWait(driver, 5).until(lambda d: "/dashboard" in d.current_url)

# Assert URL
assert "/dashboard" in driver.current_url

# Assert Text
dashboard_title = driver.find_element(By.CSS_SELECTOR, "[data-testid='dashboard-title']")
assert "dashboard" in dashboard_title.text.lower()

print("ASSERTIONS_PASSED")
driver.quit()
