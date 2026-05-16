import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    from step_logger import SeleniumStepLogger
    logger = SeleniumStepLogger()
except ImportError:
    class SeleniumStepLogger:
        def step(self, action, label, **kwargs): pass
        def pass_step(self): pass
        def fail_step(self, err=""): pass
        def emit(self): pass
    logger = SeleniumStepLogger()

APP_URL = os.environ.get("EVALFORGE_APP_URL", "http://mock-cms:8765/login")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
wait = WebDriverWait(driver, 10)

try:
    logger.step("navigate", "Navigate to CMS login page", url=APP_URL)
    driver.get(APP_URL)
    wait.until(EC.title_contains("CMS Login"))
    logger.pass_step()

    title = driver.title
    print(f"TITLE_MATCH: {title}")

except Exception as e:
    logger.fail_step(str(e)[:200])
    raise
finally:
    logger.emit()
    driver.quit()
