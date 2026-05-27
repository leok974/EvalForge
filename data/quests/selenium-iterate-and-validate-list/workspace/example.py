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
    app_url = "http://mock-cms:8765/tickets"

    try:
        logger.step("navigate", "Open page: target URL", url=app_url)
        driver.get(app_url)
        logger.pass_step()

        logger.step("assert", "Verify ticket count is exactly 4", selector="[data-testid='ticket-row']")
        ticket_rows = driver.find_elements(By.CSS_SELECTOR, "[data-testid='ticket-row']")
        assert len(ticket_rows) == 4, f"Expected 4 rows, found {len(ticket_rows)}"
        logger.pass_step()

        valid_statuses = ["Open", "Closed", "Pending"]
        
        for i, row in enumerate(ticket_rows):
            logger.step("assert", f"Verify ticket {i+1} valid status", selector="[data-testid='ticket-status']")
            status_element = row.find_element(By.CSS_SELECTOR, "[data-testid='ticket-status']")
            assert status_element.text in valid_statuses, f"Invalid status {status_element.text}"
            logger.pass_step()

        print("ALL_TICKETS_VALIDATED")

    except Exception as e:
        logger.fail_step(str(e)[:200])
        raise
    finally:
        logger.emit()
        driver.quit()

if __name__ == "__main__":
    print("INFO--- Running example.py (Reference) ---")
    run_example()
