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
    app_url = "http://mock-cms:8765/modals?show_modal=true"

    try:
        logger.step("navigate", "Open page: target URL", url=app_url)
        driver.get(app_url)
        logger.pass_step()

        logger.step("try", "Attempt to handle potential modal overlay")
        from selenium.common.exceptions import TimeoutException
        try:
            modal_cancel = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='modal-cancel']"))
            )
            logger.step("click", "Dismiss modal", selector="[data-testid='modal-cancel']")
            modal_cancel.click()
            logger.pass_step()
            
            logger.step("wait", "Wait for modal to fade out")
            WebDriverWait(driver, 2).until(
                EC.invisibility_of_element((By.CSS_SELECTOR, "[data-testid='override-modal']"))
            )
            logger.pass_step()
        except TimeoutException:
            pass
        logger.pass_step()

        logger.step("click", "Click primary trigger", selector="[data-testid='trigger-override']")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='trigger-override']").click()
        logger.pass_step()

        print("DEFENSE_ACTIVE")

    except Exception as e:
        logger.fail_step(str(e)[:200])
        raise
    finally:
        logger.emit()
        driver.quit()

if __name__ == "__main__":
    print("INFO--- Running example.py (Reference) ---")
    run_example()
