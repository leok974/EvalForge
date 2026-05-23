import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    from step_logger import SeleniumStepLogger
    _has_logger = True
except ImportError:
    _has_logger = False
    class SeleniumStepLogger:
        def step(self, name, desc, **kwargs): pass
        def pass_step(self): pass
        def fail_step(self, err): pass
        def emit(self): pass

def run_example():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        from selenium.webdriver.chrome.service import Service
        driver = webdriver.Chrome(
            service=Service("/usr/bin/chromedriver"),
            options=chrome_options
        )
    except Exception:
        from selenium import webdriver
        driver = webdriver.Chrome(options=chrome_options)

    logger = SeleniumStepLogger()
    app_url = "http://mock-cms:8765/refresh"

    try:
        logger.step("navigate", "Open page: target URL", url=app_url)
        driver.get(app_url)
        logger.pass_step()

        from selenium.common.exceptions import StaleElementReferenceException
        import time

        logger.step("find", "Find sensor reading", selector="[data-testid='sensor-reading']")
        sensor = driver.find_element(By.CSS_SELECTOR, "[data-testid='sensor-reading']")
        old_value = sensor.text
        logger.pass_step()

        logger.step("click", "Click refresh button", selector="[data-testid='refresh-button']")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='refresh-button']").click()
        logger.pass_step()

        logger.step("wait", "Allowing DOM mutation (1s)")
        time.sleep(1)
        logger.pass_step()

        logger.step("try", "Trap StaleElementReferenceException")
        try:
            new_value = sensor.text
            assert False, "Should have thrown a Stale Element Exception!"
        except StaleElementReferenceException:
            pass
        logger.pass_step()

        logger.step("assert", "Re-fetch sensor and verify updated value", selector="[data-testid='sensor-reading']")
        new_sensor = driver.find_element(By.CSS_SELECTOR, "[data-testid='sensor-reading']")
        assert old_value != new_sensor.text, "Value didn't update!"
        logger.pass_step()

        print("SENSOR_UPDATED")

    except Exception as e:
        logger.fail_step(str(e)[:200])
        raise
    finally:
        logger.emit()
        driver.quit()

if __name__ == "__main__":
    print("INFO--- Running example.py (Reference) ---")
    run_example()
