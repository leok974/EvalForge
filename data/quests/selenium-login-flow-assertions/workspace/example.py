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
    app_url = "http://mock-cms:8765/login"

    try:
        logger.step("navigate", "Open page: target URL", url=app_url)
        driver.get(app_url)
        logger.pass_step()

        logger.step("type", "Type username: admin", selector="[data-testid='login-username']")
        user_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-username']")
        user_input.send_keys("admin")
        logger.pass_step()

        logger.step("type", "Type password: ••••••••", selector="[data-testid='login-password']")
        pass_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-password']")
        pass_input.send_keys("secret123")
        logger.pass_step()

        logger.step("click", "Click: Login button", selector="[data-testid='login-submit']")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']").click()
        logger.pass_step()

        logger.step("assert", "Verify redirect to dashboard", url=driver.current_url)
        WebDriverWait(driver, 5).until(lambda d: "/dashboard" in d.current_url)
        assert "/dashboard" in driver.current_url
        logger.pass_step()

        logger.step("assert", "Verify dashboard title contains 'dashboard'")
        dashboard_title = driver.find_element(By.CSS_SELECTOR, "[data-testid='dashboard-title']")
        assert "dashboard" in dashboard_title.text.lower()
        logger.pass_step()

        print("ASSERTIONS_PASSED")

    except Exception as e:
        logger.fail_step(str(e)[:200])
        raise
    finally:
        logger.emit()
        driver.quit()

if __name__ == "__main__":
    print("INFO--- Running example.py (Reference) ---")
    run_example()
