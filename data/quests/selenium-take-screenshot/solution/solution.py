import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

APP_URL = os.environ.get("EVALFORGE_APP_URL")
ARTIFACT_DIR = os.environ.get("EVALFORGE_ARTIFACT_DIR")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

    from selenium.webdriver.chrome.service import Service
    driver = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=options
    )

try:
    driver.get(APP_URL)
    driver.find_element(By.CSS_SELECTOR, "[data-testid='login-username']").send_keys("admin")
    driver.find_element(By.CSS_SELECTOR, "[data-testid='login-password']").send_keys("secret123")
    driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']").click()
    
    screenshot_path = os.path.join(ARTIFACT_DIR, "dashboard_evidence.png")
    driver.save_screenshot(screenshot_path)
    
    assert os.path.exists(screenshot_path)
    print(f"Verified: Screenshot saved to {screenshot_path}")
finally:
    driver.quit()
