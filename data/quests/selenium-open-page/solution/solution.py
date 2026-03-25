import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

APP_URL = os.environ.get("EVALFORGE_APP_URL")

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
    assert "CMS Login" in driver.title
    print("Verification Successful: Title matches.")
finally:
    driver.quit()
