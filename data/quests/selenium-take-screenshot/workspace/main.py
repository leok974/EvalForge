import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

APP_URL = os.environ.get("EVALFORGE_APP_URL", "http://127.0.0.1:8765/login")
ARTIFACT_DIR = os.environ.get("EVALFORGE_ARTIFACT_DIR", "./artifacts")

# Ensure directory exists
if not os.path.exists(ARTIFACT_DIR):
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service("/usr/bin/chromedriver"),
    options=options
)

try:
    driver.get(APP_URL)

    # 1. Log in
    driver.find_element(By.CSS_SELECTOR, "[data-testid='login-username']").send_keys("admin")
    driver.find_element(By.CSS_SELECTOR, "[data-testid='login-password']").send_keys("secret123")
    driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']").click()

    # 2. Take screenshot
    # TODO: screenshot_path = os.path.join(ARTIFACT_DIR, "dashboard_evidence.png")
    # TODO: driver.save_screenshot(screenshot_path)
    # print(f"SCREENSHOT_SAVED: {screenshot_path}")
    pass

finally:
    driver.quit()
