from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

driver.get("http://mock-cms:8765/refresh")

sensor = driver.find_element(By.CSS_SELECTOR, "[data-testid='sensor-reading']")
old_value = sensor.text

driver.find_element(By.CSS_SELECTOR, "[data-testid='refresh-button']").click()
time.sleep(1)

try:
    new_value = sensor.text
    assert False, "Should have thrown a Stale Element Exception!"
except StaleElementReferenceException:
    pass

new_sensor = driver.find_element(By.CSS_SELECTOR, "[data-testid='sensor-reading']")
assert old_value != new_sensor.text, "Value didn't update!"

print("SENSOR_UPDATED")
driver.quit()
