import os
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- EvalForge Step Logger (graceful fallback) ---
try:
    from step_logger import SeleniumStepLogger
    from helpers import open_page, type_text, click, wait_for
except ImportError:
    class SeleniumStepLogger:
        def step(self, *a, **k): pass
        def pass_step(self): pass
        def fail_step(self, e=""): pass
        def emit(self): pass
    def open_page(driver, url, logger, label=None): driver.get(url)
    def type_text(driver, s, text, logger, label=None, by=By.CSS_SELECTOR):
        el = driver.find_element(by, s); el.clear(); el.send_keys(text)
    def click(driver, s, logger, label=None, by=By.CSS_SELECTOR):
        driver.find_element(by, s).click()
    def wait_for(driver, cond, logger, label=None, timeout=10.0):
        return WebDriverWait(driver, timeout).until(cond)


def read_and_assert():
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

        wait_for(
            driver,
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='dashboard-title']")),
            logger,
            label="Wait for: dashboard title element",
        )

        logger.step("assert", "Read and assert dashboard title text",
                    selector="[data-testid='dashboard-title']", url=driver.current_url)
        title_el = driver.find_element(By.CSS_SELECTOR, "[data-testid='dashboard-title']")
        title_text = title_el.text.strip()
        assert "Welcome" in title_text or "Dashboard" in title_text, \
            f"Unexpected title: '{title_text}'"
        logger.pass_step()

        print(f"Dashboard Title: {title_text}")
    except Exception as e:
        logger.fail_step(str(e)[:200])
        raise
    finally:
        logger.emit()
        driver.quit()


if __name__ == "__main__":
    read_and_assert()
