import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# The target URL is injected by the EvalForge harness
APP_URL = os.environ.get("EVALFORGE_APP_URL", "http://127.0.0.1:8765/login")

# Setup headless Chrome options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the driver
from selenium.webdriver.chrome.service import Service
driver = webdriver.Chrome(
    service=Service("/usr/bin/chromedriver"),
    options=options
)

try:
    # TODO: Navigate to APP_URL
    
    # TODO: Assert driver.title matches "CMS Login"
    pass

finally:
    # Always close the driver
    driver.quit()
