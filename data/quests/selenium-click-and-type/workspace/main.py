import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

APP_URL = os.environ.get("EVALFORGE_APP_URL", "http://127.0.0.1:8765/login")

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

    # TODO: Find username field and type "admin"

    # TODO: Find password field and type "secret123"

    # TODO: Click login button

    # TODO: Wait for dashboard and print LOGIN_SUCCESS
    pass

finally:
    driver.quit()
