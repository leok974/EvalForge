import os
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    user_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-username']")
    pass_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-password']")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']")
    
    assert user_field.tag_name == "input"
    assert pass_field.tag_name == "input"
    assert submit_btn.tag_name == "button"
    
    print(f"Verified: Found {user_field.tag_name}, {pass_field.tag_name}, {submit_btn.tag_name}")
finally:
    driver.quit()
