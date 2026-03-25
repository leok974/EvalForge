import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

# --- EvalForge Step Logger ---
# Provides structured automation trace for the learner view
try:
    import sys
    sys.path.insert(0, '/app/runtimes/python/selenium')
    from step_logger import SeleniumStepLogger
    from helpers import open_page
    _use_helpers = True
except ImportError:
    _use_helpers = False
    class SeleniumStepLogger:
        def step(self, *a, **k): pass
        def pass_step(self): pass
        def fail_step(self, e=""): pass
        def emit(self): pass

def check_title():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    from selenium.webdriver.chrome.service import Service
    driver = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=chrome_options
    )

    logger = SeleniumStepLogger()
    try:
        app_url = os.environ.get("EVALFORGE_APP_URL", "http://localhost:8765")

        if _use_helpers:
            open_page(driver, app_url, logger, label="Open page: CMS Login")
        else:
            logger.step("navigate", f"Open page: {app_url}", url=app_url)
            driver.get(app_url)
            logger.pass_step()

        logger.step("assert", "Verify page title matches 'CMS Login'", url=driver.current_url)
        title = driver.title
        assert title == "CMS Login", f"Expected 'CMS Login', got '{title}'"
        logger.pass_step()

        print(f"TITLE_MATCH: {title}")
    except Exception as e:
        logger.fail_step(str(e)[:200])
        raise
    finally:
        logger.emit()
        driver.quit()

if __name__ == "__main__":
    check_title()
