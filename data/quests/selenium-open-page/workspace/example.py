import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def check_title():
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
        driver.get(app_url)
        title = driver.title
        print(f"TITLE_MATCH: {title}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_title()
