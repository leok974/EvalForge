import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
    logger.pass_step()

    logger.step("type", "Enter username", selector="[data-testid='login-username']")
    username = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-username']"))
    )
    username.send_keys("admin")
    logger.pass_step()

    logger.step("type", "Enter password", selector="[data-testid='login-password']")
    password = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-password']"))
    )
    password.send_keys("secret123")
    logger.pass_step()

    logger.step("click", "Click login submit", selector="[data-testid='login-submit']")
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='login-submit']"))
    )
    submit.click()
    logger.pass_step()

    # Wait for redirect to dashboard
    logger.step("wait", "Wait for dashboard to load")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='dashboard-title']")))
    logger.pass_step()

    print("LOGIN_SUCCESS")

except Exception as e:
    logger.fail_step(str(e)[:200])
    raise
finally:
    logger.emit()
    driver.quit()
