import os
import sys
from selenium import webdriver
from selenium.webdriver.by import By
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
    def open_page(driver, url, logger, label=None): driver.get(url)
    def type_text(driver, s, text, logger, label=None, by=By.CSS_SELECTOR):
        el = driver.find_element(by, s); el.clear(); el.send_keys(text)
    def click(driver, s, logger, label=None, by=By.CSS_SELECTOR):
        driver.find_element(by, s).click()


def take_screenshot():
    app_url = os.environ.get("EVALFORGE_APP_URL", "http://localhost:8765")
    artifact_dir = os.environ.get("EVALFORGE_ARTIFACT_DIR", "./artifacts")
    os.makedirs(artifact_dir, exist_ok=True)

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
        open_page(driver, app_url, logger, label="Open page: CMS Login")

        type_text(driver, "[data-testid='login-username']", "admin",
                  logger, label="Type username: admin")
        type_text(driver, "[data-testid='login-password']", "secret123",
                  logger, label="Type password: ••••••••")
        click(driver, "[data-testid='login-submit']",
              logger, label="Click: Login button")

        logger.step("screenshot", "Save dashboard screenshot",
                    url=driver.current_url)
        screenshot_path = os.path.join(artifact_dir, "dashboard_evidence.png")
        driver.save_screenshot(screenshot_path)
        assert os.path.exists(screenshot_path), "Screenshot file not found"
        logger.pass_step()

        print(f"SCREENSHOT_SAVED: {screenshot_path}")
    except Exception as e:
        logger.fail_step(str(e)[:200])
        raise
    finally:
        logger.emit()
        driver.quit()


if __name__ == "__main__":
    take_screenshot()
