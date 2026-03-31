import os
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- EvalForge Step Logger (graceful fallback) ---
try:
    from step_logger import SeleniumStepLogger
    from helpers import open_page, find
except ImportError:
    class SeleniumStepLogger:
        def step(self, *a, **k): pass
        def pass_step(self): pass
        def fail_step(self, e=""): pass
        def emit(self): pass
    def open_page(driver, url, logger, label=None):
        driver.get(url)
    def find(driver, selector, logger, label=None, by=By.CSS_SELECTOR):
        return driver.find_element(by, selector)


def check_status():
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

        open_page(driver, f"{app_url}/dashboard", logger, label="Open page: /dashboard")

        logger.step("find", "Find element: [data-testid='core-status']",
                    selector="[data-testid='core-status']", url=driver.current_url)
        status_element = driver.find_element(By.CSS_SELECTOR, "[data-testid='core-status']")
        logger.pass_step()

        logger.step("assert", "Read status value", url=driver.current_url)
        value = status_element.text.strip()
        logger.pass_step()

        print(f"STATUS_VALUE: {value}")
    except Exception as e:
        logger.fail_step(str(e)[:200])
        raise
    finally:
        logger.emit()
        driver.quit()


if __name__ == "__main__":
    check_status()
