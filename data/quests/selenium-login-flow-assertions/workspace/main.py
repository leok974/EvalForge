import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Selenium Trace Logger ---
# Import the step logger to build your Automation Trace visual
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

# The target URL is injected by the EvalForge harness or environment
APP_URL = os.environ.get("EVALFORGE_APP_URL", "http://mock-cms:8765/login")

# Setup headless Chrome options for server rendering
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the driver
driver = webdriver.Chrome(
    service=Service("/usr/bin/chromedriver"),
    options=options
)

try:
    # 1. Start your trace with a navigation step
    logger.step("navigate", "Open page: target URL", url=APP_URL)
    driver.get(APP_URL)
    logger.pass_step()

    # TODO: Fill in username ('admin') and password ('secret123')
    # Use logger.step("type", "Type username: admin", selector="...")
    # driver.find_element(...).send_keys("admin")
    # logger.pass_step()
    
    # TODO: Click login submit
    
    # TODO: Wait until '/dashboard' is in driver.current_url
    
    # TODO: Find the dashboard title and assert the word 'dashboard' is in it
    
    # TODO: Output "ASSERTIONS_PASSED" to the console
    pass

except Exception as e:
    # Capture failures in the trace for debugging help!
    logger.fail_step(str(e)[:200])
    raise
finally:
    # 3. Always emit the trace and close the driver
    logger.emit()
    driver.quit()
