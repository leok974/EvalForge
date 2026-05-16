import os
from selenium import webdriver
from selenium.webdriver.by import By
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

    # TODO: Find username field using [data-testid='login-username']
    # user_field = ...

    # TODO: Find password field using [data-testid='login-password']
    # pass_field = ...

    # TODO: Find submit button using [data-testid='login-submit']
    # submit_btn = ...

    # print(f"STATUS_VALUE: username={user_field.tag_name}, password={pass_field.tag_name}, submit={submit_btn.tag_name}")
    pass

finally:
    driver.quit()
