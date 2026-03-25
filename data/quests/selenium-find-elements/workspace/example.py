import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def check_status():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    from selenium.webdriver.chrome.service import Service
    driver = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=chrome_options
    )
    try:
        app_url = os.environ.get("EVALFORGE_APP_URL", "http://localhost:8765")
        driver.get(f"{app_url}/dashboard")
        # In a real environment, we might need a wait here, but the mock app is fast.
        status_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="core-status"]')
        print(f"STATUS_VALUE: {status_element.text}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_status()
