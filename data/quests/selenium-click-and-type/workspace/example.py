import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- EvalForge Step Logger (graceful fallback) ---
try:
    sys.path.insert(0, '/app/runtimes/python/selenium')
    from step_logger import SeleniumStepLogger
    from helpers import open_page, type_text, click
except ImportError:
    class SeleniumStepLogger:
        def step(self, *a, **k): pass
        def pass_step(self): pass
        def fail_step(self, e=""): pass
        def emit(self): pass
    def open_page(driver, url, logger, label=None):
        driver.get(url)
    def type_text(driver, selector, text, logger, label=None, by=By.CSS_SELECTOR):
        el = driver.find_element(by, selector)
        el.clear()
        el.send_keys(text)
    def click(driver, selector, logger, label=None, by=By.CSS_SELECTOR):
        driver.find_element(by, selector).click()


def do_login():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=options
    )

    logger = SeleniumStepLogger()
    try:
        app_url = os.environ.get("EVALFORGE_APP_URL", "http://localhost:8765")

        open_page(driver, app_url, logger, label="Open page: CMS Login")

        type_text(driver, "[data-testid='login-username']", "admin",
                  logger, label="Type username: admin")

        type_text(driver, "[data-testid='login-password']", "secret123",
                  logger, label="Type password: ••••••••")

        click(driver, "[data-testid='login-submit']",
              logger, label="Click: Login button")

        logger.step("assert", "Verify redirect to dashboard", url=driver.current_url)
        assert "/dashboard" in driver.current_url, \
            f"Expected /dashboard in URL, got: {driver.current_url}"
        logger.pass_step()

        print(f"LOGIN_SUCCESS: {driver.current_url}")
    except Exception as e:
        logger.fail_step(str(e)[:200])
        raise
    finally:
        logger.emit()
        driver.quit()


if __name__ == "__main__":
    do_login()
