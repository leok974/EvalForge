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
    app_url = "http://mock-cms:8765/latency?delay=0.5"

    try:
        logger.step("navigate", "Open page: target URL", url=app_url)
        driver.get(app_url)
        logger.pass_step()

        logger.step("wait", "Wait for sync button to appear", selector="[data-testid='confirm-sync']")
        box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='confirm-sync']"))
        )
        logger.pass_step()

        logger.step("click", "Click confirm sync button", selector="[data-testid='confirm-sync']")
        box.click()
        logger.pass_step()

        print("SYNC_CONFIRMED")

    except Exception as e:
        logger.fail_step(str(e)[:200])
        raise
    finally:
        logger.emit()
        driver.quit()

if __name__ == "__main__":
    print("INFO--- Running example.py (Reference) ---")
    run_example()
